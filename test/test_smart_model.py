import unittest
from smart_model.smart_model import *


class TestSmartModel(unittest.TestCase):

    def test_smart_model(self):
        classes_1 = [Class("classe_A"), Class("classe_B")]
        packages_1 = [Package(path=['path','to','my_package'], classes=[Class("classe_C")], packages=[Package(path=['empty_package'])])]
        smart_model_1 = SmartModel(classes_1, packages_1)
        self.assertEqual(len(smart_model_1.classes), 2)
        self.assertEqual(smart_model_1.classes[0].name, "classe_A")
        self.assertEqual(str(smart_model_1.classes[0]), "Class classe_A")
        self.assertEqual(smart_model_1.classes[1].name, "classe_B")
        self.assertEqual(len(smart_model_1.packages),1)
        self.assertEqual(smart_model_1.packages[0].path, ['path','to','my_package'])
        self.assertEqual(len(smart_model_1.packages[0].classes), 1)
        self.assertEqual(smart_model_1.packages[0].classes[0].name, "classe_C")
        self.assertEqual(smart_model_1.packages[0].packages[0].path, ['empty_package'])

        classes_2 = [Class("classe_D"), Class("classe_E"), Class("classe_F")]
        smart_model_2 = SmartModel(classes_2)
        self.assertEqual(len(smart_model_2.classes), 3)
        self.assertEqual(smart_model_2.classes[0].name, "classe_D")
        self.assertEqual(smart_model_2.classes[1].name, "classe_E")
        self.assertEqual(smart_model_2.classes[2].name, "classe_F")

