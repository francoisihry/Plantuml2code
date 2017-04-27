import unittest
from os.path import dirname
from parsers.model2code.smart2c.smart2c import Smart2c
from smart_model.model import *
from smart_model.attribute import Type, Parameter


class TestSmart2C(unittest.TestCase):

    def test_smart_model(self):
        stylo = Class("Stylo")
        stylo.methods['ecrire']=Method('ecrire', type=Type.void, visibility=Visibility.public,
                 parameters=[Parameter('texte',type=Type.string)])
        classes = [stylo]
        enums = {'Couleur': Enum('Couleur', ['ROUGE', 'VERT', 'BLEU'])}
        smart_model = SmartModel(classes, enums=enums)
        Smart2c(smart_model, output_path=join(dirname(__file__),'output'))




