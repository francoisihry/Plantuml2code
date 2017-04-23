import os
from smart_model.smart_model import SmartModel



class Header:
    def __init__(self, smart_class):
        self._smart_class = smart_class
    def __str__(self):
        header=''
        for c in self._smart_class.contains:
            header += 'from {} import {}\n'.format(c.module_path, c.name)
        return header


def _package2py(package):
    for c in package.classes:
        c.extension = '.py'
        setattr(c, 'module_path', '.'.join(c.path))
        setattr(c, 'header', Header(c))

def _smart_model2py_model(smart_model):
    _package2py(smart_model)
    for p in smart_model.packages:
        _package2py(p)

def _gen_py_from_package(pack, output_path):
    for c in pack.classes:
        path = c.make_file_path(output_path)
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, 'w') as file:
            file.write(str(c.header))
    for p in pack.packages:
        _gen_py_from_package(p, output_path)

def _gen_py_from_model(smart_model, output_path):
    _gen_py_from_package(smart_model, output_path)
    for p in smart_model.packages:
        _gen_py_from_package(p, output_path)

def smart2py(smart_model, output_path = []):
    _smart_model2py_model(smart_model)

    init_path = os.path.join(*(output_path + ['__init__.py']))
    dir = os.path.dirname(init_path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(init_path, 'w'):
        ...

    _gen_py_from_model(smart_model, output_path)

