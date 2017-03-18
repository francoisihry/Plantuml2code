from smart_model.smart_model import SmartModel, Class, Accessibility, Package
from smart_model.attribute import Attribute, Method
from textx.metamodel import metamodel_from_file
from os.path import join, dirname
from copy import deepcopy
import re

MM_PLANT = metamodel_from_file(join(dirname(__file__), '../plant_uml_grammar.tx'))
NAMES_SPACES = MM_PLANT.namespaces['plant_uml_grammar']

def plant2smart(plant):
    smart_model = SmartModel()
    for c in plant.classes:
        smart_model.classes.append(_create_class(c))
    for p in plant.packages:
        smart_model.packages.append(_create_package(p))
    for r in plant.relations:
        if isinstance(r, NAMES_SPACES['Composition']):
            _add_composition(r, smart_model)
    return smart_model


def _add_composition(compo,smart_model):
    contenu = compo.contenu[0]
    contenant = compo.contenant[0]
    match_contenu = smart_model.find_classes_by_name(contenu.name)
    match_contenant = smart_model.find_classes_by_name(contenant.name)
    if len(match_contenant) == 1 and len(match_contenu) == 1 :
        class_contenant = match_contenant[0]
        class_contenu = match_contenu[0]
        class_contenant.contains.append(class_contenu)
        class_contenu.contained_by = class_contenant

    else:
        raise Exception("probleme soit il ne trouve pas les contenus/contenants."
                        "Soit il en trouve plus que 1")


def _create_package(p, path=[]):
    p_classes=[]
    p_packages=[]
    for c in p.classes:
        class_path = deepcopy(p.path)
        class_path.append(_to_snake_case(c.name))
        p_classes.append(_create_class(c, path + class_path))
    for pack in p.packages:
        pack_path = deepcopy(p.path)
        p_packages.append(_create_package(pack, path + pack_path))
    return Package(path + p.path, p_classes, p_packages)

def _to_snake_case(camel_case):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_case)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


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