# -*- coding: utf-8 -*-

# import libraries
import re
import utils
from monster import Monster
from spellprofile import SpellProfile
from spelllikeprofile import SpellLikeProfile
from specialrule import SpecialRule
from collections import OrderedDict

def get_string(str, buffer):
    regex = re.compile(str)
    match = regex.search(buffer)
    if match:
        result = match.group()
        return result
    else:
        return ''

def get_signed_integer(str, buffer):
    regex = re.compile(str)
    match = regex.search(buffer)
    if match:
        result = match.group()
        if result[0] == '+':
            return int(result[1:])
        else:
            return (int(result[1:]) * -1)
    else:
        return 0

def get_integer(str, buffer):
    regex = re.compile(str)
    match = regex.search(buffer)
    if match:
        result = match.group()
        return int(result)
    else:
        return 0

def split_csv(str):
    return re.split(', (?![^(]*\))', str)

def get_csv(str, buffer):
    regex = re.compile(str)
    match = regex.search(buffer)
    if match:
        result = split_csv(match.group())
        return result
    else:
        return []

def get_language_special_rules(buffer):
    regex = re.compile('(?<=Languages ).+')
    match = regex.search(buffer)
    if match:
        val = match.group().split("; ")
        if len(val) > 1:
            result = split_csv(val[1])
            return result
        else:
            return []
    else:
        return []

def get_class_line(buffer):
    regex = re.compile('(?<=\n)[A-Z][a-z\-]+(?:[a-z/\(\)\d\- ]+) *\d{1,2}(?=\n)')
    matches = regex.findall(buffer)
    if len(matches) is 1:
        result = matches[0]
        if 'Speed' not in result and 'Resist' not in result and 'speed' not in result and 'resist' not in result:
            return result
        else:
            return ''
    elif len(matches) > 1:
        result = matches[0]
        for s in range(1, len(matches)):
            if 'Speed' not in matches[s] and 'Resist' not in matches[s] and 'speed' not in matches[s] and 'resist' not in matches[s]:
                result += '/' + matches[s].lower()

        if 'Speed' not in result and 'Resist' not in result and 'speed' not in result and 'resist' not in result:
            return result
        else:
            return ''
    else:
        return ''

def get_psychic_pool_and_abilities(buffer):
    regex = re.compile('(?:\d+ PE—)[\d\w ;,\(\)%\.\'\/]+')
    match = regex.search(buffer)

    if match:
        result = match.group()
        return result.split(' PE—')
    else:
        regex = re.compile('(?:\d+ PE —)[\d\w ;,\(\)%\.\'\/]+')
        match = regex.search(buffer)

        if match:
            result = match.group()
            return result.split(' PE —')
        else:
            regex = re.compile('(?:\d+ PE \(see whelp magic\)—)[\d\w ;,\(\)%\.\'\/]+')
            match = regex.search(buffer)

            if match:
                result = match.group()
                return result.split(' PE (see whelp magic)—')

def get_spells(str, buffer):
    regex = re.compile(str)
    match = regex.search(buffer)
    spells = OrderedDict()
    if match:
        lines = match.group().split('\n')
        for line in lines:
            if line != '':
                val = line.split('—')
                spells[val[0]] = split_csv(val[1])

    return spells

def get_spell_casting_profiles(buffer, name, source):
    regex = re.compile('.+\n(?:(?:\d[strdthn]{2} \(\d{1,2}\/day\)|0 \(at will\)|\d[strdthn]{2}|0|\d[strdthn]{2} \(\d+\))(?:—[\d\w -+;,\(\)%\.\'\/]+\n))+(?:(?:D |Bloodline [a-z]|Opposition Schools [a-z]|Patron [a-z]|Mystery [a-z]| Domain [a-z]| Domains [a-z])[\*\d\w\(\) ;,]+\n){0,1}')
    matches = regex.findall(buffer)
    results = []
    if len(matches) > 0:
        results.append(True)
        for s in matches:
            spell_profile = SpellProfile(name)
            # Caster Level & Concentration & Type
            spell_profile.caster_level = get_integer('((?<=Spells Known \(CL )|(?<=Spells Prepared \(CL )|(?<=Extracts Prepared \(CL ))\d+', s)
            spell_profile.concentration = get_integer('((?<=Prepared \(CL \d\w\w; concentration \+)|(?<=Prepared \(CL \d\d\w\w; concentration \+)|(?<=Known \(CL \d\w\w; concentration \+)|(?<=Known \(CL \d\d\w\w; concentration \+))\d+', s)
            spell_profile.type = get_string('[A-Z][a-z]+(?= Spells Known| Spells Prepared| Extracts Prepared)', s)

            #Spells
            spell_profile.spells = get_spells('((?:\d[strdthn]{2} \(\d{1,2}\/day\)|0 \(at will\)|\d[strdthn]{2}|0|\d[strdthn]{2} \(\d+\))(?:—[\d\w -+;,\(\)%\.\'\/-]+\n))+', s)

            # Domains, Bloodline, Opposition Schools, Mystery
            spell_profile.opposition_schools = get_csv('(?<=Opposition Schools )[A-Za-z, ]+', s)
            spell_profile.domains = get_csv('((?<=Domains )|(?<=Domain ))[A-Z][A-Za-z, ]+(?=\n)', s)
            spell_profile.bloodline = get_string('(?<=Bloodline )[a-z\(\) ]+', s)
            spell_profile.mystery = get_string('(?<=Mystery )[a-z\(\) ]', s)
            spell_profile.patron = get_string('(?<=Patron )[a-z\(\) ]+', s)

            # Source
            spell_profile.source = source

            results.append(spell_profile)
    else:
        results.append(False)

    return results

