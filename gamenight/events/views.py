from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render
from django.views import generic
from django.urls import reverse

from .models import Event, Question
#from polls.models import Question, Choice


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'latest_event_list'
    #overwrite for listview only
    def get_queryset(self):
        return Event.objects.order_by('-id')[:5]


class DetailView(generic.DetailView):
    model = Event
    #detailview uses Event model no rename required
    template_name = 'events/event_detail.html'
    def get_queryset(self):
        qs = super(DetailView, self).get_queryset()
        return qs.all()
