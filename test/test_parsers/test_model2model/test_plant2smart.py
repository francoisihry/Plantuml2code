import unittest


from smart_model.model import Visibility
from smart_model.attribute import Method, Attribute, Type
from parsers.model2model.plant2smart import plant2smart, MM_PLANT

class TestPlantUmlParsing(unittest.TestCase):

    def test_class(self):
        plant = """
                @startuml
                class A {
                    + int attr1
                    - str func1(float arg, int i)
                    + A(str name)
                }
                class B
                @enduml"""
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = plant2smart(plant_uml_model)
        self.assertEqual(len(smart_model.classes), 2)
        classA = smart_model.classes['A']
        self.assertEqual(classA.path, [])
        self.assertEqual(classA.name, 'A')
        self.assertEqual(len(classA.attributes), 1)
        self.assertEqual(len(classA.constructors), 1)
        self.assertEqual(len(classA.methods), 1)
        self.assertEqual(classA.constructors[0].name,'A')
        self.assertEqual(classA.visibility, Visibility.public)
        attr1 = classA.attributes['attr1']
        self.assertTrue(isinstance(attr1, Attribute))
        self.assertEqual(attr1.name,'attr1')
        self.assertEqual(attr1.type, Type.int)
        self.assertEqual(attr1.visibility, Visibility.public)
        func1 = classA.methods['func1']
        self.assertTrue(isinstance(func1,Method))
        self.assertEqual(func1.name, 'func1')
        self.assertEqual(func1.type, Type.string)
        self.assertEqual(len(func1.parameters), 2)
        self.assertEqual(func1.parameters[0].type, Type.float)
        self.assertEqual(func1.parameters[0].name, 'arg')
        self.assertEqual(func1.parameters[1].type, Type.int)
        self.assertEqual(func1.parameters[1].name, 'i')
        self.assertEqual(func1.visibility, Visibility.private)

        classB = smart_model.classes['B']
        self.assertEqual(classB.name, 'B')
        self.assertEqual(len(classB.attributes), 0)
        self.assertEqual(classB.visibility, Visibility.public)


    def test_package(self):
        plant = """
                @startuml
                package a_simple_package{}
                package path.to.my.package1{
                    class ClassInsidePackage
                }

                package another.package{
                    package inside.pack{
                        package hey{
                            class Point{
                            }
                        }
                    }
                    package empty_package{}
                }
                @enduml"""
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = plant2smart(plant_uml_model)
        self.assertEqual(len(smart_model.packages),3)
        a_simple_package = smart_model.packages[0]
        self.assertEqual(a_simple_package.path,['a_simple_package'])
        self.assertEqual(len(a_simple_package.classes), 0)

        package2 = smart_model.packages[1]
        self.assertEqual(package2.path,['path'])
        self.assertEqual(len(package2.classes),0)
        pack_path_to_my_package = package2.packages[0].packages[0].packages[0]
        self.assertEqual(pack_path_to_my_package.path, ['path', 'to', 'my', 'package1'])
        self.assertEqual(pack_path_to_my_package.classes['ClassInsidePackage'].path, ['path', 'to', 'my', 'package1'])

        another_package = smart_model.packages[2].packages[0]
        self.assertEqual(another_package.path, ['another', 'package'])
        self.assertEqual(len(another_package.packages),2)
        pack_inside = another_package.packages[0].packages[0]
        self.assertEqual(pack_inside.path, ['another', 'package', 'inside', 'pack'])
        self.assertEqual(len(pack_inside.packages),1)
        hey_pack = pack_inside.packages[0]
        self.assertEqual(len(hey_pack.classes), 1)
        point = hey_pack.classes['Point']
        self.assertEqual(point.path, ['another', 'package', 'inside', 'pack', 'hey'])
        self.assertEqual(another_package.packages[1].path, ['another', 'package', 'empty_package'])

    def test_simple_composition(self):
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
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = plant2smart(plant_uml_model)
        point = smart_model.classes['Point']
        figure = smart_model.classes['Figure']
        self.assertIsNotNone(point.contained_by)
        self.assertEqual(point.contained_by[0].ref, figure)
        self.assertEqual(len(figure.contains),1)
        self.assertEqual(figure.contains[0].ref, point)

    def test_complex_composition(self):
        plant = """
                @startuml
                package path.to.pack{
                    package element{
                        class Point{
                            - x
                            - y
                            + get_middle()
                        }
                    }
                }
                package geo {
                    class segment
                }
                class Figure

                Figure *-- segment
                Point --* segment
                @enduml
                """
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = plant2smart(plant_uml_model)
        pack_path_to_pack_element = smart_model.packages[0].packages[0].packages[0].packages[0]
        point = pack_path_to_pack_element.classes['Point']
        segment = smart_model.packages[1].classes['segment']
        figure = smart_model.classes['Figure']
        self.assertEqual(figure.name,'Figure')
        self.assertIsNotNone(segment.contained_by)
        self.assertEqual(segment.contained_by[0].ref,figure)
        self.assertEqual(figure.contains[0].ref,segment)
        self.assertEqual(segment.contains[0].ref,point)

    def test_inheritance(self):
        plant = """
                @startuml
                package test {
                    class A
                }
                class B
                class C
                class D
                class E
                A --> B
                C --> B
                C --> D
                E --> A
                @enduml
                """
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = plant2smart(plant_uml_model)
        self.assertEqual(len(smart_model.classes), 4)
        A = smart_model.packages[0].classes['A']
        B = smart_model.classes['B']
        C = smart_model.classes['C']
        D = smart_model.classes['D']
        E = smart_model.classes['E']
        self.assertTrue(B in [r.ref for r in A.herits_of])
        self.assertTrue(A in [r.ref for r in B.is_herited_by])
        self.assertTrue(B in [r.ref for r in C.herits_of])
        self.assertTrue(C in [r.ref for r in B.is_herited_by])
        self.assertTrue(D in [r.ref for r in C.herits_of])
        self.assertTrue(C in [r.ref for r in D.is_herited_by])
        self.assertTrue(A in [r.ref for r in E.herits_of])
        self.assertTrue(E in [r.ref for r in A.is_herited_by])

    def test_type(self):
        plant = """
                @startuml
                class A {
                    + int attr1
                    - str func1(float ina, B_type b)

                }
                enum TimeUnit{
                    DAYS
                    HOURS
                    MINUTES
                }
                class B_type{
                    + TimeUnit get_couleur()
                }
                @enduml"""
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = plant2smart(plant_uml_model)
        class_A = smart_model.classes['A']
        class_B = smart_model.classes['B_type']
        self.assertEqual(class_A.attributes['attr1'].type, Type.int)
        self.assertEqual(class_A.methods['func1'].parameters[0].type, Type.float)
        self.assertEqual(class_A.methods['func1'].parameters[1].type, class_B)
        self.assertEqual(class_B.methods['get_couleur'].type, smart_model.enums['TimeUnit'])

    def test_enums(self):
        plant = """
                @startuml
                class A
                enum TimeUnit{
                    DAYS
                    HOURS
                    MINUTES
                }
                class B
                enum EmptyEnum
                package pac{
                    enum EnumInsidePac
                }

                @enduml"""
        plant_uml_model = MM_PLANT.model_from_str(plant)
        smart_model = plant2smart(plant_uml_model)
        self.assertEqual(smart_model.enums['TimeUnit'].labels, ['DAYS','HOURS','MINUTES'])
        self.assertEqual(smart_model.enums['EmptyEnum'].name, 'EmptyEnum')
        self.assertEqual(smart_model.packages[0].enums['EnumInsidePac'].name, 'EnumInsidePac')

