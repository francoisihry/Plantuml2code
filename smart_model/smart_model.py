from os.path import join
import re
import copy

class SmartModel:
    def __init__(self, classes=None, packages=None):
        if classes:
            self._classes = classes
        else:
            self._classes = []
        if packages:
            self._packages = packages
        else:
            self._packages =[]


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


class Accessibility:
    (public,
     private,
     protected,
     static
    ) = range(4)

def _to_snake_case(camel_case):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class Class:
    def __init__(self, name,
                 accessibility=Accessibility.public,
                 attributes = None,
                 methods = None,
                 contains = None,
                 contained_by = None,
                 reference_to = None,
                 is_referenced_by = None,
                 herits_of = None,
                 is_herited_by = None,
                 pack_container = None
                 ):
        self._name = name
        self._file_name = _to_snake_case(name)

        self._accessibility = accessibility
        self._pack_container = pack_container
        # if path:
        #     self._path = path
        # else:
        #     self._path = []
        # self._path.append(_to_snake_case(self._name))
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


    def __str__(self):
        return 'Class {}'.format(self._name)

    def make_file_path(self, output_path):
        return join(*(output_path+self.path))

    @property
    def name(self):
        return self._name

    @property
    def pack_container(self):
        return self._pack_container

    @pack_container.setter
    def pack_container(self, c):
        self._pack_container = c

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, fn):
        self._file_name = fn

    @property
    def accessibility(self):
        return self._accessibility

    @property
    def path(self):
        if self.pack_container:
            path = self.pack_container.path
        else:
            path=[]
        return path+[self.file_name]

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
    def __init__(self, path , classes = None, packages = None, container = None):
        self._container = container
        self._name = path[0]

        self._classes = []
        self._packages = []
        if len(path) == 1:

            if classes:
                for c in classes:
                    self._add_class(c)
            if packages:
                for p in packages:
                    self._add_package(p)
            else:
                self._packages = []
        else:
            self._packages = [Package( path = [path[i] for i in range(1,len(path))],
                                       classes=classes,
                                       packages=packages,
                                       container=self)
                                  ]



    def __str__(self):
        return 'Package {}'.format(self._name)


    def _add_class(self, c):
        self._classes.append(c)
        c.pack_container = self

    def _add_package(self, p):
        self._packages.append(p)
        p.container = self


    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, c):
        self._container = c


    @property
    def path(self):
        cont = self.container
        path = []
        while cont is not None:
            path.insert(0, cont.name)
            cont = cont.container
        path.append(self._name)
        return path

    @property
    def name(self):
        return self._name


    @property
    def classes(self):
        return self._classes

    @property
    def packages(self):
        return self._packages
