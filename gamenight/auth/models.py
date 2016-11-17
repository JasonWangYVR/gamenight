from django.db import models
from django.contrib.auth.models import User

class GNUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    addr_1 = models.CharField(max_length=30)
    addr_2 = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    prov = models.CharField(max_length=5)
    post_zip = models.CharField(max_length=10)

    class Meta:
        abstract = True
