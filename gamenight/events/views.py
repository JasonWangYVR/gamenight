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
            #return redirect(events:index,pk=post.pk)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

def create_message(request, event_id):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.created_on = timezone.now()
            post.save()
            #return redirect(events:detail,pk=post.pk)
    else:
        form = MessageForm()
    return render(request, 'events/create_message.html', {'form': form})

def create_question(request, event_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.created_on = timezone.now()
            post.save()
            #return redirect(events:index,pk=post.pk)
    else:
        form = QuestionForm()
    return render(request, 'events/create_question.html', {'form': form})

def create_choice(request, question_id):
    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.created_on = timezone.now()
            post.save()
            #return redirect(events:index,pk=post.pk)
    else:
        form = ChoiceForm()
    return render(request, 'events/create_choice.html', {'form': form})

class EditEventView(generic.UpdateView):

    model = Event
    template_name = 'events/create_event.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('events:index')

    def get_context_data(self, **kwargs):

        context = super(EditEventView, self).get_context_data(**kwargs)
        context['action'] = reverse('events:editevent', kwargs={'pk': self.get_object().id})

        return context

class EditQuestionView(generic.UpdateView):

    model = Question
    template_name = 'events/create_question.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('events:index')

    def get_context_data(self, **kwargs):

        context = super(EditQuestionView, self).get_context_data(**kwargs)
        context['action'] = reverse('events:editquestion', kwargs={'pk': self.get_object().id})

        return context

class EditChoiceView(generic.UpdateView):

    model = Choice
    template_name = 'events/create_choice.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('events:index')

    def get_context_data(self, **kwargs):

        context = super(EditChoiceView, self).get_context_data(**kwargs)
        context['action'] = reverse('events:editchoice', kwargs={'pk': self.get_object().id})

        return context

class EditMessageView(generic.UpdateView):

    model = Message
    template_name = 'events/create_message.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('events:index')

    def get_context_data(self, **kwargs):

        context = super(EditMessageView, self).get_context_data(**kwargs)
        context['action'] = reverse('events:editevent', kwargs={'pk': self.get_object().id})

        return context

class DeleteQuestionView(generic.DeleteView):

    model = Question
    success_url = reverse_lazy('events:index')

class DeleteChoiceView(generic.DeleteView):

    model = Choice
    success_url = reverse_lazy('events:index')

class DeleteMessageView(generic.DeleteView):

    model = Message
    success_url = reverse_lazy('events:index')

class DeleteEventView(generic.DeleteView):

    model = Event
    success_url = reverse_lazy('events:index')

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
