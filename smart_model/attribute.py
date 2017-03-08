from smart_model import Accessibility

class Attribute:
    def __init__(self, name, type = None, accessibility = Accessibility.public):
        self._name = name
        self._type = type
        self._accessibility = accessibility

class Parameter:
    def __init__(self, name, type = Accessibility.public):
        self._name = name
        self._type = type

class Method(Attribute):
    def __init__(self,name, type = None, accessibility = Accessibility.public,
                 parameters=[]):
        Attribute.__init__(name, type, accessibility)
        self._parameters = parameters
