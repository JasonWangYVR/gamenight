from xml.dom import minidom
import urllib2
import json

tom_vasel = 'https://www.boardgamegeek.com/xmlapi2/collection?username=TomVasel&excludesubtype=boardgameexpansion'
rahdo = 'https://www.boardgamegeek.com/xmlapi2/collection?username=rahdo&excludesubtype=boardgameexpansion'
katanan = 'https://www.boardgamegeek.com/xmlapi2/collection?username=katanan&excludesubtype=boardgameexpansion'
urls = [tom_vasel, rahdo]
game_ids = dict()
i = 0

for url in urls:
    dom = minidom.parse(urllib2.urlopen(url)) #parse the data into something we can manipulate
    games = dom.getElementsByTagName('item')

    for game in games:
        game_ids[int(game.getAttribute('objectid'))] = i
        i += 1

print len(game_ids)
with open('result.json','w') as fp:
    json.dump(game_ids, fp)
