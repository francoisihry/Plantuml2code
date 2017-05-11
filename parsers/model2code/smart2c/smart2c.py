from parsers.model2code.smart2c.c_class import CEnum, CClass

from os.path import join, exists, dirname
from os import makedirs
from parsers.model2code.smart2c import makefile


def pack2c(pack, smart_model):
    for c in pack.classes.values():
        setattr(c,'c_class',CClass(c, smart_model))
    for e in pack.enums.values():
        c_enum = CEnum(e)
        enum_usage = _find_enum_usage(e, pack)
        i=0
        # si l'enum est utilisé dans une seule classe, alors on le déclare
        # dans le .h  de la classe
        if len(enum_usage) == 1:
            enum_usage[0].c_class.add_enum(c_enum)
        else:
        # sinon si on met le c_enum dans le package qui lui generera un .h
            setattr(pack, 'c_enum', c_enum)
        # on associe la definition c de l'enum:
        setattr(e,'c_enum',CEnum(e))
    for c in pack.classes.values():
        c.c_class.gen()
    for p in pack.packages:
        pack2c(p, smart_model)


def write_code(pack, output_path):
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
    for p in pack.packages:
        write_code(p, output_path)


def _write_makefile(smart_model, output_path):
    mf = makefile.gen(smart_model)
    mf_path = join(output_path, 'Makefile')
    with open(mf_path, 'w') as mfile:
        mfile.write(mf)


def smart2c(smart_model, output_path=None):
    pack2c(smart_model, smart_model)
    write_code(smart_model, output_path)
    _write_makefile(smart_model, output_path)


def _find_enum_usage(enum, pack):
    usage=[]
    for c in pack.classes.values():
        class_attr = list(c.methods.values())+ list(c.attributes.values())
        at_usage = [at for at in class_attr if at.type == enum]
        if len(at_usage)>0 :
            usage.append(c)
    for p in pack.packages:
        usage += _find_enum_usage(enum, p)
    return usage






