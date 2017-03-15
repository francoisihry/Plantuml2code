import unittest

from parsers.plant2smart import plant2smart, MM_PLANT
from smart_model.smart_model import Accessibility

class TestPlantUmlParsing(unittest.TestCase):

    def test_class(self):
        plant = """
                @startuml
                class A {
                    + attr1
                    - func1()
                }
                class B
                @enduml"""
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = plant2smart(plant_uml_model)
        self.assertEqual(len(smart_model.classes), 2)
        classA = smart_model.classes[0]
        self.assertEqual(classA.name, 'A')
        self.assertEqual(len(classA.attributes), 2)
        self.assertEqual(classA.accessibility, Accessibility.public)
        attr1 = classA.attributes[0]
        self.assertEqual(attr1.name,'attr1')
        self.assertEqual(attr1.accessibitily, Accessibility.public)
        func1 = classA.attributes[1]
        self.assertEqual(func1.name, 'func1')
        self.assertEqual(func1.accessibitily, Accessibility.private)

        classB = smart_model.classes[1]
        self.assertEqual(classB.name, 'B')
        self.assertEqual(len(classB.attributes), 0)
        self.assertEqual(classB.accessibility, Accessibility.public)


    def test_package(self):
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
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = plant2smart(plant_uml_model)
        self.assertEqual(len(smart_model.packages),3)
        a_simple_package = smart_model.packages[0]
        self.assertEqual(a_simple_package.path,['a_simple_package'])
        self.assertEqual(len(a_simple_package.classes), 0)
        package2 = smart_model.packages[1]
        self.assertEqual(package2.path,['path', 'to', 'my', 'package1'])
        self.assertEqual(len(package2.classes),1)
        self.assertEqual(package2.classes[0].path, ['path', 'to', 'my', 'package1','class_inside_package'])

