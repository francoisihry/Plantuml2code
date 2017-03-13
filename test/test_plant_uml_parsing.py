import unittest
from textx.metamodel import metamodel_from_file
from os.path import join, dirname
from parsers.plant2smart import Plant2Smart
from plant2py  import NAMES_SPACES, MM_PLANT

class TestPlantUmlParsing(unittest.TestCase):
    def setUp(self):
        pass


    def test(self):
        plant = """
                @startuml
                class A {
                    + attr1
                    - func1()
                }
                class B
                @enduml"""
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = Plant2Smart(plant_uml_model, NAMES_SPACES)
        pass
        self.assertEqual(len(smart_model.classes), 2)
        self.assertEqual(smart_model.classes[0].name, 'A')
        self.assertEqual(len(smart_model.classes[0].attributes), 2)

