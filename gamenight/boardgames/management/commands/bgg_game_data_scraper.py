from xml.dom import minidom
import urllib2
import json
from datetime import datetime
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from boardgames.models import BoardGame, Tag

class Command(BaseCommand):
    help = 'Pulls data from BGG on games in Tom Vasel\'s and rahdo\'s collections'
    def handle(self, *args, **options):
            with open('result.json') as id_file:
                id_dict = json.load(id_file)

            ids = id_dict.keys()

starttime = datetime.now()
for item in ids:
    url = 'https://www.boardgamegeek.com/xmlapi2/thing?id=' + item + '&stats=1'
    dom = minidom.parse(urllib2.urlopen(url))
    link = dom.getElementsByTagName('link')
    game = BoardGame(
            name = (dom.getElementsByTagName('name'))[0].attributes['value'].value,
            description = dom.getElementsByTagName('description').firstChild.nodeValue,
            pub_date = dom.getElementsByTagName('yearpublished')[0].attributes['value'].value,
            bgg_rating = dom.getElementsByTagName('average')[0].attributes['value'].value,
            bgg_weight = dom.getElementsByTagName('averageweight')[0].attributes['value'].value,
            min_players = dom.getElementsByTagName('minplayers')[0].attributes['value'].value,
            max_players = dom.getElementsByTagName('maxplayers')[0].attributes['value'].value,
            min_playtime = dom.getElementsByTagName('minplaytime')[0].attributes['value'].value,
            max_playtime = dom.getElementsByTagName('maxplaytime')[0].attributes['value'].value,
            img_link = dom.getElementsByTagName('image').firstChild.nodeValue,
            designed_by = [items.attributes['value'].value for items in link if items.attributes['type'].value == "boardgamecategory"]
            tags = [items.attributes['value'].value for items in link if items.attributes['type'].value == ("boardgamecategory" || "boardgamemechanic"]
    )
    game.save()
    print "Game: " + game.name +" saved!    Time elapsed = " + str(datetime.now()-starttime)
    sleep(2.5)
