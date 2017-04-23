import os
from smart_model.smart_model import Package



class Header:
    def __init__(self, smart_class):
        self._smart_class = smart_class
    def __str__(self):
        header=''
        for c in self._smart_class.contains:
            header += 'from {} import {}\n'.format(c.module_path, c.name)
        return header

class ClassDef:
    def __init__(self, smart_class):
        self._smart_class = smart_class

    def __str__(self):
        py_class='class {}:\n'.format(self._smart_class.name)
        py_class+='    def __init__(self):\n'
        py_class += '        pass\n'
        return py_class





def _package2py(package):
    for c in package.classes:
        setattr(c, 'module_path', '.'.join(c.path))
        setattr(c, 'header', Header(c))
        setattr(c, 'classe_def', ClassDef(c))
    for p in package.packages:
        _package2py(p)


def _gen_py_from_package(pack, output_path):
    if isinstance(pack, Package):
        init_path = os.path.join(*(output_path+pack.path + ['__init__.py']))

        dir = os.path.dirname(init_path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(init_path, 'w'):
            ...

    for c in pack.classes:
        path = c.make_file_path(output_path)+'.py'
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, 'w') as file:
            file.write(str(c.header))
            file.write("\n\n")
            file.write(str(c.classe_def))
    for p in pack.packages:
        _gen_py_from_package(p, output_path)


def smart2py(smart_model, output_path = []):
    _package2py(smart_model)
    _gen_py_from_package(smart_model, output_path)

