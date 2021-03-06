from collections import OrderedDict

class Monster(object):
    def __init__(self, name, cr):
        self._attrs = OrderedDict()
        self.name = name
        self.cr = cr
        self.flavor_text = ""
        self.description = ""
        self.type = ""
        self.classline = ""
        self.init = 0
        self.perception = 0
        self.senses = []
        self.aura = []
        self.ac = 0
        self.ac_touch = 0
        self.ac_flat_footed = 0
        self.ac_bonuses = []
        self.hp = ""
        self.health_rules = ""
        self.save_fortitude = 0
        self.save_reflex = 0
        self.save_will = 0
        self.saving_throw_modifiers = []
        self.spell_resist = 0
        self.damage_reductions = []
        self.defensive_abilities = []
        self.immunities = []
        self.resistences = []
        self.weaknesses = []
        self.speed_profile = ""
        self.melee_profile = ""
        self.ranged_profile = ""
        self.special_attacks = ""
        self.space = 0
        self.reach = 0
        self.offensive_abilities = ""
        self.psychic_magic_caster_level = 0
        self.psychic_magic_concentration = 0
        self.psychic_magic_abilities = []
        self.psychic_energy_pool = 0
        self.spellcaster = False
        self.spell_like_abilities = False
        self.strength = 0
        self.dexterity = 0
        self.constitution = 0
        self.intelligence = 0
        self.wisdom = 0
        self.charisma = 0
        self.base_attack_bonus = 0
        self.combat_maneuver_bonus = 0
        self.combat_maneuver_defense = 0
        self.feats = []
        self.skills = []
        self.racial_skill_modifiers = []
        self.languages = []
        self.language_special_rules = []
        self.special_qualities = ""
        self.environment = ""
        self.organization = ""
        self.treasure = ""
        self.page = ""
        self.source = ""
        self.combat_gear = []
        self.tactics_during_combat = ""
        self.tactics_before_combat = ""
        self.tactics_base_statistics = ""
        self.boon = ""

    def __getattr__(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == '_attrs':
            return super(Monster, self).__setattr__(name, value)
        self._attrs[name] = value
