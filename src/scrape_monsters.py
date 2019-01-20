# -*- coding: utf-8 -*-

# import libraries
import urllib2
import re
import utils
import scraper
from monster import Monster
from spellprofile import SpellProfile
from spelllikeprofile import SpellLikeProfile
from bs4 import BeautifulSoup

def scrape_page(url, monsters, spell_profiles, spell_like_profiles, source):
    if "phantomArmor.html" in y:
        return
    print('scraping ' + y + '...')
    print('====================')
    monsterpage = urllib2.urlopen(url)
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
                break

            print('\t' + name.encode('utf-8') + ' CR ' + cr.encode('utf-8'))
            scraper.scrape_monster(buffer, name, cr, monsters, spell_profiles, spell_like_profiles, source)
# urls
bestiary_urls = ['http://legacy.aonprd.com/bestiary/monsterIndex.html', 'http://legacy.aonprd.com/bestiary2/additionalMonsterIndex.html',
                 'http://legacy.aonprd.com/bestiary3/monsterIndex.html', 'http://legacy.aonprd.com/bestiary4/monsterIndex.html', 'http://legacy.aonprd.com/bestiary5/index.html']
bestiary_base_urls = ['http://legacy.aonprd.com/bestiary/', 'http://legacy.aonprd.com/bestiary2/',
                      'http://legacy.aonprd.com/bestiary3/', 'http://legacy.aonprd.com/bestiary4/', 'http://legacy.aonprd.com/bestiary5/']
monster_codex_url_base = 'http://legacy.aonprd.com/monsterCodex/'
monster_codex_urls = ['boggards.html', 'bugbears.html', 'drow.html', 'duergar.html', 'fireGiants.html', 'frostGiants.html', 'ghouls.html', 'gnolls.html', 'goblins.html', 'hobgoblins.html', 'kobolds.html',
                      'lizardfolk.html', 'ogres.html', 'orcs.html', 'ratfolk.html', 'sahuagin.html', 'serpentfolk.html', 'troglodytes.html', 'trolls.html', 'vampires.html']
npc_codex_url_base = 'http://legacy.aonprd.com/npcCodex/'
npc_codex_urls = ['core/barbarian.html', 'core/bard.html', 'core/cleric.html', 'core/druid.html', 'core/fighter.html', 'core/monk.html', 'core/paladin.html', 'core/ranger.html',
                  'core/rogue.html', 'core/sorcerer.html', 'core/wizard.html', 'prestige/arcaneArcher.html', 'prestige/arcaneTrickster.html', 'prestige/assassin.html',
                  'prestige/dragonDisciple.html', 'prestige/duelist.html', 'prestige/eldritchKnight.html', 'prestige/loremaster.html', 'prestige/mysticTheurge.html',
                  'prestige/pathfinderChronicler.html', 'prestige/shadowdancer.html', 'npc/adept.html', 'npc/aristocrat.html', 'npc/commoner.html', 'npc/expert.html', 'npc/warrior.html']

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
        scrape_page(bestiary_base_urls[i] + y, monsters, spell_profiles, spell_like_profiles, "Pathfinder RPG Bestiary " + str(i+1))

    # Dump Data to Json File
    filename = "../output/monsters/bestiary" + str(i+1) + ".json"
    utils.save_json(monsters, filename)

    filename = "../output/monsters/bestiary" + str(i+1) + "_spells.json"
    utils.save_json(spell_profiles, filename)

    filename = "../output/monsters/bestiary" + str(i+1) + "_spelllikeabilities.json"
    utils.save_json(spell_like_profiles, filename)

monsters = []
spell_profiles = []
spell_like_profiles = []
print("Scraping Monster Codex")
for y in monster_codex_urls:
    scrape_page(monster_codex_url_base + y, monsters, spell_profiles, spell_like_profiles, "Pathfinder RPG Monster Codex")

# Dump Data to Json File
filename = "../output/monsters/monsterCodex.json"
utils.save_json(monsters, filename)

filename = "../output/monsters/monsterCodex_spells.json"
utils.save_json(spell_profiles, filename)

filename = "../output/monsters/monsterCodex_spelllikeabilities.json"
utils.save_json(spell_like_profiles, filename)

monsters = []
spell_profiles = []
spell_like_profiles = []
print("Scraping NPC Codex")
for y in npc_codex_urls:
    scrape_page(npc_codex_url_base + y, monsters, spell_profiles, spell_like_profiles, "Pathfinder RPG NPC Codex")

# Dump Data to Json File
filename = "../output/monsters/npcCodex.json"
utils.save_json(monsters, filename)

filename = "../output/monsters/npcCodex_spells.json"
utils.save_json(spell_profiles, filename)

filename = "../output/monsters/npcCodex_spelllikeabilities.json"
utils.save_json(spell_like_profiles, filename)
