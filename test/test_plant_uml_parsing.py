import unittest
from textx.metamodel import metamodel_from_file
from os.path import join, dirname
from parsers.plant2smart import Plant2Smart
from plant2py  import NAMES_SPACES

class TestPlantUmlParsing(unittest.TestCase):
    def setUp(self):
        self.meta_model = metamodel_from_file(join(dirname(__file__) , '../plant_uml_grammar.tx'))
        self.names_spaces = self.meta_model.namespaces['plant_uml_grammar']


    def test(self):
        plant = """
                @startuml
                class A {
                    + attr1
                    - func1()
                }
                class B
                @enduml"""
        plant_uml_model = self.meta_model.model_from_str(plant)
        smart_model = Plant2Smart(plant_uml_model, NAMES_SPACES)
