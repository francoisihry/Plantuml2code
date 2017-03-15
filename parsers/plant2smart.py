from smart_model.smart_model import SmartModel, Class, Accessibility, Package
from smart_model.attribute import Attribute, Method
from textx.metamodel import metamodel_from_file
from os.path import join, dirname
from copy import deepcopy

MM_PLANT = metamodel_from_file(join(dirname(__file__), '../plant_uml_grammar.tx'))
NAMES_SPACES = MM_PLANT.namespaces['plant_uml_grammar']

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
        class_path = deepcopy(p.path)
        class_path.append(c.name)
        p_classes.append(_create_class(c, class_path))
    for pack in p.packages:
        p_packages.append(_create_package(pack))
    return Package(p.path, p_classes, p_packages)



def _create_class( c, path =[]):
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
                 attributes=attributes,
                 path = path)

def _parse_accessibility(visibility):
    accessibitity = {"+":Accessibility.public,
                     "-" : Accessibility.private}
    return accessibitity[visibility]