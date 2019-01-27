from collections import OrderedDict

class SpellProfile(object):
    def __init__(self, name):
        self._attrs = OrderedDict()
        self.name = name
        self.type = ""
        self.caster_level = 0
        self.concentration = 0
        self.spells = OrderedDict()
        self.domains = []
        self.opposition_schools = []
        self.bloodline = ""
        self.patron = ""
        self.mystery = ""
        self.source = ""

    def __getattr__(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == '_attrs':
            return super(SpellProfile, self).__setattr__(name, value)
        self._attrs[name] = value
