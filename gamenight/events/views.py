import string
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.urls import reverse
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
from .models import Event, Question, Choice
#include forms
from .forms import EventForm, QuestionForm, ChoiceForm

def index(request):
    #what is this for? -JM
    #title = 'GameNight Event List'
    event = Event.objects.order_by('title')
    context = {
        'event': event,
        #likely not needed -JM
        #'choices' : choice,
            }
    return render(request, 'events/index.html', context)

#what is this? -JM
#def event_list(request):
#    event = Event.objects.filter.order_by('name')
#    return render(request, 'events/index.html', {'event': event})

def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    question = Question.objects.filter(on_event=event.pk)
    choice = Choice.objects.filter(question_id__in=question)

    context = {
        'event': event,
        'question' : question,
        'choice' : choice,
            }
    return render(request, 'events/event_detail.html', context)

def create_event(request):
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            #post.created_on = timezone.now()
            post.save()
            #return redirect(events:index,pk=post.pk)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


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

#class CreateQuestionView(generic.CreateView):
    #Need to figure out a way to return from creating a question to the related event detail view
    #at the moment this view only accepts one model, so we cannot return based on the event_id as the event model
    #isn't available
    #model = Question
    #template_name = 'events/create_question.html'
    #fields = '__all__'

    #def get_success_url(self):
    #    return reverse('events:index')

    #def get_context_data(self, **kwargs):

    #    context = super(CreateQuestionView, self).get_context_data(**kwargs)
    #    context['action'] = reverse('events:addquestion', kwargs={'pk': self.get_object().id})

    #    return context


#class CreateChoiceView(generic.CreateView):
    #Need to figure out a way to return from creating a question to the related event detail view
    #at the moment this view only accepts one model, so we cannot return based on the event_id as the event model
    #isn't available
#    model = Choice
#    template_name = 'events/create_choice.html'
#    fields = '__all__'

#    def get_success_url(self):
#        return reverse('events:index')

#    def get_context_data(self, **kwargs):

#        context = super(CreateChoiceView, self).get_context_data(**kwargs)
#        context['action'] = reverse('events:addchoice', kwargs={'pk': self.get_object().id})

#        return context
