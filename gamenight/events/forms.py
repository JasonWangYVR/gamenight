from django import forms
from .models import Event, Question, Choice, Message
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})

#OLD EVENT FORM
#class EventForm(forms.ModelForm):

	#class Meta:
		#model = Event
		#fields = ('title','organizer','event_date','created_on','location',)

class EventForm(forms.ModelForm):                                               #JASON: My attempt at creating a nice form for event creation.
    title = forms.CharField(
        label = 'Event Title',
        min_length = 6,
        required = True,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '6-30 Characters',
            }
        )
    )

    location = forms.CharField(
        label = 'Location',
        required = True,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '1-30 Characters',
            }
        )
    )
	
    event_date = forms.DateField(widget=DateInput())
    #widget=forms.DateField(widget=DateInput('%d/%m/%Y'))

    private_event = forms.BooleanField(
        label = 'Private Event',
        required = False,
        widget=forms.CheckboxInput()
    )
                                                                                #JASON: TODO: Add multiple attendees.
    class Meta:
        model = Event
        fields = ('title', 'location', 'event_date', 'private_event')

class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = ('question_text','pub_date')

class ChoiceForm(forms.ModelForm):

	class Meta:
		model = Choice
		fields = ('choice_text', 'votes')

class MessageForm(forms.ModelForm):

	class Meta:
		model = Message
		fields = ('text','pub_date')
		
class SearchEventsForm(forms.Form):
    qq = forms.CharField(
        required = True,
        max_length = 50,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': 'Public Event',
            }
        )
    )

class AddAttendeeForm(forms.Form):
    username = forms.CharField(
        label = 'Username',
        min_length = 6,
        required = True,
        widget=forms.TextInput(
            attrs = {
                'class': 'form-control',
                'placeholder': '6-30 Characters',
            }
        )
    )
