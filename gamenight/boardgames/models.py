from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

class BoardGame(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=20000)
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
    slug = models.SlugField(max_length=200, allow_unicode=True, null=True)

    def save(self, *args, **kwargs):
        # Newly created object, so set slug
        self.slug = slugify(self.name)
        super(BoardGame, self).save(*args, **kwargs)
    def __str__(self):
        return self.name

class Designer(models.Model):
    name = models.CharField(max_length=1000)
    game = models.ManyToManyField(BoardGame)
    def __str__(self):
        return self.name

class Tag(models.Model):
    tag_name = models.CharField(max_length=5000)
    description = models.CharField(max_length=10000)
    games = models.ManyToManyField(BoardGame)
    def __str__(self):
        return self.tag_name
