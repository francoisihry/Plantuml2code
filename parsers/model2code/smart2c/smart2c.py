from smart_model.attribute import Type
from smart_model.model import Class, Enum


class CClass:
    def __init__(self, cl):
        self._class = cl
        self._c_file = ''
        self._h_file = ''
        self.gen_h_class_structure()
        self.gen_h_constructors()
        self.gen_h_methods()
        self.gen_c_constructors()
        self.gen_c_methods()
        i=0

    def gen_h_class_structure(self):
        name = self._class.name
        self._h_file += '/* Class structure */\n'
        self._h_file += 'typedef struct {}\n'.format(name)
        self._h_file += '    {\n'

        for m in self._class.methods.values():
            self_param = 'struct {}*'.format(name)
            params = ', '.join([self_param]+[_parse_type(p.type)+' '+p.name for p in m.parameters])
            self._h_file += '        {}(*{}) ({});\n'.format(_parse_type(m.type), m.name, params)
        self._h_file += '        void(*free)(struct {}*);\n'.format(name)

        self._h_file += '    }} {};\n\n'.format(name)

    def gen_h_constructors(self):
        cons = self._class.constructors[0]
        name = self._class.name
        self._h_file += '/* Constructors */\n'
        self._h_file += '{} {}_create()\n'.format(name, name)
        self._h_file += '{}* {}_new()\n\n'.format(name, name)
        self._h_file += '/* Destructors */\n'
        self._h_file += 'void {}_free({} *self)\n'.format(name, name)
        self._h_file += 'void {}_new_free({} *self)\n\n'.format(name, name)

    def gen_c_constructors(self):
        cons = self._class.constructors[0]
        name = self._class.name
        self._c_file += '/* Constructors */\n'
        # gen create:
        self._c_file += '{} {}_create()\n'.format(name, name)
        self._c_file += '{\n'
        self._c_file += '    {} self;\n'.format(name)
        self._c_file += '    {}_init(&self);\n'.format(name)
        self._c_file += '    self.free = {}_free;\n'.format(name)
        self._c_file += '    return self;\n'
        self._c_file += '}\n\n'
        # gen new:
        self._c_file += '{}* {}_new()\n'.format(name, name)
        self._c_file += '{\n'
        self._c_file += '    {} *self = malloc(sizeof({}));\n'.format(name, name)
        self._c_file += '    if(!self) return NULL;\n'
        self._c_file += '    {}_init(self);\n'.format(name)
        self._c_file += '    self->free = {}_new_free;\n'.format(name)
        self._c_file += '    return self;\n'
        self._c_file += '}\n\n'
        # gen init:
        self._c_file += 'static void {}_init({} *self)\n'.format(name, name)
        self._c_file += '{\n'
        for method_name in self._class.methods.keys():
            self._c_file += '    self->{} = {}_{};\n'.format(method_name, name,method_name)
        self._c_file += '}\n\n'
        # gen destructors:
        self._c_file += '/* Destructors */\n'
        self._c_file += 'void {}_free({} *self)\n'.format(name, name)
        self._c_file += '{\n'
        self._c_file += '    // should be completed considering what the class contains;\n'
        self._c_file += '}\n\n'

        self._c_file += 'void {}_new_free({} *self)\n'.format(name, name)
        self._c_file += '{\n'
        self._c_file += '    if(self) {}_free(self);\n'.format(name)
        self._c_file += '    free(self);\n'
        self._c_file += '}\n\n'


        pass

    def gen_h_methods(self):
        self._h_file += '/* Methods */\n'
        for m in self._class.methods.values():
            params = ', '.join([_parse_type(p.type)+' '+p.name for p in m.parameters])
            self._h_file += '{} {} ({})\n'.format(_parse_type(m.type), m.name, params)

    def gen_c_methods(self):
        self._c_file += '/* Methods */\n'
        for m in self._class.methods.values():
            params = ', '.join([_parse_type(p.type)+' '+p.name for p in m.parameters])
            self._c_file += '{} {} ({})\n'.format(_parse_type(m.type), m.name, params)
            self._c_file += '{\n}\n\n'




class Smart2c:

    def __init__(self, smart_model, output_path=None):
        self._classes = []
        # for e in smart_model.enums.values():
        #     self.gen_enums(e)
        for c in smart_model.classes:
            self._classes.append(CClass(c))
        pass

    def gen_enums(self, e):
        # si l'enum est utilise dans une seule classe, on le met dans le .h de la classe sinon on lui crée
        # son propre .h
        self._h_file += 'typedef enum {{ {} }} {} ;'.format(', '.join(e.labels), e.name)




def _parse_type(t):
        if isinstance(t, Class) or isinstance(t, Enum):
            return t.name
        parse = {
            Type.int : 'int',
            Type.string : 'char*',
            Type.float : 'float',
            Type.void : 'void'
        }
        return parse[t]

