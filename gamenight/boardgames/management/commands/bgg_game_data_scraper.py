from xml.dom import minidom
import urllib2
import json
from datetime import datetime
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from boardgames.models import BoardGame, Tag, Designer

class Command(BaseCommand):
    help = 'Pulls data from BGG on games in Tom Vasel\'s and rahdo\'s collections'
    def handle(self, *args, **options):
            with open('result.json') as id_file:
                id_dict = json.load(id_file)
            ids = id_dict.keys()
            starttime = datetime.now()
            i = 0
            for item in ids:
                url = 'https://www.boardgamegeek.com/xmlapi2/thing?id=' + item + '&stats=1'
                dom = minidom.parse(urllib2.urlopen(url))
                n = dom.getElementsByTagName('name')[0].attributes['value'].value
                print "Parsing Game " + str(i) + ": " + n.encode("utf-8")
                g = BoardGame(
                        name = n,
                        description = dom.getElementsByTagName('description')[0].firstChild.nodeValue,
                        bgg_bayesrating = dom.getElementsByTagName('bayesaverage')[0].attributes['value'].value,
                        bgg_weight = dom.getElementsByTagName('averageweight')[0].attributes['value'].value,
                        min_players = dom.getElementsByTagName('minplayers')[0].attributes['value'].value,
                        max_players = dom.getElementsByTagName('maxplayers')[0].attributes['value'].value,
                        min_playtime = dom.getElementsByTagName('minplaytime')[0].attributes['value'].value,
                        max_playtime = dom.getElementsByTagName('maxplaytime')[0].attributes['value'].value,
                )
                g.save()

                img = dom.getElementsByTagName('image')
                if img != []:
                    g.img_link = img[0].firstChild.nodeValue

                year = dom.getElementsByTagName('yearpublished')[0].attributes['value'].value
                if int(year) > 0 :    #ensures the year will be of the correct format for datetime!
                    if len(year) < 4:
                        year = '0' + year
                    g.pub_date = datetime.strptime(year, '%Y')

                link = dom.getElementsByTagName('link')
                designers = [items.attributes['value'].value for items in link if items.attributes['type'].value == "boardgamedesigner"]
                for d in designers:
                    q = Designer.objects.filter(name = d)
                    if not q:
                        person = Designer(name = d)
                        person.save()
                    else:
                        person = q.first()

                    g.designed_by.add(person)
                    g.save()


                tags = [items.attributes['value'].value for items in link if items.attributes['type'].value == "boardgamecategory"  or items.attributes['type'].value == "boardgamemechanic"]
                for t in tags:
                    q = Tag.objects.filter(tag_name = t)
                    if not q:
                        tag = Tag(tag_name = t )
                        tag.save()

                    else:
                        tag = q.first()
                    g.tags.add(tag)
                    g.save()

                print "     Game " + str(i) + ": " + g.name.encode("utf-8") +" saved!    Time elapsed = " + str(datetime.now()-starttime)
                i += 1
                sleep(.5)
