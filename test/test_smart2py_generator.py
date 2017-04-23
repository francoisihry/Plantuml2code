import unittest
from generators.smart2py import smart2py
from smart_model.smart_model import *

class TestSmart2Py(unittest.TestCase):

    def test_smart_model(self):
        classes = [Class("classe_A"), Class("classe_B")]
        packages = [Package(path=['path','to','my_package'], classes=[Class("classe_C")], packages=[Package(path=['empty_package'])])]
        smart_model = SmartModel(classes, packages)
        smart2py(smart_model, output_path=['.','output'])




