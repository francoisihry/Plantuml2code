
class SmartModel:
    def __init__(self, classes=[], packages=[]):
        self._classes = classes
        self._packages = packages

    @property
    def classes(self):
        return self._classes

    @property
    def packages(self):
        return self._packages

    def add_class(self, c):
        self._classes.append(c)

    def add_package(self, p):
        self._packages.append(p)

Accessibility = ["public", "private", "protected", "static"]

class Class:
    def __init__(self, name,
                 accessibility = "public",
                 path = [],
                 attributes = [],
                 methods = [],
                 contained_classes = [],
                 contained_by = None,
                 reference_to = [],
                 is_referenced_by = [],
                 herits_of = [],
                 is_herited_by = []
                 ):
        self._name = name
        self._accessibility = accessibility
        self._path = path
        # Attributes
        self._attributes = attributes
        self._methods = methods
        # Composition
        self._contains = contained_classes
        self._contained_by =contained_by
        # Reference
        self._reference_to = reference_to
        self._is_referenced_by = is_referenced_by
        # Inheritance
        self._herits_of = herits_of
        self._is_herited_by = is_herited_by

    @property
    def name(self):
        return self._name

    @property
    def accessibility(self):
        return self._accessibility

    @property
    def path(self):
        return self.path

    @property
    def attributes(self):
        return self._attributes

    @property
    def methods(self):
        return self._methods

    @property
    def contains(self):
        return self._contains

    @property
    def contained_by(self):
        return self._contained_by

    @property
    def reference_to(self):
        return self._reference_to

    @property
    def is_referenced_by(self):
        return self._is_referenced_by

    @property
    def herits_of(self):
        return self._herits_of

    @property
    def is_herited_by(self):
        return self._is_herited_by

class Package:
    def __init__(self, path = [], classes = [], packages = []):
        self._path = path
        self._classes = classes
        self._packages = packages

    @property
    def path(self):
        return self._path

    @property
    def classes(self):
        return self._classes

    @property
    def packages(self):
        return self._packages
