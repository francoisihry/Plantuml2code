from parsers.model2code.smart2c.c_class import CEnum, CClass

from os.path import join, exists, dirname
from os import makedirs
from parsers.model2code.smart2c import makefile
from smart_model.model import Enum

def smart2c_class(pack, smart_model):
    for c in pack.classes.values():
        setattr(c,'c_class',CClass(c, smart_model))
    for p in pack.packages:
        smart2c_class(p, smart_model)

def enum_ref(pack, smart_model):
    for e in pack.enums.values():
        c_enum = CEnum(e)
        enum_usage = _find_enum_usage(smart_model, e)
        # si l'enum est utilisé dans une seule classe, alors on le déclare
        # dans le .h  de la classe
        if len(enum_usage) == 1:
            c_enum.should_have_its_own_file = False
            enum_usage[0].c_class.add_enum(c_enum)
        else:
            c_enum.should_have_its_own_file = True
        # sinon si on ajoute une reference dans chaque classe le contenant
        # et on precise dans l'enum qu'il doit etre write dans sont propre .h
            [c.c_class.add_enum(c_enum) for c in enum_usage]
        # on associe la definition c de l'enum:
        setattr(e,'c_enum',c_enum)
    for p in pack.packages:
        enum_ref(p, smart_model)

def pack2c(pack, smart_model):
    for c in pack.classes.values():
        c.c_class.gen()
    for p in pack.packages:
        pack2c(p, smart_model)


def write_code(pack, output_path):
    # writting classes:
    for c in pack.classes.values():
        c_path = join(output_path, c.c_class.path_c)
        h_path = join(output_path, c.c_class.path_h)
        c_dir = dirname(c_path)
        if not exists(c_dir):
            makedirs(c_dir)
        with open(c_path, 'w') as c_file:
            c_file.write(c.c_class.c_file)
        h_dir = dirname(h_path)
        if not exists(h_dir):
            makedirs(h_dir)
        with open(h_path, 'w') as h_file:
            h_file.write(c.c_class.h_file)
    # writting enums:
    enums = [e for e in pack.enums.values() if e.c_enum.should_have_its_own_file]
    for e in enums:
        h_path = join(output_path, e.c_enum.path_h)
        h_dir = dirname(h_path)
        if not exists(h_dir):
            makedirs(h_dir)
        with open(h_path, 'w') as h_file:
            h_file.write(e.c_enum.h_file)
    for p in pack.packages:
        write_code(p, output_path)


def _write_makefile(smart_model, output_path):
    mf = makefile.gen(smart_model)
    mf_path = join(output_path, 'Makefile')
    with open(mf_path, 'w') as mfile:
        mfile.write(mf)


def smart2c(smart_model, output_path=None):
    smart2c_class(smart_model, smart_model)
    enum_ref(smart_model, smart_model)
    pack2c(smart_model, smart_model)
    write_code(smart_model, output_path)
    _write_makefile(smart_model, output_path)


def _find_enum_usage(pack, enum):
    enum_usage = []
    for c in pack.classes.values():
        enum_needs = CClass._find_inclusion_needs(c, Enum)
        if enum in enum_needs and c not in enum_usage:
            enum_usage.append(c)
    for p in pack.packages:
        enum_usage += _find_enum_usage(p, enum)
    return enum_usage



