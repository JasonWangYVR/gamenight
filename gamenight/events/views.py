from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .models import Event, Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'latest_event_list'
    #overwrite for listview only
    def get_queryset(self):
        return Event.objects.order_by('-id')[:5]

def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    question = Question.objects.filter(on_event=event.pk)
    #choice = Choice.objects.filter(question=question.pk)
    context = {
        'event': event,
        'question_list' : question,
        #'choices' : choice,
            }
    return render(request, 'events/event_detail.html', context)
