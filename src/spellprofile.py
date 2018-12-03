class SpellProfile(object):
    def __init__(self, name):
        self.name = name
        self.type = ""
        self.caster_level = 0
        self.spells = {}
        self.concentration = 0
        self.domains = []
        self.opposition_schools = []
        self.bloodline = ""
