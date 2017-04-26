import unittest
from parsers.model2code.smart2py.smart2py import smart2py
from smart_model.smart_model import *




class TestSmart2Py(unittest.TestCase):

    def test_smart_model(self):
        class_a = Class("classe_A")
        class_b = Class("classe_B", contains=[class_a])
        classes = [class_a, class_b]
        packages = [Package(path=['path','to','my_package'], classes=[Class("classe_C")], packages=[Package(path=['empty_package'])])]
        smart_model = SmartModel(classes, packages)
        smart2py(smart_model, output_path=['.','output'])




