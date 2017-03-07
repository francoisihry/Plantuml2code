class SmartModel:    def __init__(self, name, path = [],                 contained_classes = [],                 contained_by = None,                 reference_to = [],                 is_referenced_by = [],                 herits_of = [],                 is_herited_by = []                 ):        self._name = name        self._path = path        # Composition        self._contains = contained_classes        self._contained_by =contained_by        # Reference        self._reference_to = reference_to        self._is_referenced_by = is_referenced_by        # Inheritance        self._herits_of = herits_of        self._is_herited_by = is_herited_by    @property    def name(self):        return self._name    @property    def path(self):        return self._path    @property    def contains(self):        return self._contains    @property    def contained_by(self):        return self._contained_by    @property    def reference_to(self):        return self._reference_to    @property    def is_referenced_by(self):        return self._is_referenced_by    @property    def herits_of(self):        return self._herits_of    @property    def is_herited_by(self):        return self._is_herited_by


class SmartModel:
    def __init__(self, name, path = [],
                 contained_classes = [],
                 contained_by = None,
                 reference_to = [],
                 is_referenced_by = [],
                 herits_of = [],
                 is_herited_by = []
                 ):
        self._name = name
        self._path = path
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
    def path(self):
        return self._path

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

