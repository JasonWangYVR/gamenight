from django import forms
from .models import Event, Question, Choice, Message

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
    event_date = forms.DateTimeField(
        label = 'Date/Time',
        required = True,
        widget=forms.DateTimeInput(
			attrs = {
				'class': 'form-control',
				'placeholder': 'YYYY-MM-DD',
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
    private_event = forms.BooleanField(
        label = 'Private Event',
        required = False,
        widget=forms.CheckboxInput()
    )
                                                                                #JASON: TODO: Add multiple attendees.
    class Meta:
        model = Event
        fields = ('title', 'event_date', 'location', 'private_event')

class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = ('question_text','on_event','pub_date')

class ChoiceForm(forms.ModelForm):

	class Meta:
		model = Choice
		fields = ('question','choice_text', 'votes')

class MessageForm(forms.ModelForm):

	class Meta:
		model = Message
		fields = ('text','posted_by','on_event','pub_date')
