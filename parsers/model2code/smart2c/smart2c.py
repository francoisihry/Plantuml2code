from smart_model.attribute import Type


class Smart2c:

    def __init__(self, smart_model, output_path=None):
        self._c_file = ''
        self._h_file = ''
        for e in smart_model.enums.values():
            self.gen_enums(e)
        for c in smart_model.classes:
            self.gen_methods(c)

    def gen_enums(self, e):
        self._h_file += 'typedef enum {{ {} }} {} ;'.format(', '.join(e.labels), e.name)

    def gen_methods(self, c):
        code = ''
        for m in c.methods.values():

            params = ', '.join([self._parse_type(p.type)+' '+p.name for p in m.parameters])
            code += '{} {} ({})'.format(self._parse_type(m.type), m.name, params)
        self._c_file += code

    def _parse_type(self, t):
        parse = {
            Type.int : 'int',
            Type.string : 'char*',
            Type.float : 'float',
            Type.void : 'void'
        }
        return parse[t]


