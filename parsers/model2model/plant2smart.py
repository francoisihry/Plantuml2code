from smart_model.model import SmartModel, Class, Visibility, Package, Relation
from smart_model.attribute import Attribute, Method, Parameter, Access
from textx.metamodel import metamodel_from_file
from os.path import join, dirname


MM_PLANT = metamodel_from_file(join(dirname(__file__), '../../plant_uml_grammar.tx'))
NAMES_SPACES = MM_PLANT.namespaces['plant_uml_grammar']

def plant2smart(plant):
    smart_model = SmartModel()
    for c in plant.classes:
        smart_model.classes.append(_create_class(c, None))
    for p in plant.packages:
        smart_model.packages.append(_create_package(p))
    for r in plant.relations:
        _add_relation(r, smart_model)
    return smart_model

class Range:
    def __init__(self, plant_range):
        if len(plant_range):
            plant_range = plant_range[0]
            if len(plant_range) == 1:
                parsed = self._parse(plant_range[0])
                if plant_range =='*':
                    self.min = 0
                    self.max = parsed
                else:
                    self.min = parsed
                    self.max = parsed
            else:
                self.min = self._parse(plant_range[0])
                self.max = self._parse(plant_range[3])
        else:
            self.min = None
            self.max = None

    def _parse(self, char):
        if char == '*':
            return float('inf')
        else:
            return int(char)


def _add_relation(rel, smart_model):
        contenu = rel.contenu[0]
        contenant = rel.contenant[0]
        class_contenu_range = Range(rel.range_contenu)
        class_contenant_range = Range(rel.range_contenant)
        match_contenu = smart_model.find_classes_by_name(contenu.name)
        match_contenant = smart_model.find_classes_by_name(contenant.name)
        if len(match_contenant) == 1 and len(match_contenu) == 1 :
            class_contenant = match_contenant[0]
            class_contenu = match_contenu[0]
        else:
            raise Exception("probleme soit il ne trouve pas les contenus/contenants."
                            "Soit il en trouve plus que 1")
        if isinstance(rel, NAMES_SPACES['Composition']):
            contenant_contient = class_contenant.contains
            contenu_contenu_par = class_contenu.contained_by
        elif isinstance(rel, NAMES_SPACES['Heritage']):
            contenant_contient = class_contenant.is_herited_by
            contenu_contenu_par = class_contenu.herits_of
        if len(rel.label)==1:
            label = rel.label[0]
        else:
            label = None
        contenant_contient.append(Relation(class_contenu,
                                           class_contenu_range.min,
                                           class_contenu_range.max,
                                           label = label)
                                  )
        contenu_contenu_par.append(Relation(class_contenant,
                                            class_contenant_range.min,
                                            class_contenant_range.max,
                                            label = label)
                                   )

def _create_package(p):
    classes = [_create_class(c, p ) for c in p.classes]
    packages = [_create_package(pack) for pack in p.packages]
    return Package(p.path, classes, packages)


def _create_class( c, container):
    attributes = []
    for at in c.attributes:
        name = at.name
        type = at.type
        visibility =_parse_visibility(at.visibility)
        access = _parse_access(at.access)
        if isinstance(at,NAMES_SPACES['Value']):
            attributes.append(Attribute(name, type=type,
                                     visibility=visibility,
                                        access=access))
        else:
            params = [Parameter(p.name, p.type) for p in at.params]
            attributes.append(Method(name, type=type, visibility=visibility,
                                     parameters=params,
                                        access=access))


    return Class(c.name,
                 attributes=attributes,
                 pack_container=container)

def _parse_visibility(visibility):
    accessibitity = {"+":Visibility.public,
                     "-" : Visibility.private}
    return accessibitity[visibility]

def _parse_access(visibility):
    accessibitity = {"{static}":Access.static,
                     "{abstract}" : Access.abstract,
                     None:None}
    return accessibitity[visibility]