
class Attribute:
    def __init__(self, name, type = None, accessibility = "public"):
        self._name = name
        self._type = type
        self._accessibility = accessibility

class Parameter:
    def __init__(self, name, type = "public"):
        self._name = name
        self._type = type

class Method(Attribute):
    def __init__(self,name, type = None, accessibility = "public",
                 parameters=[]):
        Attribute.__init__(name, type, accessibility)
        self._parameters = parameters
