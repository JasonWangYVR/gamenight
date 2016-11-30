from django import forms
from .models import Event, Question

class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ('title','organizer','event_date','created_on','location',)

class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = ('question_text','pub_date','on_event')
