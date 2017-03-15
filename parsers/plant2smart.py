from smart_model.smart_model import SmartModel, Class, Accessibility, Package
from smart_model.attribute import Attribute, Method
from plant2py import NAMES_SPACES

def plant2smart(plant):
    smart_model = SmartModel()
    for c in plant.classes:
        smart_model.classes.append(_create_class(c))
    for p in plant.packages:
        smart_model.packages.append(_create_package(p))
    return smart_model


def _create_package( p):
    p_classes=[]
    p_packages=[]
    for c in p.classes:
        p_classes.append(_create_class(c))
    for pack in p.packages:
        p_packages.append(_create_package(pack))
    return Package(p.path, p_classes, p_packages)



def _create_class( c):
    attributes = []
    for at in c.attributes:
        name = at.name
        accesibility =_parse_accessibility(at.visibility)
        if isinstance(at,NAMES_SPACES['Value']):
            attributes.append(Attribute(name,
                                     accessibility=accesibility))
        else:
            attributes.append(Method(name, accessibility=accesibility))


    return Class(c.name,
                 attributes=attributes)

def _parse_accessibility(visibility):
    accessibitity = {"+":Accessibility.public,
                     "-" : Accessibility.private}
    return accessibitity[visibility]