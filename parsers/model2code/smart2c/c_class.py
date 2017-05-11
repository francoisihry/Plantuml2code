from smart_model.attribute import Type
from smart_model.model import Class, Enum
from tools.warning import warning
from os.path import join

INDENT = '   '
IFDEF_CPP_MACRO_PATTERN = '#ifdef __cplusplus\n' \
                       '    extern "C" {{\n' \
                       '#endif\n\n' \
                       '{}\n' \
                       '#ifdef __cplusplus\n' \
                       '}}\n' \
                       '#endif\n'
def c_title(title):
    return '/* {} ===========================' \
           '============================= */\n'.format(title)

def h_title(title):
    return '/* {} */\n'.format(title)




class CClass:
    def __init__(self, cl, smart_model):
        self._smart_model = smart_model
        self._class = cl
        self._c_file = ''
        self._h_file = ''
        self._vtable_name = '_{}VirtualTable'.format(self._class.name)
        self._h_file_name = '{}.h'.format(cl.file_name)
        self._c_file_name = '{}.c'.format(cl.file_name)

        self._c_enums =[]
        if len(self._class.constructors)>0:
            self._h_constructor_params = ', '.join([_parse_param_type(p)
                                        for p in self._class.constructors[0].parameters])
            self._c_constructor_params = ', '.join([_parse_param_type(p) + ' ' + p.name
                                                    for p in self._class.constructors[0].parameters])
        else :
            self._h_constructor_params = ''
            self._c_constructor_params = ''
        self._c_vtable_inst_name = 'VTABLE'
        self._vtable_ref_name = 'vtable'
        self._vtable_name = self._class.name.lower() + '_vtable_t'
        self._free_name = self._class.name+'_free'
        self._free_new_name = self._class.name + '_new_free'
        for m in self._class.methods.values():
            method_name = '{}_{}'.format(self._class.name,m.name)
            setattr(m, 'c_name', method_name)

    @staticmethod
    def make_h_file_name(smart_class):
        return  '{}.h'.format(smart_class.file_name)

    @staticmethod
    def make_c_file_name(smart_class):
        return '{}.c'.format(smart_class.file_name)

    @staticmethod
    def make_h_path(smart_class):
        return join(*(smart_class.path + [CClass.make_h_file_name(smart_class)]))

    @staticmethod
    def make_c_path(smart_class):
        return join(*(smart_class.path + [CClass.make_c_file_name(smart_class)]))

    @property
    def path_h(self):
        return self.make_h_path(self._class)

    @property
    def path_c(self):
        return self.make_c_path(self._class)

    @property
    def c_file(self):
        return self._c_file

    @property
    def h_file(self):
        return self._h_file

    @property
    def c_file_name(self):
        return self.make_c_file_name(self._class)

    def gen(self):

        self._gen_h_include()
        self._gen_h_enums()
        self._gen_h_class_structure()
        self._gen_h_v_table()
        self._gen_h_constructors()
        self._gen_h_methods()
        self._gen_h_ifdef_cpp_macro()
        self._gen_h_ifndef_file()
        self._gen_h_header()

        self._gen_c_incude()
        self._gen_c_init_prototype()
        self._gen_c_v_table()
        self._gen_c_constructors()
        self._gen_c_init()
        self._gen_c_destructors()
        self._gen_c_methods()
        self._gen_c_header()


    def _gen_c_header(self):
        header = '/*\n'
        header += ' * {}\n'.format(self._c_file_name)
        header += ' */\n\n'
        self._c_file = header + self._c_file

    def _gen_c_incude(self):
        self._c_file += '#include <stdlib.h>\n'
        self._c_file += '#include <stdio.h>\n\n'

        self._c_file += '#include "{}"\n\n'.format(self._h_file_name)

    def _gen_c_init_prototype(self):
        params = ', '.join([self._class.name+'*',self._h_constructor_params])
        init_met_name = '{}_init'.format(self._class.name)
        self._c_file += 'static void {0}({1});\n\n'.format(init_met_name, params)


    def _gen_c_v_table(self):
        self._c_file += c_title('virtual table')
        self._c_file += '{} {} = {{\n'.format(self._vtable_name, self._c_vtable_inst_name)
        self._c_file += INDENT + self._free_name+',\n'
        for m in self._class.methods.values():
            self._c_file += INDENT + '{},\n'.format(m.c_name)
        self._c_file += '};\n\n'


    def _gen_c_constructors(self):
        self._c_file += c_title('constructors')
        name = self._class.name
        init_params_create = '&self'
        init_params_new = 'self'
        if len(self._class.constructors) > 0:
            init_params_create = ', '.join([init_params_create]+[p.name for p in self._class.constructors[0].parameters])
            init_params_new = ', '.join([init_params_new] + [p.name for p in self._class.constructors[0].parameters])

        # gen create:
        self._c_file += '{0} {0}_create({1})\n'.format(name, self._c_constructor_params)
        self._c_file += '{\n'
        self._c_file += INDENT + '{} self;\n'.format(name)
        self._c_file += INDENT + 'self.{} =  &{};\n'.format(self._vtable_ref_name, self._c_vtable_inst_name)
        self._c_file += INDENT + '{}_init({});\n'.format(name, init_params_create)
        self._c_file += INDENT + 'return self;\n'
        self._c_file += '}\n\n'
        # gen new:
        self._c_file += '{0}* {0}_new({1})\n'.format(name, self._c_constructor_params)
        self._c_file += '{\n'
        self._c_file += INDENT + '{} *self = malloc(sizeof({}));\n'.format(name, name)
        self._c_file += INDENT + 'if(!self) return NULL;\n'
        self._c_file += INDENT + '{}.destroy = {};\n'.format(self._c_vtable_inst_name, self._free_new_name)
        self._c_file += INDENT + 'self->{} =  &{};\n'.format(self._vtable_ref_name, self._c_vtable_inst_name)

        self._c_file += INDENT + '{}_init({});\n'.format(name, init_params_new)
        self._c_file += INDENT + 'return self;\n'
        self._c_file += '}\n\n'


    def _gen_c_init(self):
        params = ', '.join([self._class.name + ' *self', self._c_constructor_params])
        self._c_file += 'static void {}_init({})\n'.format(self._class.name, params)
        self._c_file += '{\n'
        self._c_file += '}\n\n'


    def _gen_c_destructors(self):
        self._c_file += c_title('destructors')
        self._c_file += 'void {}({} *self)\n'.format(self._free_name, self._class.name)
        self._c_file += '{\n'
        self._c_file += INDENT + '/* should be completed considering what the class contains */\n'
        self._c_file += '}\n\n'

        self._c_file += 'void {}({} *self)\n'.format(self._free_new_name, self._class.name)
        self._c_file += '{\n'
        self._c_file += INDENT + 'if(self) {}(self);\n'.format(self._free_name)
        self._c_file += INDENT + 'free(self);\n'
        self._c_file += '}\n\n'

    def _gen_c_methods(self):
        if len(self._class.methods.values()):
            self._c_file += c_title('methods')
        for m in self._class.methods.values():
            params = ', '.join([self._class.name+' *self']+[_parse_type(p.type)+' '+p.name for p in m.parameters])
            self._c_file += '{} {} ({})\n'.format(_parse_method_type(m), m.c_name, params)
            self._c_file += '{\n}\n\n'

    def _gen_h_header(self):
        header = '/*\n'
        header += ' * {}\n'.format(self._h_file_name)
        header += ' */\n\n'
        self._h_file = header + self._h_file

    @staticmethod
    def _find_inclusion_needs(my_type, type_filter):
        if not isinstance(my_type, Class):
            return []
        inlcusion_needs = []
        for at in my_type.attributes.values():
            if at.type not in inlcusion_needs and isinstance(at.type, type_filter):
                inlcusion_needs.append(at.type)
        for m in my_type.methods.values():
            if m.type not in inlcusion_needs and isinstance(m.type, type_filter):
                inlcusion_needs.append(m.type)
                for p in m.parameters:
                    if p.type not in inlcusion_needs and isinstance(p.type, type_filter):
                        inlcusion_needs.append(p.type)
        # si il s'inclut lui-meme on le retire des imports
        inlcusion_needs = list(filter(lambda t: t != my_type, inlcusion_needs))
        # on enleve aussi les enums qu'il definit dans son .h
        # [inlcusion_needs.remove(e) for e in my_type.c_class._c_enums]
        return inlcusion_needs

    @staticmethod
    def _find_more_heavy(inlcusion_weights):
        more_heavy = list(inlcusion_weights.keys())[0]
        for i in inlcusion_weights.keys():
            if len(inlcusion_weights[i]) > len(inlcusion_weights[more_heavy]):
                more_heavy = i
        return more_heavy

    # @staticmethod
    # def find_enum_usage(pack, enum):
    #     enum_usage = 0
    #     for c in pack.classes.values():
    #         enum_needs = CClass._find_inclusion_needs(c, Enum)
    #         if enum in enum_needs:
    #             enum_usage += 1
    #     for p in pack.packages:
    #         enum_usage += CClass.find_enum_usage(p, enum)
    #     return enum_usage

    def _gen_h_include(self):
        defined_enums_type = [e._enum for e in self._c_enums]
        # si les type de fonction/attributs ou parametre sont definis dans un autre .h alors il faut l'inclure:
        class_inlcusion_needs = self._find_inclusion_needs(self._class, Class)
        inclusions = []
        while len(class_inlcusion_needs):
            inlcusion_weights ={i:self._find_inclusion_needs(i, Class) for i in class_inlcusion_needs }
            more_heavy = self._find_more_heavy(inlcusion_weights)
            inclusions.append(more_heavy)
            e = inlcusion_weights[more_heavy]
            for i in inlcusion_weights[more_heavy]:
                if i in class_inlcusion_needs:
                    class_inlcusion_needs.remove(i)
            class_inlcusion_needs.remove(more_heavy)
        # Now we include all the .h of the classes contained in inclusions
        for c in inclusions:
            self._h_file += '#include "{}"\n'.format(self.make_h_path(c))
        enum = [e for e in self._c_enums if e.should_have_its_own_file]
        for e in enum:
                self._h_file += '#include "{}"\n'.format(self.make_h_path(e._enum))



    def _gen_h_class_structure(self):
        name = self._class.name
        self._h_file += h_title('class structure')
        self._h_file += 'typedef struct {}\n'.format(name)
        self._h_file += INDENT + '{\n'


        if len(self._class.attributes.values()):
            self._h_file += 2*INDENT + '/* attributes */\n'
        for at in self._class.attributes.values():
            self._h_file += 2*INDENT + '{} {};\n'.format(_parse_attribute_type(at), at.name)


        self._h_file += 2*INDENT + '/* virtual table */\n'
        self._h_file += 2*INDENT + 'const struct {} *{};\n'.format(self._vtable_name, self._vtable_ref_name)

        self._h_file += INDENT + '}} {};\n\n'.format(name)

    def _gen_h_v_table(self):
        self._h_file += h_title('virtual table')
        self._h_file += 'typedef struct {}\n'.format(self._vtable_name)
        self._h_file += INDENT + '{\n'

        self._h_file += INDENT + '/* destructor */\n'
        self._h_file += 2 * INDENT + 'void (*destroy) (struct {}*);\n'.format(self._class.name)
        if len(self._class.methods.values()):
            self._h_file += INDENT + '/* methods */\n'
        for m in self._class.methods.values():
            self_param = '{}*'.format(self._class.name)
            params = ', '.join([self_param]+[_parse_type(p.type)+' '+p.name for p in m.parameters])
            self._h_file += 2*INDENT + '{}(*{}) ({});\n'.format(_parse_method_type(m), m.name, params)
        self._h_file += INDENT + '}} {};\n\n'.format(self._vtable_name)



    def _gen_h_constructors(self):
        # cons = self._class.constructors[0]
        name = self._class.name
        self._h_file += h_title('constructors')
        self._h_file += '{0} {0}_create({1});\n'.format(name,  self._h_constructor_params)
        self._h_file += '{0}* {0}_new({1});\n\n'.format(name, self._h_constructor_params)
        self._h_file += h_title('destructors')
        self._h_file += 'void {}({}*);\n'.format(self._free_name, name)
        self._h_file += 'void {}({}*);\n\n'.format(self._free_new_name, name)


    def _gen_h_enums(self):
        enums = [e for e in self._c_enums if not e.should_have_its_own_file]
        if len(enums):
            self._h_file += h_title('enumerations')
        for e in enums:
            self._h_file += '{}'.format(e.h_file)
            self._h_file += '\n\n'


    def _gen_h_methods(self):
        if len(self._class.methods.values()):
            self._h_file += h_title('methods')
        for m in self._class.methods.values():
            params = ', '.join([self._class.name+'*']+[_parse_type(p.type)+' '+p.name for p in m.parameters])
            self._h_file += '{} {} ({});\n'.format(_parse_method_type(m), m.c_name, params)


    def _gen_h_ifndef_file(self):
        name = '{}_H'.format(self._class.name.upper())
        self._h_file = '#ifndef {0}\n' \
                       '#define {0}\n\n' \
                       '{1}\n' \
                       '#endif /* {0} */'.format(name, self._h_file)

    def _gen_h_ifdef_cpp_macro(self):
        self._h_file = IFDEF_CPP_MACRO_PATTERN.format(self._h_file)


    def add_enum(self, c_enum):
        self._c_enums.append(c_enum)

