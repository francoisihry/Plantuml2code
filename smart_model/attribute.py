from smart_model.smart_model import Accessibility

class Attribute:
    def __init__(self, name, type = None, accessibility = Accessibility.public):
        self._name = name
        self._type = type
        self._accessibility = accessibility

    @property
    def accessibitily(self):
        return self._accessibility

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

class Parameter:
    def __init__(self, name, type = None):
        self._name = name
        self._type = type

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type



class Method(Attribute):
    def __init__(self,name, type = None, accessibility = Accessibility.public,
                 parameters=[]):
        Attribute.__init__(self, name, type, accessibility)
        self._parameters = parameters

    @property
    def parameters(self):
        return  self._parameters