def get_spell_like_ability_profiles(buffer, name, source):
    regex = re.compile('.+\n(?:(?:(?:Constant|\d+\/day|At will|\d+\/week|\d+\/year)—[\d\w \/;,\(\)%\.\'-\+]+\n))+')
    matches = regex.findall(buffer)
    results = []
    if len(matches) > 0:
        results.append(True)
        for s in matches:
            spell_like_profile = SpellLikeProfile(name)

            # Caster Level & Concentration & Type
            spell_like_profile.caster_level = get_integer('(?<=Spell-Like Abilities \(CL )\d+', s)
            spell_like_profile.type = get_string('[A-Z][a-z]+(?= Spell-Like Abilities)', s)
            spell_like_profile.concentration = get_integer('((?<=Spell-Like Abilities \(CL \d\w\w; concentration \+)|(?<=Spell-Like Abilities \(CL \d\d\w\w; concentration \+))\d+', s)

            # Spell-Like Abiltiies
            spell_like_profile.abilities = get_spells('((?:(?:Constant|\d+\/day|At will|\d+\/week|\d+\/year)—[\d\w \/;,\(\)%\.\'-\+]+\n))+', s)

            # Source
            spell_like_profile.source = source

            results.append(spell_like_profile)
    else:
        results.append(False)
    return results

