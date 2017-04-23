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
        pack_path_to_my_package = smart_model_1.packages[0].packages[0].packages[0]
        self.assertEqual(pack_path_to_my_package.path, ['path','to','my_package'])
        self.assertEqual(len(pack_path_to_my_package.classes), 1)
        self.assertEqual(pack_path_to_my_package.classes[0].name, "classe_C")
        self.assertEqual(pack_path_to_my_package.packages[0].path, ['path', 'to', 'my_package','empty_package'])

