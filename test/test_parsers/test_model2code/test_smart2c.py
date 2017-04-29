import unittest
from os.path import dirname
from parsers.model2code.smart2c.smart2c import Smart2c
from smart_model.model import *
from smart_model.attribute import Type, Parameter, Attribute


class TestSmart2C(unittest.TestCase):

    def test_smart_model(self):
        stylo = Class("Stylo")
        stylo.methods['ecrire'] = Method('ecrire', type=Type.void, visibility=Visibility.public,
                 parameters=[Parameter('texte',type=Type.string)])
        enum_couleur = Enum('Couleur', ['ROUGE', 'VERT', 'BLEU'])
        stylo.methods['lire_encre'] = Method('lire_encre', type=enum_couleur)
        stylo.constructors.append(Method('Stylo', parameters=[Parameter('couleur',type=enum_couleur)]))
        classes = [stylo]
        enums = {enum_couleur.name: enum_couleur}
        smart_model = SmartModel(classes, enums=enums)
        stylo.attributes['couleur'] = Attribute('couleur',type=enum_couleur, visibility=Visibility.private)
        Smart2c(smart_model, output_path=join(dirname(__file__),'output'))