def scrape_monster(buffer, name, cr, monsters, spell_profiles, spell_like_profiles, page, source, flavor_text, description):
    monster = Monster(name, cr)

    ##Flavor Text and Description
    monster.flavor_text = flavor_text
    monster.description = description

    ## General
    #Typeline
    monster.type = get_string('[LEGCN]{1,2} (Fine|Diminutive|Tiny|Small|Medium|Large|Huge|Gargantuan|Colossal).+', buffer)
    #Classline
    monster.classline = get_class_line(buffer)
    # Initiative Bonus
    monster.init = get_signed_integer('(?<=Init ).\d+', buffer)
    # Senses
    monster.senses = get_csv('(?<=Senses ).+(?=;)', buffer)
    # Perception Bonus
    monster.perception = get_signed_integer('(?<=Perception ).\d+', buffer)
    # Auras
    monster.aura = get_csv('(?<=Aura ).+', buffer)

    ## Defense
    # AC and Bonuses
    monster.ac = get_integer('(?<=AC )\d+', buffer)
    monster.ac_touch = get_integer('(?<=touch )\d+', buffer)
    monster.ac_flat_footed = get_integer('(?<=flat-footed )\d+', buffer)
    monster.ac_bonuses = get_csv('((?<=flat-footed \d\d \()|(?<=flat-footed \d \()).+(?=\))', buffer)
    # HP & Special Rules
    monster.hp = get_string('(?<=hp )[0-9\(\)d\+– ]+(?=[;\n])', buffer)
    monster.health_rules = get_string('(?<=\d\); ).+(?=\nFort)', buffer)
    # Saves
    monster.save_fortitude = get_signed_integer('(?<=Fort ).\d+', buffer)
    monster.save_reflex = get_signed_integer('(?<=Ref ).\d+', buffer)
    monster.save_will = get_signed_integer('(?<=Will ).\d+', buffer)
    monster.saving_throw_modifiers = get_csv('((?<=Will \+\d; )|(?<=Will \+\d\d; )).+', buffer)
    # Resistences, Immunities and Weaknesses
    monster.spell_resist = get_integer('(?<=SR )\d+', buffer)
    monster.damage_reductions = get_csv('(?<=DR )[\d\/, \w]+', buffer)
    monster.immunities = get_csv('(?<=Immune )[\d \w\+\(\)–,]+', buffer)
    monster.weaknesses = get_csv('(?<=Weaknesses )[\d \w\+\(\)–,]+', buffer)
    monster.resistences = get_csv('(?<=Resist )[\d \w\+\(\)–,]+', buffer)
    # Defenseive Abilities
    monster.defensive_abilities = get_csv('(?<=Defensive Abilities )[\d \w\+\(\)–,]+', buffer)

    ## Offense
    # Speed Profile
    monster.speed_profile = get_string('(?<=Speed ).+', buffer)
    # Attacks
    monster.melee_profile = get_string('(?<=Melee ).+', buffer)
    monster.ranged_profile = get_string('(?<=Ranged ).+', buffer)
    monster.special_attacks = get_string('(?<=Special Attacks ).+', buffer)
    # Space & Reach
    monster.space = get_integer('(?<=Space )\d+', buffer)
    monster.reach = get_integer('(?<=Reach )\d+', buffer)
    # Offensive Abilities
    monster.offensive_abilities = get_csv('(?<=Offensive Abilities )[\d \w\+\(\)–,]+', buffer)

    ##Statistics
    # Ability Scores
    monster.strength = get_integer('(?<=\nStr )\d+', buffer)
    monster.dexterity = get_integer('(?<=, Dex )\d+', buffer)
    monster.constitution = get_integer('(?<=, Con )\d+', buffer)
    monster.intelligence = get_integer('(?<=, Int )\d+', buffer)
    monster.wisdom = get_integer('(?<=, Wis )\d+', buffer)
    monster.charisma = get_integer('(?<=, Cha )\d+', buffer)
    # Base Attack Bonus
    monster.base_attack_bonus = get_integer('(?<=Base Atk \+)\d+', buffer)
    # Combat Maneuver Bonus & Defense
    monster.combat_maneuver_bonus = get_signed_integer('(?<=CMB ).\d+', buffer)
    monster.combat_maneuver_defense = get_integer('(?<=CMD )\d+', buffer)
    # Feats, Skills and Languages
    monster.feats = get_csv('(?<=Feats ).+', buffer)
    monster.skills = get_csv('(?<=Skills )[A-Za-z \(\)\+–—,\d]+', buffer)
    monster.racial_skill_modifiers = get_csv('(?<=Racial Modifiers )[A-Za-z \(\)\+–,\d]+', buffer)
    monster.languages = get_csv('(?<=Languages )[A-Za-z\d,\.\' ]+', buffer)
    monster.language_special_rules = get_language_special_rules(buffer)
    # Special Qualities
    monster.special_qualities = get_string('(?<=SQ ).+', buffer)

    ##Ecology
    # Enviroment, Organization, Treasure
    monster.environment = get_string('(?<=Environment ).+', buffer)
    monster.organization = get_string('(?<=Organization ).+', buffer)
    monster.treasure = get_string('(?<=Treasure ).+', buffer)

    # Encode the buffer for spellcasting checks
    buffer = buffer

    ## Spellcasting, Spell-Like Abilities and Psychic Magic
    # Psychic Magic
    monster.psychic_magic_caster_level = get_integer('(?<=Psychic Magic \(CL )\d+', buffer)

    if monster.psychic_magic_caster_level != 0:
        # Concentration
        monster.psychic_magic_concentration = get_integer('((?<=Psychic Magic \(CL \d\w\w; concentration \+)|(?<=Psychic Magic \(CL \d\d\w\w; concentration \+))\d+', buffer)
        # Energy Pool and Abilities
        result = get_psychic_pool_and_abilities(buffer)
        monster.psychic_energy_pool = int(result[0])
        monster.psychic_magic_abilities = split_csv(result[1])

    # Spellcasting
    result = get_spell_casting_profiles(buffer, monster.name, source)
    monster.spellcaster = result[0]
    if monster.spellcaster is True:
        for s in range(1, len(result)):
            spell_profiles.append(result[s])

    # Spell-Like Abilities
    result = get_spell_like_ability_profiles(buffer, monster.name, source)
    monster.spell_like_abilities = result[0]
    if monster.spell_like_abilities is True:
        for s in range(1, len(result)):
            spell_like_profiles.append(result[s])

    ## Tactics
    monster.tactics_before_combat = get_string('(?<=Before Combat ).+', buffer)
    monster.tactics_during_combat = get_string('(?<=During Combat ).+', buffer)
    monster.tactics_base_statistics = get_string('(?<=Base Statistics ).+', buffer)
    monster.combat_gear = get_csv('(?<=Combat Gear ).+', buffer)

    monster.boon = get_string('(?<=Boon ).+', buffer)

    # Add Source
    monster.page = page
    monster.source = source
    monsters.append(monster)

def scrape_special_rules(special_rules, buffer, universal, page, source):
    regex = re.compile('(?:[\w.()-]+ )+\((?:Su|Ex|Sp)\):* .+')
    matches = regex.findall(buffer)

    for s in matches:
        special_rule = SpecialRule(page)
        special_rule.name = get_string('.+(?= \((?:Su|Ex|Sp)\))', s)
        special_rule.type = get_string('(?:Su|Ex|Sp)', s)
        special_rule.text = get_string('((?<=\((?:Su|Ex|Sp)\) )|(?<=\((?:Su|Ex|Sp)\): )).+', s)
        special_rule.source = source
        special_rule.universal = universal

        special_rules.append(special_rule)
