from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, render
from django.views import generic
from django.urls import reverse
#included models
from .models import Event, Question, Choice
from django.contrib.auth.models import User,Group

# Create your views here.
#index taken from Django tutorials
class IndexView(generic.ListView):
    template_name = 'events/index.html'
    context_object_name = 'latest_event_list'
    #overwrite for listview only
    def get_queryset(self):
        return Event.objects.order_by('-id')[:5]
#view for individual events and related models

                                                                                #JASON: auth has been integrated
def detail(request, event_id):
    #grab single events obj
    event = get_object_or_404(Event, pk=event_id)
    if event.private_event == True:
        if request.user.is_authenticated():
            if user in event.group:
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
            else:                                                               #JASON: user is not in private event
                return redirect('events:private_event')
        else:                                                                   #JASON: user not logged in
            return redirect('authentication:login')
    else:                                                                       #JASON: event is public
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


class CreateEventView(generic.CreateView):

    model = Event
    template_name = 'events/create_event.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('events:index')

    def get_context_data(self, **kwargs):

        context = super(CreateEventView, self).get_context_data(**kwargs)
        context['action'] = reverse('events:create')

        return context

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

class CreateQuestionView(generic.CreateView):
    #Need to figure out a way to return from creating a question to the related event detail view
    #at the moment this view only accepts one model, so we cannot return based on the event_id as the event model
    #isn't available
    model = Question
    template_name = 'events/create_question.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('events:index')

    def get_context_data(self, **kwargs):

        context = super(CreateQuestionView, self).get_context_data(**kwargs)
        context['action'] = reverse('events:addquestion', kwargs={'pk': self.get_object().id})

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

class CreateChoiceView(generic.CreateView):
    #Need to figure out a way to return from creating a question to the related event detail view
    #at the moment this view only accepts one model, so we cannot return based on the event_id as the event model
    #isn't available
    model = Choice
    template_name = 'events/create_choice.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('events:index')

    def get_context_data(self, **kwargs):

        context = super(CreateChoiceView, self).get_context_data(**kwargs)
        context['action'] = reverse('events:addchoice', kwargs={'pk': self.get_object().id})

        return context
