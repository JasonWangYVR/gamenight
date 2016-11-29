from django import forms
from .models import Event

class EventForm(forms.ModelForm):

	class Meta:
		model = Event
		fields = ('title','organizer','event_date','created_on','last_edited_date','location',)