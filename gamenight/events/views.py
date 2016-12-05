import string
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import template
from django.core.urlresolvers import resolve
from django.core.exceptions import ObjectDoesNotExist
from django.core import urlresolvers
from django.db.models import Q
#utilities
from django.utils import timezone
#included models
from .models import Event, Question, Choice, Message, User
from authentication.models import UserProfile
#include forms
from .forms import EventForm, QuestionForm, ChoiceForm, MessageForm
from boardgames.forms import SearchForm

def index(request):
    #title = 'GameNight Event List'
    #TODO: filter for user created and invited
    event = Event.objects.order_by('title')
    context = {
        'event': event,
		'search': SearchForm(),
            }
    return render(request, 'events/index.html', context)

	
def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.private_event == False:
        question = Question.objects.filter(on_event=event.pk)
        choice = Choice.objects.filter(question_id__in=question)
        message = Message.objects.filter(on_event=event.pk)

        context = {
            'event': event,
            'question' : question,
            'choice' : choice,
    		'message' : message,
    		'search': SearchForm(),
                }
        return render(request, 'events/event_detail.html', context)
    else:
        if request.user.is_authenticated():
            user = UserProfile.objects.get(user=request.user, deleted=False)
            try:
                is_attending = user.attending_events.get(id=event_id)
            except ObjectDoesNotExist:
                return redirect('home:index') #Not going to this event
            question = Question.objects.filter(on_event=event.pk)
            choice = Choice.objects.filter(question_id__in=question)
            message = Message.objects.filter(on_event=event.pk)

            is_organizer = False
            if request.user == event.organizer:
                is_organizer = True

            context = {
                'event': event,
                'question' : question,
                'choice' : choice,
                'message' : message,
                'search': SearchForm(),
                'is_organizer': is_organizer,
                    }
            return render(request, 'events/event_detail.html', context)
        else:
            return redirect('authentication:login')

def add_attendee(request, event_id, username_to_add):
    event = get_object_or_404(Event, id=event_id)
    try:
        to_add = User.objects.get(username=username_to_add, deleted=False)
        try: 
            to_add_profile = UserProfile.objects.get(user=to_add)
            try:
                ok = to_add_profile.attending_events.get(id=event_id)
                message="User already attending"
            except ObjectDoesNotExist:
                to_add_profile.attending_events.add(event)
                message="User successfully added"
        except ObjectDoesNotExist:
            message="User needs to set up their profile!"
    except ObjectDoesNotExist:
        message="User does not exist"

def remove_attendee(request, event_id, user_to_remove):
    event = get_object_or_404(Event, id=event_id)
    try:
        to_remove = User.objects.get(user_to_remove, deleted=False)
        try:
            to_remove_profile = UserProfile.objects.get(user=to_remove)
            try:
                ok = to_remove_profile.attending_events.get(id=event_id)
                to_remove_profile.attending_events.remove(id=event_id)
                message="User has been successfully removed."
            except ObjectDoesNotExist:
                message="User is not attending this event."
        except ObjectDoesNotExist:
            message="User's profile does not exist"
    except ObjectDoesNotExist:
        message="User does not exist!"

