import unittest
from textx.metamodel import metamodel_from_file
from os.path import join, dirname



plant1 ="""
@startuml
class qs5d
abstract class abstract_cl{
    - hey
    + baaahahh()

}
package path.to.my.package{
    class class_inside_package{
    }
}
class_inside_package *-- abstract_cl
@enduml
"""
class TestPlantUmlGrammar(unittest.TestCase):
    def setUp(self):
        self.meta_model = metamodel_from_file(join(dirname(__file__) , '../plant_uml_grammar.tx'))

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


    def test_attributes(self):
        pass

    def test_relations(self):
        pass