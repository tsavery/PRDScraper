from collections import OrderedDict

class SpecialRule(object):
    def __init__(self, page):
        self._attrs = OrderedDict()
        self.page = page
        self.universal = True
        self.name = ""
        self.type = ""
        self.text = ""
        self.source = ""

    def __getattr__(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == '_attrs':
            return super(SpecialRule, self).__setattr__(name, value)
        self._attrs[name] = value
