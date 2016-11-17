from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render
from django.views import generic
from django.urls import reverse
#included models
from .models import Event, Question, Choice

# Create your views here.
#index taken from Django tutorials
class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'latest_event_list'
    #overwrite for listview only
    def get_queryset(self):
        return Event.objects.order_by('-id')[:5]
#view for individual events and related models
def detail(request, event_id):
    #grab single events obj
    event = get_object_or_404(Event, pk=event_id)
    #grab collection of questions that are related to event obj
    # through primary key foreign key relationship
    question = Question.objects.filter(on_event=event.pk)

    #not impletmented yet
    #choice = Choice.objects.filter(question=question.pk)

    #store objects (or collections) in context (dictionary)
    context = {
        'event': event,
        'question_list' : question,
        #'choices' : choice,
            }
    #return request, template, and dictionary to views (template)
    return render(request, 'events/event_detail.html', context)
