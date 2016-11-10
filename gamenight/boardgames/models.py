from __future__ import unicode_literals

from django.db import models

class BoardGame(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    #pub_date is when the game was originally published, not added to our db
    pub_date = models.DateTimeField('date published')
    #rating on bgg as of being pulled from bgg
    bgg_rating = models.IntegerField(default=0)
    bgg_weight = models.IntegerField()
    min_players = models.IntegerField(default=1)
    max_players = models.IntegerField()
    best_player_count = models.IntegerField()
    min_playtime = models.IntegerField()
    max_playtime = models.IntegerField()
    designed_by = models.ManyToManyField('Designer')
    img_link = models.URLField()
    tags = models.ManyToManyField('Tag')

class Designer(models.Model):
    name = models.CharField(max_length=100)
    game = models.ManyToManyField(BoardGame)

class Tag(models.Model):
    tag_name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    games = models.ManyToManyField(BoardGame)
