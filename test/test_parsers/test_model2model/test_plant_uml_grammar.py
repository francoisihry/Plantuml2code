import unittest
from textx.metamodel import metamodel_from_file
from os.path import join, dirname


class TestPlantUmlGrammar(unittest.TestCase):
    def setUp(self):
        self.meta_model = metamodel_from_file(join(dirname(__file__), '..','..', '..', 'plant_uml_grammar.tx'))
        self.names_spaces = self.meta_model.namespaces['plant_uml_grammar']


    def test_classes(self):
        plant = """
        @startuml
        class A {
            + attr1
            - func1()
        }
        class B
        @enduml"""
        plant_uml_model = self.meta_model.model_from_str(plant)

        self.assertEqual(len(plant_uml_model.classes),2)
        class_A = plant_uml_model.classes[0]
        self.assertTrue(isinstance(class_A,self.names_spaces['Class']))
        self.assertEqual(class_A.name,"A")
        self.assertEqual(len(class_A.attributes),2)

        attr1 = class_A.attributes[0]
        self.assertTrue(isinstance(attr1, self.names_spaces['ValueWithoutType']))

        attr2 = class_A.attributes[1]
        self.assertTrue(isinstance(attr2, self.names_spaces['MethodWithoutType']))

        class_B = plant_uml_model.classes[1]
        self.assertEqual(class_B.name, "B")

    def test_packages(self):
        plant = """
        @startuml
        package a_simple_package{}
        package path.to.my.package1{
            class class_inside_package
        }

        package another.package{
            package inside.pack{}
        }
        @enduml"""
        plant_uml_model = self.meta_model.model_from_str(plant)
        packages = plant_uml_model.packages
        self.assertEqual(len(packages),3)
        self.assertEqual(packages[0].path, ["a_simple_package"])
        self.assertEqual(packages[1].path, ["path","to","my","package1"])
        self.assertEqual(len(packages[1].classes), 1)
        self.assertEqual(packages[1].classes[0].name, "class_inside_package")
        self.assertEqual(packages[2].path, ["another", "package"])
        self.assertEqual(len(packages[2].packages), 1)
        self.assertEqual(packages[2].packages[0].path, ["inside", "pack"])


    def test_parameters(self):
        plant = """
                @startuml
                class Point{
                    + Point(int x, int y)
                }
                @enduml
                """
        plant_uml_model = self.meta_model.model_from_str(plant)
        self.assertTrue(isinstance(plant_uml_model.classes[0].attributes[0], self.names_spaces['MethodWithoutType']))
        self.assertTrue(isinstance(plant_uml_model.classes[0].attributes[0].params[0], self.names_spaces['ParameterWithType']))
        self.assertEqual(plant_uml_model.classes[0].attributes[0].params[0].type, 'int')

    def test_relations(self):
        plant = """
        @startuml
        class Point{
            - x
            - y
            + get_middle()
        }

        class Figure

        Figure *-- Point
        @enduml
        """
        plant_uml_model = self.meta_model.model_from_str(plant)
        self.assertEqual(len(plant_uml_model.relations), 1)
        point = plant_uml_model.classes[0]
        compo = plant_uml_model.relations[0]
        figure = plant_uml_model.classes[1]
        self.assertTrue(isinstance(compo, self.names_spaces['Composition']))
        contenu = compo.contenu[0]
        self.assertEqual(contenu, point)
        contenant = compo.contenant [0]
        self.assertEqual(contenant, figure)
