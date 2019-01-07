# -*- coding: utf-8 -*-

import sys
sys.path.append('../')

import unittest
import scraper
from spellprofile import SpellProfile
from spelllikeprofile import SpellLikeProfile
from monster import Monster
from collections import OrderedDict

class TestScraperFunctions(unittest.TestCase):

    def setUp(self):
        self.monster_name_test = 'Celestial Theurge'
        self.monster_cr_test = '8'
        self.monster_stat_block_test = """XP 4,800
Human cleric 3
Sorcerer 4
Mystic theurge 2
NG Medium humanoid (human)
Init +5; Senses Perception +8
Defense
AC 18, touch 10, flat-footed 18 (+7 armor, +1 natural)
hp 69 (3d8+4d6+2d6+31); regeneration 5 (acid or fire)
Fort +8, Ref +4, Will +11; +2 vs. magic
Defensive Abilities barbed defense; DR 10/good; Immune fire, poison; Resist acid 10, cold 10; SR 22
Offense
Speed 20 ft.
Melee +1 spear +13 (1d8+7)
Ranged mwk heavy crossbow +6 (1d10)
Space 30 ft.; Reach 30 ft.
Special Attacks channel positive energy 6/day (DC 12 [DC 14 against undead], 2d6)
Bloodline Spell-Like Abilities (CL 4th; concentration +5)
4/day—heavenly fire (1d4+2)
Domain Spell-Like Abilities (CL 3rd; concentration +5)
5/day—rebuke death, touch of glory
Spell-Like Abilities (CL 12th)
At will—greater teleport (self plus 50 lbs. of objects only), hold person (DC 17), major image (DC 17), produce flame, pyrotechnics (DC 16), scorching ray (2 rays only)
1/day—order's wrath (DC 18), summon (level 4, 1 barbed devil 35%), unholy blight (DC 18)
Cleric Spells Prepared (CL 5th; concentration +7)
3rd—prayer, searing ligh tD
2nd—bless weaponD, delay poison, remove paralysis, shield other
1st—cure light woundsD, divine favor (2), protection from evil, remove fear
0 (at will)—create water, guidance, purify food and drink, stabilize
D Domain spell; Domains Glory, Healing
Sorcerer Spells Known (CL 6th; concentration +7; 25% spell failure)
3rd (3/day)—haste
2nd (5/day)—bull's strength, protection from arrows
1st (7/day)—bless, burning hands (DC 12), enlarge person, shield, true strike
0 (at will)—dancing lights, detect magic, detect poison, mage hand, mending, message, read magic
Bloodline celestial
Tactics
Before Combat The mystic theurge casts bull's strength.
During Combat The mystic theurge casts haste and shield, then supports her companions with spells. She targets undead with channeled energy and searing light.
Base Statistics Without bull's strength, the mystic theurge's statistics are Melee +1 spear +11 (1d8+5/×3).
Statistics
Str 22, Dex 10, Con 14, Int 8, Wis 14, Cha 12
Base Atk +5; CMB +11; CMD 21
Feats Arcane Armor Mastery, Arcane Armor Training, Combat Casting, Eschew Materials, Extra Channel, Toughness, Weapon Focus (spear)
Skills Diplomacy +7, Knowledge (arcana, religion) +5, Knowledge (nobility) +4, Perception +8, Spellcraft +3
Languages Common
SQ aura, bloodline arcana (summoned creatures gain DR 2/evil), combined spells (1st)
Combat Gear +1 bolts (3), +1 evil outsider-bane bolts (3), +1 undead-bane bolts (3), scrolls of cure serious wounds (2), scrolls of neutralize poison (2), scroll of remove disease, antitoxin (2), holy water (2); Other Gear +1 breastplate, +1 spear, masterwork heavy crossbow with 10 bolts, amulet of natural armor +1, cloak of resistance +1, pair of platinum rings (worth 50 gp), 287 gp
Ecology
Environment any (Hell)
Organization solitary
Treasure standard"""

    def test_get_string(self):
        self.assertEqual(scraper.get_string('Foo', 'FooBar'), 'Foo')
        self.assertEqual(scraper.get_string('\w+', 'FooBar'), 'FooBar')
        self.assertEqual(scraper.get_string('\d+', 'FooBar'), '')

    def test_get_integer(self):
        self.assertEqual(scraper.get_integer('\d+', 'ABC45FGH'), 45)
        self.assertEqual(scraper.get_integer('\d+', 'ABCDEFGH'), 0)

    def test_get_signed_integer(self):
        self.assertEqual(scraper.get_signed_integer('.\d+', 'Init +4'), 4)
        self.assertEqual(scraper.get_signed_integer('.\d+', 'Init -4'), -4)
        self.assertEqual(scraper.get_signed_integer('.\d+', 'ABCDEF'), 0)

    def test_split_csv(self):
        self.assertEqual(scraper.split_csv('oranges, apples(12, red), bananas'), ['oranges', 'apples(12, red)', 'bananas'])
        self.assertEqual(scraper.split_csv('apples(12, red)'), ['apples(12, red)'])

    def test_get_csv(self):
        self.assertEqual(scraper.get_csv('(?<=Feats ).+', 'Feats One, Two, Three(Four, Five)'), ['One', 'Two', 'Three(Four, Five)'])
        self.assertEqual(scraper.get_csv('(?<=Feats ).+', 'Skills One, Two, Three(Four, Five)'), [])

    def test_get_language_special_rules(self):
        self.assertEqual(scraper.get_language_special_rules('Languages Common, Sylvan; telepathy 100 ft., speak with animals'), ['telepathy 100 ft.', 'speak with animals'])
        self.assertEqual(scraper.get_language_special_rules('Languages Common, Sylvan; telepathy 100 ft.'), ['telepathy 100 ft.'])
        self.assertEqual(scraper.get_language_special_rules('Languages Common, Sylvan'), [])

    def test_get_class_line(self):
        self.assertEqual(scraper.get_class_line('\nAasimar cleric 1\n'), 'Aasimar cleric 1')
        self.assertEqual(scraper.get_class_line('\nHuman animal lord ranger 10\n'), 'Human animal lord ranger 10')
        self.assertEqual(scraper.get_class_line('\nHalfling bard 5\nDruid 4\nMystic theurge 4\n'), 'Halfling bard 5/druid 4/mystic theurge 4')
        self.assertEqual(scraper.get_class_line('\nBugbear ninja 5/shadowdancer 4\n'), 'Bugbear ninja 5/shadowdancer 4')

    def test_get_psychic_pool_and_abilities(self):
        self.assertEqual(scraper.get_psychic_pool_and_abilities('20 PE—one (3 PE), two(2 PE, DC 17), three (5 PE), four (4 PE, DC 9)'), ['20', 'one (3 PE), two(2 PE, DC 17), three (5 PE), four (4 PE, DC 9)'])
        self.assertEqual(scraper.get_psychic_pool_and_abilities('20 PE —one (3 PE), two(2 PE, DC 17), three (5 PE), four (4 PE, DC 9)'), ['20', 'one (3 PE), two(2 PE, DC 17), three (5 PE), four (4 PE, DC 9)'])
        self.assertEqual(scraper.get_psychic_pool_and_abilities('0 PE (see whelp magic)—one (3 PE), two(2 PE, DC 17), three (5 PE), four (4 PE, DC 9)'), ['0', 'one (3 PE), two(2 PE, DC 17), three (5 PE), four (4 PE, DC 9)'])

    def test_get_spells(self):
        input = '1st—bless, command (DC 14), protection from evilD\n0 (at will)—detect magic, guidance, stabilize\n'
        correct = OrderedDict()
        correct['1st'] = ['bless', 'command (DC 14)', 'protection from evilD']
        correct['0 (at will)'] = ['detect magic', 'guidance', 'stabilize']
        self.assertEqual(scraper.get_spells('((?:\d[strdthn]{2} \(\d{1,2}\/day\)|0 \(at will\)|\d[strdthn]{2}|0|\d[strdthn]{2} \(\d+\))(?:—[\d\w -+;,\(\)%\.\'\/-]+\n))+', input), correct)

        input = '2nd (7)—calm emotions (DC 21), eagle\'s splendor, gallant inspiration, honeyed tongue, share memory (DC 21), tactical acumen\n1st (8)—hideous laughter (DC 20), identify, liberating command, saving finale, solid note, timely inspiration\n0 (at will)—detect magic, ghost sound (DC 19), lullaby (DC 19), message, prestidigitation, summon instrument\n'
        correct = OrderedDict()
        correct['2nd (7)'] = ['calm emotions (DC 21)', 'eagle\'s splendor', 'gallant inspiration', 'honeyed tongue', 'share memory (DC 21)', 'tactical acumen']
        correct['1st (8)'] = ['hideous laughter (DC 20)', 'identify', 'liberating command', 'saving finale', 'solid note', 'timely inspiration']
        correct['0 (at will)'] = ['detect magic', 'ghost sound (DC 19)', 'lullaby (DC 19)', 'message', 'prestidigitation', 'summon instrument']
        self.assertEqual(scraper.get_spells('((?:\d[strdthn]{2} \(\d{1,2}\/day\)|0 \(at will\)|\d[strdthn]{2}|0|\d[strdthn]{2} \(\d+\))(?:—[\d\w -+;,\(\)%\.\'\/-]+\n))+', input), correct)

    def test_get_spell_casting_profiles_success(self):
        results = scraper.get_spell_casting_profiles(self.monster_stat_block_test, self.monster_name_test)

        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], True)

        self.assertTrue(isinstance(results[1], SpellProfile))
        self.assertEqual(results[1].name, self.monster_name_test)
        self.assertEqual(results[1].type, 'Cleric')
        self.assertEqual(results[1].caster_level, 5)
        self.assertEqual(results[1].concentration, 7)
        cleric_spells = OrderedDict()
        cleric_spells['3rd'] = ['prayer', 'searing ligh tD']
        cleric_spells['2nd'] = ['bless weaponD', 'delay poison', 'remove paralysis', 'shield other']
        cleric_spells['1st'] = ['cure light woundsD', 'divine favor (2)', 'protection from evil', 'remove fear']
        cleric_spells['0 (at will)'] = ['create water', 'guidance', 'purify food and drink', 'stabilize']
        self.assertDictEqual(results[1].spells, cleric_spells )
        self.assertEqual(results[1].domains, ['Glory', 'Healing'])
        self.assertEqual(results[1].opposition_schools, [])
        self.assertEqual(results[1].bloodline, '')
        self.assertEqual(results[1].patron, '')
        self.assertEqual(results[1].mystery, '')

        self.assertTrue(isinstance(results[2], SpellProfile))
        self.assertEqual(results[2].name, self.monster_name_test)
        self.assertEqual(results[2].type, 'Sorcerer')
        self.assertEqual(results[2].caster_level, 6)
        self.assertEqual(results[2].concentration, 7)
        sorc_spells = OrderedDict()
        sorc_spells['3rd (3/day)'] = ['haste']
        sorc_spells['2nd (5/day)'] = ['bull\'s strength', 'protection from arrows']
        sorc_spells['1st (7/day)'] = ['bless', 'burning hands (DC 12)', 'enlarge person', 'shield', 'true strike']
        sorc_spells['0 (at will)'] = ['dancing lights', 'detect magic', 'detect poison', 'mage hand', 'mending', 'message', 'read magic']
        self.assertDictEqual(results[2].spells, sorc_spells )
        self.assertEqual(results[2].domains, [])
        self.assertEqual(results[2].opposition_schools, [])
        self.assertEqual(results[2].bloodline, 'celestial')
        self.assertEqual(results[2].patron, '')
        self.assertEqual(results[2].mystery, '')

    def test_get_spell_casting_profiles_failure(self):
        results = scraper.get_spell_casting_profiles('', 'name')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], False)

    def test_get_spell_like_ability_profiles_success(self):
        results = scraper.get_spell_like_ability_profiles(self.monster_stat_block_test, self.monster_name_test)
        self.assertEqual(results[0], True)
        self.assertEqual(len(results), 4)

        self.assertIsInstance(results[1], SpellLikeProfile)
        self.assertEqual(results[1].name, self.monster_name_test)
        self.assertEqual(results[1].type, 'Bloodline')
        self.assertEqual(results[1].caster_level, 4)
        self.assertEqual(results[1].concentration, 5)
        bloodline_abilities = OrderedDict()
        bloodline_abilities['4/day'] = ['heavenly fire (1d4+2)']
        self.assertEqual(results[1].abilities, bloodline_abilities)

        self.assertIsInstance(results[2], SpellLikeProfile)
        self.assertEqual(results[2].name, self.monster_name_test)
        self.assertEqual(results[2].type, 'Domain')
        self.assertEqual(results[2].caster_level, 3)
        self.assertEqual(results[2].concentration, 5)
        domain_abilities = OrderedDict()
        domain_abilities['5/day'] = ['rebuke death', 'touch of glory']
        self.assertDictEqual(results[2].abilities, domain_abilities)

        self.assertIsInstance(results[3], SpellLikeProfile)
        self.assertEqual(results[3].name, self.monster_name_test)
        self.assertEqual(results[3].type, '')
        self.assertEqual(results[3].caster_level, 12)
        self.assertEqual(results[3].concentration, 0)
        base_abilities = OrderedDict()
        base_abilities['At will'] = ['greater teleport (self plus 50 lbs. of objects only)', 'hold person (DC 17)', 'major image (DC 17)', 'produce flame', 'pyrotechnics (DC 16)', 'scorching ray (2 rays only)']
        base_abilities['1/day'] = ['order\'s wrath (DC 18)', 'summon (level 4, 1 barbed devil 35%)', 'unholy blight (DC 18)']
        self.assertDictEqual(results[3].abilities, base_abilities)

    def test_get_spell_like_ability_profiles_failure(self):
        results = scraper.get_spell_like_ability_profiles('', 'name')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], False)

    def test_scrape_monster(self):
        monsters = []
        spellprofiles = []
        spelllikeprofiles = []

        scraper.scrape_monster(self.monster_stat_block_test.decode('utf-8'), self.monster_name_test, self.monster_cr_test, monsters, spellprofiles, spelllikeprofiles, 'Test Source')
        self.assertEqual(len(monsters), 1, 'Monster list length is: ' + str(len(monsters)) + ', expected: 1' )
        self.assertIsInstance(monsters[0], Monster, 'First Entry is not of type Monster')

        monster = monsters[0]
        self.assertEqual(monster.type, 'NG Medium humanoid (human)')
        self.assertEqual(monster.classline, 'Human cleric 3/sorcerer 4/mystic theurge 2')
        self.assertEqual(monster.init, 5)
        self.assertEqual(monster.perception, 8)
        self.assertEqual(monster.senses, [])
        self.assertEqual(monster.aura, [])
        self.assertEqual(monster.ac, 18)
        self.assertEqual(monster.ac_touch, 10)
        self.assertEqual(monster.ac_flat_footed, 18)
        self.assertEqual(monster.ac_bonuses, ['+7 armor', '+1 natural'])
        self.assertEqual(monster.hp, '69 (3d8+4d6+2d6+31)')
        self.assertEqual(monster.health_rules, 'regeneration 5 (acid or fire)')
        self.assertEqual(monster.save_fortitude, 8)
        self.assertEqual(monster.save_reflex, 4)
        self.assertEqual(monster.save_will, 11)
        self.assertEqual(monster.saving_throw_modifiers, ['+2 vs. magic'])
        self.assertEqual(monster.spell_resist, 22)
        self.assertEqual(monster.damage_reductions, ['10/good'])
        self.assertEqual(monster.defensive_abilities, ['barbed defense'])
        self.assertEqual(monster.immunities, ['fire', 'poison'])
        self.assertEqual(monster.resistences, ['acid 10', 'cold 10'])
        self.assertEqual(monster.weaknesses, [])
        self.assertEqual(monster.speed_profile, '20 ft.')
        self.assertEqual(monster.melee_profile, '+1 spear +13 (1d8+7)')
        self.assertEqual(monster.ranged_profile, 'mwk heavy crossbow +6 (1d10)')
        self.assertEqual(monster.special_attacks, 'channel positive energy 6/day (DC 12 [DC 14 against undead], 2d6)')
        self.assertEqual(monster.offensive_abilities, [])
        self.assertEqual(monster.psychic_magic_caster_level, 0)
        self.assertEqual(monster.psychic_magic_concentration, 0)
        self.assertEqual(monster.psychic_energy_pool, 0)
        self.assertEqual(monster.psychic_magic_abilities, [])
        self.assertTrue(monster.spellcaster)
        self.assertTrue(monster.spell_like_abilities)
        self.assertEqual(monster.space, 30)
        self.assertEqual(monster.reach, 30)
        self.assertEqual(monster.strength, 22)
        self.assertEqual(monster.dexterity, 10)
        self.assertEqual(monster.constitution, 14)
        self.assertEqual(monster.intelligence, 8)
        self.assertEqual(monster.wisdom, 14)
        self.assertEqual(monster.charisma, 12)
        self.assertEqual(monster.base_attack_bonus, 5)
        self.assertEqual(monster.combat_maneuver_bonus, 11)
        self.assertEqual(monster.combat_maneuver_defense, 21)
        self.assertEqual(monster.feats, ['Arcane Armor Mastery', 'Arcane Armor Training', 'Combat Casting', 'Eschew Materials', 'Extra Channel', 'Toughness', 'Weapon Focus (spear)'])
        self.assertEqual(monster.skills, ['Diplomacy +7', 'Knowledge (arcana, religion) +5', 'Knowledge (nobility) +4', 'Perception +8', 'Spellcraft +3'])
        self.assertEqual(monster.racial_skill_modifiers, [])
        self.assertEqual(monster.languages, ['Common'])
        self.assertEqual(monster.language_special_rules, [])
        self.assertEqual(monster.special_qualities, 'aura, bloodline arcana (summoned creatures gain DR 2/evil), combined spells (1st)')
        self.assertEqual(monster.environment, 'any (Hell)')
        self.assertEqual(monster.organization, 'solitary')
        self.assertEqual(monster.treasure, 'standard')
        self.assertEqual(monster.source, 'Test Source')
        self.assertEqual(monster.tactics_during_combat, 'The mystic theurge casts haste and shield, then supports her companions with spells. She targets undead with channeled energy and searing light.')
        self.assertEqual(monster.tactics_before_combat, 'The mystic theurge casts bull\'s strength.')
        self.assertEqual(monster.tactics_base_statistics, 'Without bull\'s strength, the mystic theurge\'s statistics are Melee +1 spear +11 (1d8+5/×3).')

        self.assertEqual(len(spellprofiles), 1)
        self.assertIsInstance(spellprofiles[1], SpellProfile)
        self.assertEqual(len(spellprofiles), 1)
        self.assertIsInstance(spellprofiles[1], SpellProfile)
        
if __name__ == '__main__':
    unittest.main()
