from django.db import models
from django.contrib.auth.models import User
from events.models import Event
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
    attending_events = models.ManyToManyField(Event)
    deleted = models.BooleanField()

    def create_profile(self, user, addr_1, addr_2, city, prov, post_zip):
        self.user = user
        self.addr_1 = addr_1
        self.addr_2 = addr_2
        self.city = city
        self.prov = prov
        self.post_zip = post_zip
        self.deleted = False
        self.save()
        return self

    #TODO: def delete_profile()
