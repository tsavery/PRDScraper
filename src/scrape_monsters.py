# -*- coding: utf-8 -*-

# import libraries
import urllib2
import jsonpickle
import re
import json
import os
import errno
from monster import Monster
from spellprofile import SpellProfile
from spelllikeprofile import SpellLikeProfile
from bs4 import BeautifulSoup

def removeTrailingAndLeadingSpaces(value):
    while value.endswith(' '):
        value = value[:-1]
    while value.startswith(' '):
        value = value[1:]
    return value

def obj_dict(obj):
    return del_empty(obj.__dict__.copy())

def del_empty(d):
    for key, value in list(d.items()):
        if (not isinstance(value, int) and len(value) is 0) or (isinstance(value, int) and value == 0):
            del d[key]
        elif isinstance(value, dict):
            del_empty(value)
    return d

# urls
bestiary_urls = ['http://legacy.aonprd.com/bestiary/monsterIndex.html', 'http://legacy.aonprd.com/bestiary2/additionalMonsterIndex.html',
                 'http://legacy.aonprd.com/bestiary3/monsterIndex.html', 'http://legacy.aonprd.com/bestiary4/monsterIndex.html', 'http://legacy.aonprd.com/bestiary5/index.html']
bestiary_base_urls = ['http://legacy.aonprd.com/bestiary/', 'http://legacy.aonprd.com/bestiary2/',
                 'http://legacy.aonprd.com/bestiary3/', 'http://legacy.aonprd.com/bestiary4/', 'http://legacy.aonprd.com/bestiary5/']


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
            if any(c in x.get_text() for c in ("Starting Statistics", "Advancement", "Artifact")):
                continue
            name = ""
            cr = 0
            if x.b and x.b.find('span', class_='stat-block-cr') or x.find('span', class_='stat-block-cr'):
                if(x.b):
                    pair = x.b.get_text().split('CR')
                else:
                    pair = x.get_text().split('CR')
                name = removeTrailingAndLeadingSpaces(pair[0])

                cr = removeTrailingAndLeadingSpaces(pair[1])
                print('\t' + name + ' CR ' + cr)
                currentElement = x

                # get all the content for the stat block as plain text
                buffer = ""
                while currentElement.get('class'):
                    currentElement = currentElement.find_next('p')
                    buffer += currentElement.get_text() + "\n"
                # parse the statblock into the object using regexes
                monster = Monster(name, cr)

                # Initiative Bonus
                regex = re.compile('(?<=Init ).\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    if result[0] == '+':
                        monster.init = int(result[1:])
                    else:
                        monster.init = (int(result[1:]) * -1)

                # Senses
                regex = re.compile('(?<=Senses ).+(?=;)')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.senses = result

                # Perception Bonus
                regex = re.compile('(?<=Perception ).\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    if result[0] == '+':
                        monster.perception = int(result[1:])
                    else:
                        monster.perception = (int(result[1:]) * -1)

                # Auras
                regex = re.compile('(?<=Aura ).+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.aura = result

                # AC and Bonuses
                regex = re.compile('(?<=AC )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.ac = int(result)
                regex = re.compile('(?<=touch )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.ac_touch = int(result)
                regex = re.compile('(?<=touch )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.ac_flat_footed = int(result)

                regex = re.compile('((?<=flat-footed \d\d \()|(?<=flat-footed \d \()).+(?=\))')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.ac_bonuses = result

                # Shield Bonus
                regex = re.compile('(?<=\+)\d+(?= shield)')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.shield_ac_bonus = int(result)

                # Natural Armor Bonus
                regex = re.compile('(?<=\+)\d+(?= natural)')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.natural_ac_bonus = int(result)

                # Dodge Armor Bonus
                regex = re.compile('(?<=\+)\d+(?= dodge)')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.dodge_ac_bonus = int(result)

                # Deflection Armor Bonus
                regex = re.compile('(?<=\+)\d+(?= deflection)')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.deflection_ac_bonus = int(result)

                # HP
                regex = re.compile('(?<=hp )[0-9\(\)d\+– ]+(?=[;\n])')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.hp = result

                # Health Rules
                regex = re.compile('(?<=\d\); ).+(?=\nFort)')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.health_rules = result

                # Fortitude Save
                regex = re.compile('(?<=Fort ).\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    if result[0] == '+':
                        monster.fortitude = int(result[1:])
                    else:
                        monster.fortitude = (int(result[1:]) * -1)

                # Reflex Save
                regex = re.compile('(?<=Ref ).\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    if result[0] == '+':
                        monster.reflex = int(result[1:])
                    else:
                        monster.reflex = (int(result[1:]) * -1)

                # Will Save
                regex = re.compile('(?<=Will ).\d+', re.UNICODE)
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    if result[0] == '+':
                        monster.will = int(result[1:])
                    else:
                        monster.will = (int(result[1:]) * -1)

                # Saving Throw Modifiers
                regex = re.compile('((?<=Will \+\d; )|(?<=Will \+\d\d; )).+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.saving_throw_modifiers = result

                # Spell Resistence
                regex = re.compile('(?<=SR )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.spell_resist = int(result)

                # Damage Resistences
                regex = re.compile('(?<=DR )[\d\/, \w]+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.damage_resists = result

                # Defenseive Abilities
                regex = re.compile('(?<=Defensive Abilities )[\d \w\+\(\)–,]+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.defensive_abilities = result

                # Immunities
                regex = re.compile('(?<=Immune )[\d \w\+\(\)–,]+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.immunities = result

                # Weaknesses
                regex = re.compile('(?<=Weaknesses )[\d \w\+\(\)–,]+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.immunities = result

                # Resistences
                regex = re.compile('(?<=Resist )[\d \w\+\(\)–,]+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.resistences = result

                # Speed Profile
                regex = re.compile('(?<=Speed ).+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.speed_profile = result

                # Melee Profile
                regex = re.compile('(?<=Melee ).+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.melee_profile = result

                # Ranged Profile
                regex = re.compile('(?<=Ranged ).+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.ranged_profile = result

                # Special Attacks
                regex = re.compile('(?<=Special Attacks ).+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.special_attacks = result

                # Space
                regex = re.compile('(?<=Space )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.space = int(result)

                # Reach
                regex = re.compile('(?<=Reach )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.space = int(result)

                # Offensive Abilities
                regex = re.compile('(?<=Offensive Abilities )[\d \w\+\(\)–,]+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.offensive_abilities = result

                # Strength
                regex = re.compile('(?<=Str )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.strength = int(result)

                # Dexterity
                regex = re.compile('(?<=Dex )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.dexterity = int(result)

                # Constitution
                regex = re.compile('(?<=Con )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.constitution = int(result)

                # Intelligence
                regex = re.compile('(?<=Int )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.intelligence = int(result)

                # Wisdom
                regex = re.compile('(?<=Wis )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.wisdom = int(result)

                # Charisma
                regex = re.compile('(?<=Cha )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.charisma = int(result)

                # Base Attack Bonus
                regex = re.compile('(?<=Base Atk \+)\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.base_attack_bonus = int(result)

                # Combat Maneuver Bonus
                regex = re.compile('(?<=CMB ).\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    if result[0] == '+':
                        monster.combat_maneuver_bonus = int(result[1:])
                    else:
                        monster.combat_maneuver_bonus = (int(result[1:]) * -1)

                # Combat Maneuver Defense
                regex = re.compile('(?<=CMD )\d+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.combat_maneuver_defense = int(result)

                # Feats
                regex = re.compile('(?<=Feats ).+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.feats = result

                # Skills
                regex = re.compile('(?<=Skills )[A-Za-z \(\)\+–—,\d]+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.skills = result

                # Racial Skill Modifiers
                regex = re.compile('(?<=Racial Modifiers )[A-Za-z \(\)\+–,\d]+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.racial_skill_modifiers = result

                # Languages
                regex = re.compile('(?<=Languages )[A-Za-z\d,\.\' ]+')
                match = regex.search(buffer)
                if match:
                    result = re.split(', (?![^(]*\))', match.group())
                    monster.languages = result

                # Language Special Rules
                regex = re.compile('(?<=Languages ).+')
                match = regex.search(buffer)
                if match:
                    val = match.group().split("; ")
                    if len(val) > 1:
                        result = re.split(', (?![^(]*\))', val[1])
                        monster.language_special_rules = result

                # Special Qualities
                regex = re.compile('(?<=SQ ).+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.special_qualities = result

                # Enviroment
                regex = re.compile('(?<=Environment ).+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.environment = result

                # Organization
                regex = re.compile('(?<=Organization ).+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.organization = result

                # Treasure
                regex = re.compile('(?<=Treasure ).+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.treasure = result

                # Typeline
                regex = re.compile('[LEGCN]{1,2} (Fine|Diminutive|Tiny|Small|Medium|Large|Huge|Gargantuan|Colossal).+')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    monster.type = result

                # Classline
                regex = re.compile('(?<=\n)[A-Z][a-z]+ ([a-z/\(\)\d]+ )+\d{1,2}(?=\n)')
                match = regex.search(buffer)
                if match:
                    result = match.group()
                    if 'speed' not in result and 'Resist' not in result:
                        monster.classline = result

                #Encode the buffer for spellcasting checks
                buffer = buffer.encode('utf-8')

                # Psychic Magic
                regex = re.compile('(?<=Psychic Magic \(CL )\d+')
                match = regex.search(buffer)

                if match:
                    # Psychic Magic Caster Level
                    result = match.group()
                    monster.psychic_magic_caster_level = int(result)

                    # Psyhcic Concentration
                    spellregex = re.compile('((?<=Psychic Magic \(CL \d\w\w; concentration \+)|(?<=Psychic Magic \(CL \d\d\w\w; concentration \+))\d+')
                    spellmatch = spellregex.search(buffer)

                    if spellmatch:
                        result = spellmatch.group()
                        monster.psychic_magic_concentration = int(result)

                    # Psychic Energy Pool and Abilities
                    spellregex = re.compile('(?:\d\d PE—)[\d\w ;,\(\)%\.\'\/]+')
                    spellmatch = spellregex.search(buffer)

                    if spellmatch:
                        result = spellmatch.group()
                        val = result.split(' PE—')
                        monster.psychic_energy_pool = int(val[0])
                        monster.psychic_magic_abilities = re.split(', (?![^(]*\))', val[1])

                # Check for Spellcasting
                regex = re.compile('((?<=Spells Known \(CL )|(?<=Spells Prepared \(CL ))\d+')
                match = regex.search(buffer)

                if match:
                    monster.spellcaster = True
                    spell_profile = SpellProfile(name)
                    result = match.group()
                    # Caster Level
                    spell_profile.caster_level = int(result)

                    # Concentration Bonus
                    spellregex = re.compile('((?<=Prepared \(CL \d\w\w; concentration \+)|(?<=Prepared \(CL \d\d\w\w; concentration \+)|(?<=Known \(CL \d\w\w; concentration \+)|(?<=Known \(CL \d\d\w\w; concentration \+))\d+')
                    spellmatch = spellregex.search(buffer)
                    if spellmatch:
                        result = spellmatch.group()
                        spell_profile.concentration = int(result)

                    # Spells
                    spellregex = re.compile('[A-Z][a-z]+(?= Spells Known| Spells Prepared| Extracts Prepared)')
                    spellmatch = spellregex.search(buffer)
                    if(spellmatch):
                        result = spellmatch.group()
                        spell_profile.type = result
                    spellregex = re.compile('((?:\d[strdthn]{2} \(\d{1,2}\/day\)|0 \(at will\)|\d[strdthn]{2}|0|\d[strdthn]{2} \(\d+\))(?:—[\d\w ;,\(\)%\.\'\/]+\n))+', re.MULTILINE)
                    spellmatch = spellregex.search(buffer)
                    if spellmatch:
                        lines = spellmatch.group().decode('utf-8').split('\n')
                        for line in lines:
                            if line != '':
                                val = line.split('—'.decode('utf-8'))
                                spell_profile.spells[val[0]] = re.split(', (?![^(]*\))', val[1])
                        # Domains, Bloodline, Opposition Schools, Mystery
                        choiceregex = re.compile('(?<=Opposition Schools )[A-Za-z, ]+')
                        choicematch = choiceregex.search(buffer)
                        if choicematch:
                            result = re.split(', (?![^(]*\))', choicematch.group())
                            spell_profile.opposition_schools = result

                        choiceregex = re.compile('((?<=Domains )|(?<=Domain ))[A-Za-z, ]+')
                        choicematch = choiceregex.search(buffer)
                        if choicematch:
                            result = re.split(', (?![^(]*\))', choicematch.group())
                            spell_profile.domains = result

                        choiceregex = re.compile('(?<=Bloodline )[a-z\(\) ]+')
                        choicematch = choiceregex.search(buffer)
                        if choicematch:
                            result = choicematch.group()
                            spell_profile.bloodline = result

                        choiceregex = re.compile('(?<=Mystery )[a-z\(\) ]+')
                        choicematch = choiceregex.search(buffer)
                        if choicematch:
                            result = choicematch.group()
                            spell_profile.mystery = result

                        spell_profiles.append(spell_profile)

                # Check for Spell-Like Abilities
                regex = re.compile('(?<=Spell-Like Abilities \(CL )\d+')
                match = regex.search(buffer)
                if match:
                    monster.spell_like_abilities = True
                    spell_like_profile = SpellLikeProfile(name)
                    # Spell-Like Ability Caster Level
                    result = match.group()
                    spell_like_profile.spell_like_caster_level = int(result)

                    spellregex = re.compile('[A-Z][a-z]+(?= Spell-Like)')
                    spellmatch = spellregex.search(buffer)
                    if(spellmatch):
                        result = spellmatch.group()
                        SpellLikeProfile.type = result

                    # Concentration Bonus
                    spellregex = re.compile('((?<=Spell-Like Abilities \(CL \d\w\w; concentration \+)|(?<=Spell-Like Abilities \(CL \d\d\w\w; concentration \+))\d+')
                    spellmatch = spellregex.search(buffer)
                    if spellmatch:
                        result = spellmatch.group()
                        spell_like_profile.spell_like_concentration = int(result)

                    # Spell-Like Abiltiies
                    regex = re.compile('((?:(?:Constant|\d+\/day|At will|\d+\/week|\d+\/year)—[\d\w \/;,\(\)%\.\']+\n))+')
                    spellmatch = regex.search(buffer)
                    if spellmatch:
                        lines = spellmatch.group().decode('utf-8').split('\n')
                        for line in lines:
                            if line != '':
                                val = line.split('—'.decode('utf-8'))
                                spell_like_profile.spell_like_abilities[val[0]] = re.split(', (?![^(]*\))', val[1])

                    spell_like_profiles.append(spell_like_profile)

                # Add Source
                monster.source = "Pathfinder RPG Bestiary " + str(i+1)
                monsters.append(monster)

    # Dump Data to Json File
    jsonstr = json.dumps(monsters, default=obj_dict, indent=4)
    filename = "..\\output\\monsters\\bestiary" + str(i+1) + ".json"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    f = open(filename, "w")
    f.write(jsonstr)
    f.close()
    jsonstr = json.dumps(spell_profiles, default=obj_dict, indent=4)
    filename = "..\\output\\monsters\\bestiary" + str(i+1) + "_spells.json"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    f = open(filename, "w")
    f.write(jsonstr)
    f.close()
    jsonstr = json.dumps(spell_like_profiles, default=obj_dict, indent=4)
    filename = "..\\output\\monsters\\bestiary" + str(i+1) + "_spelllikeabilities.json"
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    f = open(filename, "w")
    f.write(jsonstr)
    f.close()
