# -*- coding: utf-8 -*-

# import libraries
import urllib2
import re
import json
import utils
import scraper
from monster import Monster
from spellprofile import SpellProfile
from spelllikeprofile import SpellLikeProfile
from bs4 import BeautifulSoup

# urls
bestiary_urls = ['http://legacy.aonprd.com/bestiary/monsterIndex.html', 'http://legacy.aonprd.com/bestiary2/additionalMonsterIndex.html',
                 'http://legacy.aonprd.com/bestiary3/monsterIndex.html', 'http://legacy.aonprd.com/bestiary4/monsterIndex.html', 'http://legacy.aonprd.com/bestiary5/index.html']
bestiary_base_urls = ['http://legacy.aonprd.com/bestiary/', 'http://legacy.aonprd.com/bestiary2/',
                 'http://legacy.aonprd.com/bestiary3/', 'http://legacy.aonprd.com/bestiary4/', 'http://legacy.aonprd.com/bestiary5/']
monster_codex_url_base = 'http://legacy.aonprd.com/monsterCodex/'
monster_codex_urls = ['boggards.html', 'bugbears.html', 'drow.html', 'duergar.html', 'fireGiants.html', 'frostGiants.html', 'ghouls.html', 'gnolls.html', 'goblins.html', 'hobgoblins.html', 'kobolds.html',
                    'lizardfolk.html', 'ogres.html', 'orcs.html', 'ratfolk.html', 'sahuagin.html', 'serpentfolk.html', 'troglodytes.html', 'trolls.html', 'vampires.html']


for i in range(0,5):
    print('Scraping Beastiary ' + str(i+1))
    print('====================')
    page = urllib2.urlopen(bestiary_urls[i])
    soup = BeautifulSoup(page, 'html.parser')

    body = soup.find('div', class_='body')

    # remove tags from hyperlinks
    links = []
    for a in body('a'):
        leftsideonly = a.get('href').split('#')
        if "../openGameLicense.html" not in leftsideonly[0]:
            links.append(leftsideonly[0])

    # remove duplicates
    links = list(set(links))
    links.sort()
    links.pop(0)
    monsters = []
    spell_profiles = []
    spell_like_profiles = []
    for y in links:
        if "phantomArmor.html" in y:
            continue
        print('scraping ' + y + '...')
        print('====================')
        monsterpage = urllib2.urlopen(bestiary_base_urls[i] + y)
        monstersoup = BeautifulSoup(monsterpage, 'html.parser')

        for x in monstersoup.find_all('p', class_='stat-block-title'):
            if "CR" not in x.get_text() or "Trap" in x.get_text():
                continue
            name = ""
            cr = 0
            if x.b and x.b.find('span', class_='stat-block-cr') or x.find('span', class_='stat-block-cr'):
                if(x.b):
                    pair = x.b.get_text().split('CR')
                else:
                    pair = x.get_text().split('CR')
                name = utils.remove_trailing_and_leading_spaces(pair[0])

                cr = utils.remove_trailing_and_leading_spaces(pair[1])

                currentElement = x

                # get all the content for the stat block as plain text
                buffer = ""
                lines = 0
                while currentElement.get('class'):
                    if 'stat-block-title' in currentElement.get('class') and lines > 0:
                        break
                    currentElement = currentElement.find_next('p')
                    buffer += currentElement.get_text() + "\n"
                    lines += 1
                if lines < 5:
                    continue

                print('\t' + name.encode('utf-8') + ' CR ' + cr.encode('utf-8'))
                scraper.scrape_monster(buffer, name, cr, monsters, spell_profiles, spell_like_profiles, "Pathfinder RPG Bestiary " + str(i+1))

    # Dump Data to Json File
    jsonstr = json.dumps(monsters, default=utils.obj_dict, sort_keys=False, indent=4)
    filename = "..\\output\\monsters\\bestiary" + str(i+1) + ".json"
    utils.save_json(jsonstr, filename)

    jsonstr = json.dumps(spell_profiles, default=utils.obj_dict, indent=4)
    filename = "..\\output\\monsters\\bestiary" + str(i+1) + "_spells.json"
    utils.save_json(jsonstr, filename)

    jsonstr = json.dumps(spell_like_profiles, default=utils.obj_dict, indent=4)
    filename = "..\\output\\monsters\\bestiary" + str(i+1) + "_spelllikeabilities.json"
    utils.save_json(jsonstr, filename)

monsters = []
spell_profiles = []
spell_like_profiles = []
print("Scraping Monster Codex")
for y in monster_codex_urls:
    print('scraping ' + y + '...')
    print('====================')
    monsterpage = urllib2.urlopen(monster_codex_url_base + y)
    monstersoup = BeautifulSoup(monsterpage, 'html.parser')

    for x in monstersoup.find_all('p', class_='stat-block-title'):
        if "CR" not in x.get_text() or "Trap" in x.get_text():
            continue
        name = ""
        cr = 0
        if x.b and x.b.find('span', class_='stat-block-cr') or x.find('span', class_='stat-block-cr'):
            if(x.b):
                pair = x.b.get_text().split('CR')
            else:
                pair = x.get_text().split('CR')
            name = utils.remove_trailing_and_leading_spaces(pair[0])

            cr = utils.remove_trailing_and_leading_spaces(pair[1])

            currentElement = x

            # get all the content for the stat block as plain text
            buffer = ""
            lines = 0
            while currentElement.get('class'):
                if 'stat-block-title' in currentElement.get('class') and lines > 0:
                    break
                currentElement = currentElement.find_next('p')
                buffer += currentElement.get_text() + "\n"
                lines += 1
            if lines < 5:
                continue
            print('\t' + name.encode('utf-8') + ' CR ' + cr.encode('utf-8'))
            scraper.scrape_monster(buffer, name, cr, monsters, spell_profiles, spell_like_profiles, "Pathfinder RPG Monster Codex")

# Dump Data to Json File
jsonstr = json.dumps(monsters, default=utils.obj_dict, indent=4)
filename = "..\\output\\monsters\\monsterCodex.json"
utils.save_json(jsonstr, filename)

jsonstr = json.dumps(spell_profiles, default=utils.obj_dict, indent=4)
filename = "..\\output\\monsters\\monsterCodex_spells.json"
utils.save_json(jsonstr, filename)

jsonstr = json.dumps(spell_like_profiles, default=utils.obj_dict, indent=4)
filename = "..\\output\\monsters\\monsterCodex_spelllikeabilities.json"
utils.save_json(jsonstr, filename)
