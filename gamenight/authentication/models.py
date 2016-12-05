from django.db import models
from django.contrib.auth.models import User
#from events.models import Event
#from boardgames.models import BoardGame

#JASON: This entire model needs to reworked, and it also needs to actually work.
#       TODO:   -Add ManyToMany for favorite boardgames
#               -Add ManyToMany for events that the user is attending.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addr_1 = models.CharField(max_length=30)
    addr_2 = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    prov = models.CharField(max_length=5)
    post_zip = models.CharField(max_length=10)
    attending_events = models.ManyToManyField('events.Event')
    favorite_games = models.ManyToManyField('boardgames.BoardGame')
    deleted = models.BooleanField()