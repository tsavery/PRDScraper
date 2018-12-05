class SpellLikeProfile(object):
    def __init__(self, name):
        self.name = name
        self.type = ""
        self.spell_like_caster_level = 0
        self.spell_like_concentration = 0
        self.spell_like_abilities = {}
