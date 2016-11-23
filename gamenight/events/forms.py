from django import forms
from events.models import Event

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
        widget=forms.DateTimeInput()
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
