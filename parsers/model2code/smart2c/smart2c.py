from smart_model.attribute import Type
from smart_model.model import Class, Enum

IFDEF_CPP_MACRO_PATTERN = '#ifdef __cplusplus\n' \
                       '    extern "C" {{\n' \
                       '#endif\n\n' \
                       '{}\n\n' \
                       '#ifdef __cplusplus\n' \
                       '}}\n' \
                       '#endif\n'
def c_title(title):
    return '/* {} ===========================' \
           '============================= */\n'.format(title)

def h_title(title):
    return '/* {} */\n'.format(title)

class CClass:
    def __init__(self, cl):
        self._class = cl
        self._c_file = ''
        self._h_file = ''
        self._h_file_name = '{}.h'.format(cl.file_name)
        self._c_file_name = '{}.c'.format(cl.file_name)
        self._c_enums =[]

    def gen(self):

        self._gen_h_enums()
        self._gen_h_class_structure()
        self._gen_h_constructors()
        self._gen_h_methods()
        self._gen_h_ifdef_cpp_macro()
        self._gen_h_ifndef_file()
        self._gen_h_header()


        self._gen_c_incude()
        self._gen_c_constructors()
        self._gen_c_methods()
        self._gen_c_header()

    def _gen_h_header(self):
        header = '/*\n'
        header += ' * {}\n'.format(self._h_file_name)
        header += ' */\n\n'
        self._h_file = header + self._h_file

    def _gen_c_header(self):
        header = '/*\n'
        header += ' * {}\n'.format(self._c_file_name)
        header += ' */\n\n'
        self._c_file = header + self._c_file

    def _gen_c_incude(self):
        self._c_file += '#include <stdlib.h>\n'
        self._c_file += '#include <stdio.h>\n\n'

        self._c_file += '#include "{}"\n\n'.format(self._h_file_name)

    def _gen_h_class_structure(self):
        name = self._class.name
        self._h_file += h_title('class structure')
        self._h_file += 'typedef struct {}\n'.format(name)
        self._h_file += '    {\n'

        for m in self._class.methods.values():
            self_param = 'struct {}*'.format(name)
            params = ', '.join([self_param]+[_parse_type(p.type)+' '+p.name for p in m.parameters])
            self._h_file += '        {}(*{}) ({});\n'.format(_parse_type(m.type), m.name, params)
        self._h_file += '        void(*free)(struct {}*);\n'.format(name)

        self._h_file += '    }} {};\n\n'.format(name)

    def _gen_h_constructors(self):
        cons = self._class.constructors[0]
        name = self._class.name
        self._h_file += h_title('constructors')
        self._h_file += '{} {}_create();\n'.format(name, name)
        self._h_file += '{}* {}_new();\n\n'.format(name, name)
        self._h_file += h_title('destructors')
        self._h_file += 'void {}_free({} *self);\n'.format(name, name)
        self._h_file += 'void {}_new_free({} *self);\n\n'.format(name, name)

    def _gen_c_constructors(self):
        cons = self._class.constructors[0]
        name = self._class.name

        init_met_name = '{}_init'.format(name)
        self._c_file += 'static {0}* {1}({0}*);\n\n'.format(name, init_met_name)
        self._c_file += c_title('constructors')
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
        self._c_file += c_title('destructors')
        self._c_file += 'void {}_free({} *self)\n'.format(name, name)
        self._c_file += '{\n'
        self._c_file += '    /* should be completed considering what the class contains */\n'
        self._c_file += '}\n\n'

        self._c_file += 'void {}_new_free({} *self)\n'.format(name, name)
        self._c_file += '{\n'
        self._c_file += '    if(self) {}_free(self);\n'.format(name)
        self._c_file += '    free(self);\n'
        self._c_file += '}\n\n'


        pass

    def _gen_h_methods(self):
        self._h_file += h_title('methods')
        for m in self._class.methods.values():
            params = ', '.join([_parse_type(p.type)+' '+p.name for p in m.parameters])
            method_name = '{}_{}'.format(self._class.name, m.name)
            self._h_file += '{} {} ({});\n'.format(_parse_type(m.type), method_name, params)

    def _gen_c_methods(self):
        self._c_file += c_title('methods')
        for m in self._class.methods.values():
            params = ', '.join([_parse_type(p.type)+' '+p.name for p in m.parameters])
            method_name = '{}_{}'.format(self._class.name,m.name)
            self._c_file += '{} {} ({})\n'.format(_parse_type(m.type), method_name, params)
            self._c_file += '{\n}\n\n'

    def _gen_h_enums(self):
        self._h_file += h_title('enumerations')
        for e in self._c_enums:
            self._h_file += '{}'.format(e.h_file)
        self._h_file += '\n\n'

    def add_enum(self, c_enum):
        self._c_enums.append(c_enum)

    def _gen_h_ifndef_file(self):
        name = '{}_H_'.format(self._class.name.upper())
        self._h_file = '#ifndef {0}\n' \
                       '#define {0}\n\n' \
                       '{1}\n' \
                       '#endif /* {0} */'.format(name, self._h_file)

    def _gen_h_ifdef_cpp_macro(self):
        self._h_file = IFDEF_CPP_MACRO_PATTERN.format(self._h_file)

class CEnum:
    def __init__(self, enum):
        self._enum = enum
        labels = ',\n        '.join(enum.labels)
        self.should_have_its_own_file = False
        self.h_file = 'typedef enum \n    {{\n        {}\n    }} {} ;'.format(labels, enum.name)

class Smart2c:

    def __init__(self, smart_model, output_path=None):
        self._classes = []
        # for e in smart_model.enums.values():
        #     self.gen_enums(e)
        for c in smart_model.classes:
            setattr(c,'c_class',CClass(c))
        for e in smart_model.enums.values():
            c_enum = CEnum(e)
            enum_usage = self._find_enum_usage(e, smart_model)
            i=0
            # si l'enum est utilisé dans une seule classe, alors on le déclare
            # dans le .h  de la classe
            if len(enum_usage) == 1:
                enum_usage[0].c_class.add_enum(c_enum)
            else:
            # sinon si on indique qu'un fichier devra etre cree pour l'enum
                c_enum.should_have_its_own_file = True
            # on associe la definition c de l'enum:
            setattr(e,'c_enum',CEnum(e))
        for c in smart_model.classes:
            c.c_class.gen()






        pass

    def _find_enum_usage(self, enum, pack):
        usage=[]
        for c in pack.classes:
            class_attr = list(c.methods.values())+ list(c.attributes.values())
            at_usage = [at for at in class_attr if at.type == enum]
            if len(at_usage)>0 :
                usage.append(c)
        for p in pack.packages:
            usage += self._find_enum_usage(enum, p)
        return usage




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

