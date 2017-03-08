from smart_model.smart_model import SmartModel, Class, Accessibility
from smart_model.attribute import Attribute, Method
# from plant2py import NAMES_SPACES

class Plant2Smart:
    def __init__(self, plant, names_spaces):
        self._plant = plant
        self._names_spaces = names_spaces
        self._smart_model = SmartModel()

    def parse(self):

        for c in self._plant.classes:
            new_class = self._create_class(c)
            pass



    def _create_class(self, c):
        attributes = []
        for at in c.attributes:
             if isinstance(at,self._names_spaces['Value']):
                 attributes.append(Attribute(at.name,
                                             accessibility=self._parse_accessibility(at.visibility)))
             else:
                 attributes.append(Method())


        return Class(c.name,
                     attributes=attributes)

    def _parse_accessibility(self,visibility):
        accessibitity = {"+":Accessibility.public,
                         "-" : Accessibility.private}
        return accessibitity[visibility]