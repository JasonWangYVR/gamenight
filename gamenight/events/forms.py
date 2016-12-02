from django import forms
from .models import Event, Question, Choice, Message

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

class MessageForm(forms.ModelForm):

	class Meta:
		model = Message
		fields = ('text','posted_by','on_event','pub_date')