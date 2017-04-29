import os

from tools.todo import todo
from smart_model.attribute import Visibility, Access
from smart_model.model import Package, to_snake_case


class Header:
    def __init__(self, smart_class):
        self._smart_class = smart_class
    def gen(self):
        header=''
        for c in self._smart_class.contains+self._smart_class.herits_of:
            header += 'from {} import {}\n'.format(c.ref.module_path, c.ref.name)
        return header



class ClassDef:
    def __init__(self, smart_class):
        self._smart_class = smart_class
        self._params = 'self'
        if len(smart_class.constructors)==1:
            constructor=smart_class.constructors[0]
            self._params += ', '+', '.join([p.name for p in constructor.parameters])
        self._inhertited_class = ''
        if len(smart_class.herits_of)>0:
            self._inhertited_class += ' ('
            self._inhertited_class += ', '.join([c.ref.name for c in self._smart_class.herits_of])
            self._inhertited_class += ')'

    def gen(self):
        py_class='class {}{}:\n'.format(self._smart_class.name, self._inhertited_class)
        py_class+='    def __init__({}):\n'.format(self._params)
        content = self._gen_contained()
        content += self._gen_attributes()

        if content == '':
            py_class += '        pass\n'
        else:
            py_class += content
        py_class += self._gen_methods()
        return py_class

    def _gen_contained(self):
        contained_generated = ''
        for c in self._smart_class.contains:
            if c.label:
                label = c.label
            else:
                label = to_snake_case(c.ref.name)
                if c.max > 1:
                    label += 's'

            if len(c.ref.constructors)==1:
                params = [p.name for p in c.ref.constructors[0].parameters]

                constructor = c.ref.name +'('+', '.join([p+'=None' for p in params])+')'
            else:
                params = ''
                constructor = c.ref.name + '()'
            if c.max == 1 and c.min == 1:
                contained_generated+= todo('        # ' + 'TODO define the '
                                                          'parameters : {}\n'.format(' ,'.join(params)))
                contained_generated+= '        self.{} = {}\n'.format(label,constructor)
            else:
                todo_add_elements = '        # TODO you should add {} elements in the list'.format(c.ref.name)
                if c.max != float('inf'):
                    todo_add_elements += ' up to {} elements'.format(c.max)
                todo_add_elements+='\n'
                contained_generated += todo(todo_add_elements)
                contained_generated+= '        self.{} = []\n'.format(label)
        return contained_generated

    def _gen_attributes(self):
        attributes_generated = ''
        for at in self._smart_class.attributes.values():
            if at.visibility is not Visibility.public:
                at_name = '_' + at.name
            else:
                at_name = at.name
            attributes_generated += '        self.{} = None\n'.format(at_name)
        return attributes_generated
    
    def _gen_methods(self):
        methods_generated = ''
        for met in self._smart_class.methods.values():
            methods_generated += '\n'
            decorator =''
            params = 'self, '+', '.join(p.name for p in met.parameters)
            if met.access == Access.static:
                decorator += '    @staticmethod\n'

            if met.visibility is not Visibility.public:
                met_name = '_' + met.name
            else:
                met_name = met.name
            methods_generated += decorator
            methods_generated += '    def {}({}):\n'.format(met_name, params)
            methods_generated += todo('        # TODO : Complete method content\n')
            methods_generated += '        pass\n'
        return methods_generated



def _package2py(package):
    for c in package.classes.values():
        setattr(c, 'module_path', '.'.join(c.path+[c.file_name]))
        setattr(c, 'header', Header(c))
        setattr(c, 'classe_def', ClassDef(c))
    for p in package.packages:
        _package2py(p)


def _gen_py_from_package(pack, output_path):
    if isinstance(pack, Package):
        init_path = os.path.join(output_path,os.path.join(*(pack.path + ['__init__.py'])))

        dir = os.path.dirname(init_path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(init_path, 'w'):
            ...

    for c in pack.classes.values():
        path = c.make_file_path(output_path)+'.py'
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, 'w') as file:
            file.write(c.header.gen())
            file.write("\n\n")
            file.write(c.classe_def.gen())
    for p in pack.packages:
        _gen_py_from_package(p, output_path)


def smart2py(smart_model, output_path=[]):
    _package2py(smart_model)
    _gen_py_from_package(smart_model, output_path)