def create_event(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = EventForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.organizer = request.user
                #post.created_on = timezone.now()
                post.save()

                profile = UserProfile.objects.get(user=request.user, deleted=False)
                profile.attending_events.add(post)
                return redirect('events:index')
        else:
            form = EventForm()
            return render(request, 'events/create_event.html', {'form': form})
    else:
        return redirect('authentication:login')

def edit_event(request, event_id):
	if request.user.is_authenticated():
		post = get_object_or_404(Event, pk=event_id)
		if post.organizer == request.user:	
			if request.method == "POST":
				form = EventForm(request.POST, instance=post)
				if form.is_valid():
					post = form.save(commit=False)
					post.organizer = request.user
					post.save()
					return redirect('events:index')
			else:
				form = EventForm(instance=post)
				return render(request, 'events/edit_event.html', {'form': form})
		else:
			return redirect('home:index') #must be owner of event, new page?
	else:
		return redirect('authentication:login')

def create_message(request, event_id):
    if request.user.is_authenticated():
        event = get_object_or_404(Event, pk=event_id)
        if event.private_event == False:
            if request.method == "POST":
                form = MessageForm(request.POST)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.posted_by = request.user
                    post.on_event = event
                    post.save()
                    return redirect('events:detail',event_id)
            else:
                form = MessageForm()
            return render(request, 'events/create_message.html', {'form': form})
        else:
            try:
                is_attending = user.attending_events.get(id=event_id)
                user = UserProfile.objects.get(user=request.user, deleted=False)
                if request.method == "POST":
                    form = MessageForm(request.POST)
                    if form.is_valid():
                        post = form.save(commit=False)
                        post.posted_by = request.user
                        post.on_event = event
                        post.save()
                        return redirect('events:detail',event_id)
                else:
                    form = MessageForm()
                return render(request, 'events/create_message.html', {'form': form})
            except ObjectDoesNotExist:
                return rediect('home:index') #Not going to this event
    else:
        return redirect('authentication:login')

def create_question(request, event_id):
    if request.user.is_authenticated():
        event = get_object_or_404(Event, pk=event_id)
        if event.private_event == False:
            if event.organizer == request.user:
                if request.method == "POST":
                    form = QuestionForm(request.POST)
                    if form.is_valid():
                        post = form.save(commit=False)
                        post.on_event = event
                        #post.created_on = timezone.now()
                        post.save()
                        return redirect('events:detail',event_id)
                else:
                    form = QuestionForm()
                return render(request, 'events/create_question.html', {'form': form})
            else:
                return redirect('home:index') #maybe a new page saying that he can't edit it unless he is organizer
        else:
            try:
                is_attending = user.attending_events.get(id=event_id)
                user = UserProfile.objects.get(user=request.user, deleted=False)
                if event.organizer == user:
                    if request.method == "POST":
                        form = QuestionForm(request.POST)
                        if form.is_valid():
                            post = form.save(commit=False)
                            post.on_event = event
                            #post.created_on = timezone.now()
                            post.save()
                            return redirect('events:detail',event_id)
                    else:
                        form = QuestionForm()
                    return render(request, 'events/create_question.html', {'form': form})
                else:
                    return redirect('home:index')
            except ObjectDoesNotExist:
                return rediect('home:index') #Not going to this event
    else:
        return redirect('authentication:login')
            

def create_choice(request, question_id):
    if request.user.is_authenticated():
        question = get_object_or_404(Question, pk=question_id)
        if request.method == "POST":
            form = ChoiceForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.question = question
                post.save()
                return redirect('events:index')
        else:
            form = ChoiceForm()
        return render(request, 'events/create_choice.html', {'form': form})
    else:
        return redirect('authentication:login')

def edit_question(request, question_id):
    if request.user.is_authenticated():
        post = get_object_or_404(Question, pk=question_id)
        if post.on_event.organizer == request.user:
            if request.method == "POST":
                form = QuestionForm(request.POST, instance=post)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.organizer = request.user
                    post.save()
                    return redirect('events:index')
            else:
                form = QuestionForm(instance=post)
            return render(request, 'events/create_question.html', {'form': form})
        else:
            return redirect('home:index') #not his question to edit
    else:
        return redirect('authentication:login')
	
def edit_choice(request, choice_id):
    if request.user.is_authenticated():
        post = get_object_or_404(Choice, pk=choice_id)
        if post.question.on_event.organizer == request.user:
            if request.method == "POST":
                form = ChoiceForm(request.POST, instance=post)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.organizer = request.user
                    post.save()
                    return redirect('events:index')
            else:
                form = ChoiceForm(instance=post)
            return render(request, 'events/create_choice.html', {'form': form})
        else:
            return redirect('home:index') #Not his choice to alter?
    else:
        return redirect('authentication:login')

def edit_message(request, message_id):
    if request.user.is_authenticated():
        post = get_object_or_404(Message, pk=message_id)
        if post.posted_by == request.user:
            if request.method == "POST":
                form = MessageForm(request.POST, instance=post)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.organizer = request.user
                    post.save()
                    return redirect('events:index')
            else:
                form = MessageForm(instance=post)
            return render(request, 'events/create_message.html', {'form': form})	
        else:
            return redirect('home:index') #Not his message to alter
    else:
        return redirect('authentication:login')


def delete_question(request, question_id):
    if request.user.is_authenticated():
        instance = get_object_or_404(Question, pk=question_id)
        if instance.on_event.organizer == request.user:
            instance.delete()
            return redirect('events:index')
        else:
            return redirect('home:index') #not his to touch
    else:
        return redirect('authentication:login')

def delete_message(request, message_id):
    if request.user.is_authenticated():
        instance = get_object_or_404(Message, pk=message_id)
        if instance.posted_by == request.user:
            instance.delete()
            return redirect('events:index')
        else:
            return redirect('home:index') #not his to touch
    else:
        return redirect('authentication:login')

def delete_choice(request, choice_id):
    if request.user.is_authenticated():
        instance = get_object_or_404(Choice, pk=choice_id)
        if instance.question.on_event.organizer == request.user:
            instance.delete()
            return redirect('events:index')
        else:
            return redirect('home:index') #Not his to touch
    else:
        return redirect('authentication:login')

def delete_event(request, event_id):
    if request.user.is_authenticated():
        instance = get_object_or_404(Event, pk=event_id)
        if instance.organizer == request.user:
            instance.delete()
            return redirect('events:index')
        else:
            return redirect('home:index') #not his to touch
    else:
        return redirect('authentication:login')


def vote(request, choice_id):
    if request.user.is_authenticated():
        choice = get_object_or_404(Choice, pk=choice_id)
        if choice.question.on_event.private_event == False:
            try:
                selected_choice = choice
            except (KeyError, Choice.DoesNotExist):
                # Redisplay the question voting form.
                return render(request, 'events/index.html', {
                    'choice': choice,
                    'error_message': "You didn't select a choice.",
                })
            else:
                selected_choice.votes += 1
                selected_choice.save()
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse('events:index'))
        else:
            try:
                is_attending = user.attending_events.get(id=event_id)
                try:
                    selected_choice = choice
                except (KeyError, Choice.DoesNotExist):
                    # Redisplay the question voting form.
                    return render(request, 'events/index.html', {
                        'choice': choice,
                        'error_message': "You didn't select a choice.",
                    })
                else:
                    selected_choice.votes += 1
                    selected_choice.save()
                    # Always return an HttpResponseRedirect after successfully dealing
                    # with POST data. This prevents data from being posted twice if a
                    # user hits the Back button.
                    return HttpResponseRedirect(reverse('events:index'))

            except ObjectDoesNotExist:
                return redirect('home:index')
    else:
        return redirect('authentication:login')


def public_events(request):
    title = 'Public Events'
    #TODO: filter for public
    event_list = Event.objects.filter()
    page = request.GET.get('page')
    paginator = Paginator(event_list, 10)
    try:
        event = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer, deliver first page.
        event = paginator.page(1)
    except EmptyPage:
    # If page is out of range (e.g. 9999), deliver last page of results.
        event = paginator.page(paginator.num_pages)
    #Pagination End
    context = {
        'event': event,
        'title': title
        }
    return render(request, 'events/public_events.html', context)
