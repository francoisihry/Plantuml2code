from enum   import Enum
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

    @property
    def packages(self):
        return self._packages

    @property
    def classes(self):
        return self._classes

    def find_classes_by_name(self, name):
        return self._find_classes_in_pack_by_name(self,name)

    @staticmethod
    def _find_classes_in_pack_by_name(pack, name):
        class_list = [c for c in pack.classes if c.name == name]
        for pack in pack.packages:
            class_list += SmartModel._find_classes_in_pack_by_name(pack, name)
        return class_list

Accessibility = Enum("Accessibility",["public", "private", "protected", "static"])


class Class:
    def __init__(self, name,
                 accessibility = Accessibility.public,
                 path = None,
                 attributes = None,
                 methods = None,
                 contains = None,
                 contained_by = None,
                 reference_to = None,
                 is_referenced_by = None,
                 herits_of = None,
                 is_herited_by = None
                 ):
        self._name = name
        self._accessibility = accessibility
        if path:
            self._path = path
        else:
            self._path = []
            # Attributes
        if attributes:
            self._attributes = attributes
        else:
            self._attributes = []
        if methods:
            self._methods = methods
        else:
            self._methods = []
        # Composition
        if contains:
            self._contains = contains
        else:
            self._contains = []
        self._contained_by = contained_by

        # Reference
        if reference_to:
            self._reference_to = reference_to
        else:
            self._reference_to = []
        if is_referenced_by:
            self._is_referenced_by = is_referenced_by
        else:
            self._is_referenced_by = []
        # Inheritance
        if herits_of:
            self._herits_of = herits_of
        else:
            self._herits_of = []
        if is_herited_by:
            self._is_herited_by = is_herited_by
        else:
            self._is_herited_by = []

    @property
    def name(self):
        return self._name

    @property
    def accessibility(self):
        return self._accessibility

    @property
    def path(self):
        return self._path

    @property
    def attributes(self):
        return self._attributes

    @property
    def methods(self):
        return self._methods

    @property
    def contains(self):
        return self._contains

    @contains.setter
    def contains(self, cl):
        self._contains.append(cl)

    @property
    def contained_by(self):
        return self._contained_by

    @contained_by.setter
    def contained_by(self, cl):
        self._contained_by = cl

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
