from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User,Group
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=140)
    #group = models.ForeignKey(Group, on_delete=models.CASCADE)                 #JASON: We don't need groups.
    #uncertain if this is the correct declaration for Group
    organizer = models.ForeignKey(User, on_delete= models.CASCADE)
    #should we cascade user deletion and event deletion?

    event_date = models.DateTimeField()                                         #JASON: Not sure if we should use DateTimeField,
    created_on = models.DateTimeField()                                         #       but that's what's happening for now I guess.
    last_edited_date = models.DateTimeField()

    location = models.CharField(max_length=100)
    private_event = models.BooleanField()                                       #JASON: for private/public events
    attendees = models.ManyToManyField(User)                                    #JASON: who is going?

    def __str__(self):
        return self.title

    def new_event(self, title, organizer, event_date, location,
        private_event):
        self.title = title
        self.organizer = organizer
        #self.event_date = event_date
        self.location = location
        self.private_event = private_event
        # self.created_on =                                                     #JASON: Not sure how we're doing date and time yet.
        # self.last_edited_date =
		attendees.add(organizer)
    

class Message(models.Model):
    text = models.CharField(max_length=500)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    on_event = models.ForeignKey(Event, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    message_number = models.IntegerField(default=0)
    #message_number will help us maintain order of messages in a given Event

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    on_event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name='the related event')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
