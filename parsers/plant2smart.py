from smart_model.smart_model import SmartModel, Class, Accessibility, Package
from smart_model.attribute import Attribute, Method

class Plant2Smart:
    def __init__(self, plant, names_spaces):
        self._plant = plant
        self._names_spaces = names_spaces
        self._smart_model = SmartModel()

        self._classes= []
        self._packages = []

        self._parse()

    @property
    def classes(self):
        return self._classes

    def _parse(self):
        for c in self._plant.classes:
            self._classes.append(self._create_class(c))
        for p in self._plant.packages:
            self._packages.append(self._create_package(p))


    def _create_package(self, p):
        p_classes=[]
        p_packages=[]
        for c in p.classes:
            p_classes.append(self._create_class(c))
        for pack in p.packages:
            p_packages.append(self._create_package(pack))
        return Package(p.path, p_classes, p_packages)



    def _create_class(self, c):
        attributes = []
        for at in c.attributes:
            name = at.name
            accesibility = self._parse_accessibility(at.visibility)
            if isinstance(at, self._names_spaces['Value']):
                attributes.append(Attribute(name,
                                         accessibility=accesibility))
            else:
                attributes.append(Method(name, accessibility=accesibility))


        return Class(c.name,
                     attributes=attributes)

    def _parse_accessibility(self,visibility):
        accessibitity = {"+":Accessibility.public,
                         "-" : Accessibility.private}
        return accessibitity[visibility]