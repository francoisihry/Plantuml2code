from smart_model.model import SmartModel, Class, Visibility, Package, Relation, Enum
from smart_model.attribute import Attribute, Method, Parameter, Access, Type
from textx.metamodel import metamodel_from_file
from os.path import join, dirname


MM_PLANT = metamodel_from_file(join(dirname(__file__), '../../plant_uml_grammar.tx'))
NAMES_SPACES = MM_PLANT.namespaces['plant_uml_grammar']


def plant2smart(plant):
    smart_model = SmartModel()
    for c in plant.classes:
        smart_model.classes[c.name] = _create_class(c, None, smart_model)
    for enum in plant.enums:
        smart_model.enums[enum.name] = Enum(enum.name, enum.labels,smart_model)
    for p in plant.packages:
        smart_model.packages.append(_create_package(p, smart_model))
    for r in plant.relations:
        _add_relation(r, smart_model)
    # add type : must be done at the end so that it can link to existing class
    _add_types(plant, smart_model)

    return smart_model

class Range:
    def __init__(self, plant_range):
        if plant_range is not None:
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
        contenu = rel.contenu
        contenant = rel.contenant
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

def _create_package(p, smart_model):
    classes = [_create_class(c, p , smart_model) for c in p.classes]
    enums = {e.name : Enum(e.name, e.labels, p) for e in p.enums}
    packages = [_create_package(pack, smart_model) for pack in p.packages]
    return Package(p.path, classes, packages, enums=enums)

def _add_types(plant, smart_model):
    for plant_class in plant.classes:
        smart_class = plant_class.smart_class
        for plant_at in plant_class.attributes:
            if isinstance(plant_at,NAMES_SPACES['ValueWithType']):
                smart_at = smart_class.attributes[plant_at.name]
                smart_at.type = _parse_type(plant_at.type, smart_model)
            elif not isinstance(plant_at,NAMES_SPACES['ValueWithoutType']):
                if plant_at.name == plant_class.name:
                    smart_at = smart_class.constructors[0]
                else:
                    smart_at = smart_class.methods[plant_at.name]
                for i in range(0, len(plant_at.params)):
                    plant_param = plant_at.params[i]
                    smart_param = smart_at.parameters[i]
                    if hasattr(plant_param, 'type'):
                        p_type = _parse_type(plant_param.type, smart_model)
                    else:
                        p_type = None
                    smart_param.type = p_type
                if isinstance(plant_at,NAMES_SPACES['MethodWithType']) :
                    smart_at.type = _parse_type(plant_at.type, smart_model)
    for p in plant.packages:
        _add_types(p, smart_model)



def _create_class( c, container, smart_model):
    attributes = []
    for at in c.attributes:
        name = at.name
        # type = _parse_type(at.type)
        visibility =_parse_visibility(at.visibility)
        access = _parse_access(at.access)
        if isinstance(at,NAMES_SPACES['ValueWithType']) or  isinstance(at,NAMES_SPACES['ValueWithoutType']):
            attributes.append(Attribute(name,
                                     visibility=visibility,
                                        access=access))
        else:
            params=[]
            for p in at.params:
                params.append(Parameter(p.name))
            attributes.append(Method(name,  visibility=visibility,
                                     parameters=params,
                                        access=access))


    smart_cl = Class(c.name,
                 attributes=attributes,
                 pack_container=container)
    setattr(c, 'smart_class', smart_cl)
    return smart_cl

def _parse_type(_type, smart_model):
    parse = {"int":Type.int,
                  "Int":Type.int,
                  "float" : Type.float,
                  "Float" : Type.float,
                  "str" : Type.string,
                  "Str" : Type.string,
                  "String" : Type.string,
                  "void" : Type.void,
                  "Void" : Type.void,
                  None:None
                  }
    if _type in parse.keys():
        return parse[_type]
    enum_names = _make_enum_names_dictionnary(smart_model)
    if _type in enum_names.keys():
        return enum_names[_type]
    class_names = _make_class_names_dictionnary(smart_model)
    if _type in class_names.keys():
        return class_names[_type]
    else:
        raise Exception('Unable to parse {} type'.format(_type))


def _make_class_names_dictionnary(pack):
    class_list = pack.classes.items()
    for p in pack.packages:
        class_list += p.classes.items()
    return dict(class_list)

def _make_enum_names_dictionnary(pack):
    enums = {e:pack.enums[e] for e in pack.enums.keys()}
    for p in pack.packages:
        for e in p.enums.keys():
            enums[e] = p.enums[e]
    return enums

def _parse_visibility(visibility):
    accessibitity = {"+":Visibility.public,
                     "-" : Visibility.private}
    return accessibitity[visibility]

def _parse_access(visibility):
    accessibitity = {"{static}":Access.static,
                     "{abstract}" : Access.abstract,
                     None:None}
    return accessibitity[visibility]