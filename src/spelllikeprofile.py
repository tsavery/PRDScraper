from collections import OrderedDict

class SpellLikeProfile(object):
    def __init__(self, name):
        self._attrs = OrderedDict()
        self.name = name
        self.type = ""
        self.spell_like_caster_level = 0
        self.spell_like_concentration = 0
        self.spell_like_abilities = OrderedDict()

    def __getattr__(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == '_attrs':
            return super(SpellLikeProfile, self).__setattr__(name, value)
        self._attrs[name] = value
