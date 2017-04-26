class Visibility:
    (public,
     private,
     protected
    ) = range(3)


class Access:
    (static,
     abstract
    ) = range(2)


class Attribute:
    def __init__(self, name, type=None,
                 visibility=Visibility.public,
                 access=None):
        self._name = name
        self._type = type
        self._visibility = visibility
        self._access = access

    @property
    def visibility(self):
        return self._visibility

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def access(self):
        return self._access


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
    def __init__(self, name, type = None, visibility = Visibility.public,
                 access=None,
                 parameters=[]):
        Attribute.__init__(self, name, type, visibility, access)
        self._parameters = parameters

    @property
    def parameters(self):
        return  self._parameters


