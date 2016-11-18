from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models
from django.template.defaultfilters import slugify

class BoardGame(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    #pub_date is when the game was originally published, not when added to our db
    pub_date = models.DateField('date published', null=True)
    #rating on bgg as of being pulled from bgg
    bgg_rating = models.FloatField(default=0.0)
    bgg_bayesrating = models.FloatField(default=0.0)
    bgg_weight = models.FloatField(default=0.0)
    min_players = models.IntegerField(default=1)
    max_players = models.IntegerField(default=2)
    best_player_count = models.IntegerField(null=True)
    min_playtime = models.IntegerField(default=2)
    max_playtime = models.IntegerField(default=5)
    designed_by = models.ManyToManyField('Designer')
    img_link = models.URLField()
    tags = models.ManyToManyField('Tag')
    favoriters = models.ForeignKey(User)
    slug = models.SlugField(allow_unicode=True, null=True)
    def save(self, *args, **kwargs):
        # Newly created object, so set slug
        self.slug = slugify(self.name)
        super(BoardGame, self).save(*args, **kwargs)

class Designer(models.Model):
    name = models.CharField(max_length=100)
    game = models.ManyToManyField(BoardGame)

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    games = models.ManyToManyField(BoardGame)
