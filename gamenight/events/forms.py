from django import forms
from .models import Event, Question, Choice

class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ('title','organizer','event_date','created_on','location',)

class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = ('question_text','pub_date','on_event')

class ChoiceForm(forms.ModelForm):

	class Meta:
		model = Choice
		fields = ('question','choice_text', 'votes')
