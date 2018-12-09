# -*- coding: utf-8 -*-

# import libraries
import re
import utils
from monster import Monster
from spellprofile import SpellProfile
from spelllikeprofile import SpellLikeProfile

def split_csv(str):
    return re.split(', (?![^(]*\))', str)

def scrape_monster(buffer, name, cr, monsters, spell_profiles, spell_like_profiles, source):
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
        result = split_csv(match.group())
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
        result = split_csv(match.group())
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
        result = split_csv(match.group())
        monster.ac_bonuses = result

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
        result = split_csv(match.group())
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
        result = split_csv(match.group())
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
        result = split_csv(match.group())
        monster.defensive_abilities = result

    # Immunities
    regex = re.compile('(?<=Immune )[\d \w\+\(\)–,]+')
    match = regex.search(buffer)
    if match:
        result = split_csv(match.group())
        monster.immunities = result

    # Weaknesses
    regex = re.compile('(?<=Weaknesses )[\d \w\+\(\)–,]+')
    match = regex.search(buffer)
    if match:
        result = split_csv(match.group())
        monster.immunities = result

    # Resistences
    regex = re.compile('(?<=Resist )[\d \w\+\(\)–,]+')
    match = regex.search(buffer)
    if match:
        result = split_csv(match.group())
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
        result = split_csv(match.group())
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
        result = split_csv(match.group())
        monster.feats = result

    # Skills
    regex = re.compile('(?<=Skills )[A-Za-z \(\)\+–—,\d]+')
    match = regex.search(buffer)
    if match:
        result = split_csv(match.group())
        monster.skills = result

    # Racial Skill Modifiers
    regex = re.compile('(?<=Racial Modifiers )[A-Za-z \(\)\+–,\d]+')
    match = regex.search(buffer)
    if match:
        result = split_csv(match.group())
        monster.racial_skill_modifiers = result

    # Languages
    regex = re.compile('(?<=Languages )[A-Za-z\d,\.\' ]+')
    match = regex.search(buffer)
    if match:
        result = split_csv(match.group())
        monster.languages = result

    # Language Special Rules
    regex = re.compile('(?<=Languages ).+')
    match = regex.search(buffer)
    if match:
        val = match.group().split("; ")
        if len(val) > 1:
            result = split_csv(match.group())
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
            monster.psychic_magic_abilities = split_csv(val[1])

    # Check for Spellcasting
    regex = re.compile('.+\n(?:(?:\d[strdthn]{2} \(\d{1,2}\/day\)|0 \(at will\)|\d[strdthn]{2}|0|\d[strdthn]{2} \(\d+\))(?:—[\d\w -+;,\(\)%\.\'\/]+\n))+(?:(?:D |Bloodline [a-z]|Opposition Schools [a-z]|Patron [a-z]|Mystery [a-z]| Domain [a-z]| Domains [a-z])[\*\d\w\(\) ;,]+\n){0,1}')
    matches = regex.findall(buffer)
    for s in matches:
        monster.spellcaster = True
        spell_profile = SpellProfile(name)
        # Caster Level
        spellregex = re.compile('((?<=Spells Known \(CL )|(?<=Spells Prepared \(CL )|(?<=Extracts Prepared \(CL ))\d+')
        spellmatch = spellregex.search(s)
        if spellmatch:
            result = spellmatch.group()
            spell_profile.caster_level = int(result)
        # Concentration Bonus
        spellregex = re.compile('((?<=Prepared \(CL \d\w\w; concentration \+)|(?<=Prepared \(CL \d\d\w\w; concentration \+)|(?<=Known \(CL \d\w\w; concentration \+)|(?<=Known \(CL \d\d\w\w; concentration \+))\d+')
        spellmatch = spellregex.search(s)
        if spellmatch:
            result = spellmatch.group()
            spell_profile.concentration = int(result)

        # Spells
        spellregex = re.compile('[A-Z][a-z]+(?= Spells Known| Spells Prepared| Extracts Prepared)')
        spellmatch = spellregex.search(s)
        if(spellmatch):
            result = spellmatch.group()
            spell_profile.type = result
        spellregex = re.compile('((?:\d[strdthn]{2} \(\d{1,2}\/day\)|0 \(at will\)|\d[strdthn]{2}|0|\d[strdthn]{2} \(\d+\))(?:—[\d\w -+;,\(\)%\.\'\/-]+\n))+', re.MULTILINE)
        spellmatch = spellregex.search(s)
        if spellmatch:
            lines = spellmatch.group().decode('utf-8').split('\n')
            for line in lines:
                if line != '':
                    val = line.split('—'.decode('utf-8'))
                    spell_profile.spells[val[0]] = split_csv(val[1])
            # Domains, Bloodline, Opposition Schools, Mystery
            choiceregex = re.compile('(?<=Opposition Schools )[A-Za-z, ]+')
            choicematch = choiceregex.search(s)
            if choicematch:
                result = split_csv(choicematch.group())
                spell_profile.opposition_schools = result

            choiceregex = re.compile('((?<=Domains )|(?<=Domain ))[A-Z][A-Za-z, ]+(?=\n)')
            choicematch = choiceregex.search(s)
            if choicematch:
                result = split_csv(choicematch.group())
                spell_profile.domains = result

            choiceregex = re.compile('(?<=Bloodline )[a-z\(\) ]+')
            choicematch = choiceregex.search(s)
            if choicematch:
                result = choicematch.group()
                spell_profile.bloodline = result

            choiceregex = re.compile('(?<=Mystery )[a-z\(\) ]+')
            choicematch = choiceregex.search(s)
            if choicematch:
                result = choicematch.group()
                spell_profile.mystery = result

            choiceregex = re.compile('(?<=Patron )[a-z\(\) ]+')
            choicematch = choiceregex.search(s)
            if choicematch:
                result = choicematch.group()
                spell_profile.patron = result

            spell_profiles.append(spell_profile)

    # Check for Spell-Like Abilities
    regex = re.compile('.+\n(?:(?:(?:Constant|\d+\/day|At will|\d+\/week|\d+\/year)—[\d\w \/;,\(\)%\.\'-\+]+\n))+')
    matches = regex.findall(buffer)

    for s in matches:
        monster.spell_like_abilities = True
        spell_like_profile = SpellLikeProfile(name)
        spellregex = re.compile('(?<=Spell-Like Abilities \(CL )\d+')
        spellmatch = spellregex.search(s)
        # Spell-Like Ability Caster Level
        if spellmatch:
            result = spellmatch.group()
            spell_like_profile.spell_like_caster_level = int(result)


        spellregex = re.compile('[A-Z][a-z]+(?= Spell-Like Abilities)')
        spellmatch = spellregex.search(s)
        if(spellmatch):
            result = spellmatch.group()
            spell_like_profile.type = result

        # Concentration Bonus
        spellregex = re.compile('((?<=Spell-Like Abilities \(CL \d\w\w; concentration \+)|(?<=Spell-Like Abilities \(CL \d\d\w\w; concentration \+))\d+')
        spellmatch = spellregex.search(s)
        if spellmatch:
            result = spellmatch.group()
            spell_like_profile.spell_like_concentration = int(result)

        # Spell-Like Abiltiies
        regex = re.compile('((?:(?:Constant|\d+\/day|At will|\d+\/week|\d+\/year)—[\d\w \/;,\(\)%\.\'-\+]+\n))+')
        spellmatch = regex.search(s)
        if spellmatch:
            lines = spellmatch.group().decode('utf-8').split('\n')
            for line in lines:
                if line != '':
                    val = line.split('—'.decode('utf-8'))
                    spell_like_profile.spell_like_abilities[val[0]] = split_csv(val[1])

        spell_like_profiles.append(spell_like_profile)

    # Before Combat Tactics
    regex = re.compile('(?<=Before Combat ).+')
    match = regex.search(buffer)
    if match:
        result = match.group()
        monster.tactics_before_combat = result

    # During Combat Tactics
    regex = re.compile('(?<=During Combat ).+')
    match = regex.search(buffer)
    if match:
        result = match.group()
        monster.tactics_during_combat = result

    # Base Statistics Tactics
    regex = re.compile('(?<=Base Statistics ).+')
    match = regex.search(buffer)
    if match:
        result = match.group()
        monster.tactics_base_statistics = result

    # Combat Gear
    regex = re.compile('(?<=Combat Gear ).+')
    match = regex.search(buffer)
    if match:
        result = split_csv(match.group())
        monster.combat_gear = result

    # Add Source
    monster.source = source
    monsters.append(monster)