class CEnum:
    def __init__(self, enum):
        self._enum = enum
        labels = ',\n{}'.format(2*INDENT).join(enum.labels)
        self._h_file = 'typedef enum \n{0}{{\n{0}{0}{1}\n{0}}} {2} ;'.format(INDENT, labels, enum.name)
        self._should_have_its_own_file = False

    @property
    def should_have_its_own_file(self):
        return self._should_have_its_own_file

    @should_have_its_own_file.setter
    def should_have_its_own_file(self, b):
        self._should_have_its_own_file = b


    @property
    def path_h(self):
        return CClass.make_h_path(self._enum)

    @property
    def h_file(self):
            file_name = 'enum_{}.h'.format(self._enum.name)
            header = '/*\n'
            header += ' * {}\n'.format(file_name)
            header += ' */\n\n'
            return header + self._h_file


def _parse_param_type(p):
    t = p.type
    if t is None:
        warning('You should define a type for the param {}'.format(p.name))
    return _parse_type(t)

def _parse_method_type(m):
    t = m.type
    if t is None:
        warning('You should define a type for the method {}'.format(m.name))
    return _parse_type(t)

def _parse_attribute_type(at):
    t = at.type
    if t is None:
        warning('You should define a type for the attribute {}'.format(at.name))
    return _parse_type(t)

def _parse_type(t):
    if isinstance(t, Class) or isinstance(t, Enum):
        return t.name
    parse = {
        Type.int: 'int',
        Type.string: 'char*',
        Type.float: 'float',
        Type.void: 'void',
        None : ''
    }
    return parse[t]

