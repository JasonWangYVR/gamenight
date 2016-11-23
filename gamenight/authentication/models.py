from django.db import models
from django.contrib.auth.models import User

#JASON: This entire model needs to reworked, and it also needs to actually work.
#       TODO:   -Add ManyToMany for favorite boardgames
#               -Add ManyToMany for events that the user is attending.
class GNUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addr_1 = models.CharField(max_length=30)
    addr_2 = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    prov = models.CharField(max_length=5)
    post_zip = models.CharField(max_length=10)

    class Meta:
        abstract = True
