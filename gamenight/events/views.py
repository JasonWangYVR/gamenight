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
#include forms
from .forms import EventForm, QuestionForm, ChoiceForm, MessageForm

def index(request):
    #title = 'GameNight Event List'
    #TODO: filter for user created and invited
    event = Event.objects.order_by('title')
    context = {
        'event': event,
            }
    return render(request, 'events/index.html', context)

def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    question = Question.objects.filter(on_event=event.pk)
    choice = Choice.objects.filter(question_id__in=question)
    message = Message.objects.filter(on_event=event.pk)

    context = {
        'event': event,
        'question' : question,
        'choice' : choice,
		'message' : message,
            }
    return render(request, 'events/event_detail.html', context)

def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.organizer = request.user
            #post.created_on = timezone.now()
            post.save()
            return redirect('events:index')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})
	
def edit_event(request, event_id):
    post = get_object_or_404(Event, pk=event_id)
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

def create_message(request, event_id):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.posted_by = request.user
            post.on_event = get_object_or_404(Event, pk=event_id)
            post.save()
            return redirect('events:detail',event_id)
    else:
        form = MessageForm()
    return render(request, 'events/create_message.html', {'form': form})

def create_question(request, event_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.on_event = get_object_or_404(Event, pk=event_id)
            #post.created_on = timezone.now()
            post.save()
            return redirect('events:detail',event_id)
    else:
        form = QuestionForm()
    return render(request, 'events/create_question.html', {'form': form})

def create_choice(request, question_id):
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.question = get_object_or_404(Question, pk=question_id)
            post.save()
            return redirect('events:index')
    else:
        form = ChoiceForm()
    return render(request, 'events/create_choice.html', {'form': form})

def edit_question(request, question_id):
    post = get_object_or_404(Question, pk=question_id)
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
	
def edit_choice(request, choice_id):
    post = get_object_or_404(Choice, pk=choice_id)
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

def edit_message(request, message_id):
    post = get_object_or_404(Message, pk=message_id)
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


def delete_question(request, question_id):
    instance = get_object_or_404(Question, pk=question_id)
    instance.delete()
    return redirect('events:index')

def delete_message(request, message_id):
    instance = get_object_or_404(Message, pk=message_id)
    instance.delete()
    return redirect('events:index')

def delete_choice(request, choice_id):
    instance = get_object_or_404(Choice, pk=choice_id)
    instance.delete()
    return redirect('events:index')

def delete_event(request, event_id):
    instance = get_object_or_404(Event, pk=event_id)
    instance.delete()
    return redirect('events:index')


def vote(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
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
