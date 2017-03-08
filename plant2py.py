import sys
from textx.metamodel import metamodel_from_file
from os.path import join, dirname
from parsers.plant2smart import Plant2Smart

DEBUG = False
MM_PLANT = metamodel_from_file(join(dirname(__file__), 'plant_uml_grammar.tx'), debug=DEBUG)
NAMES_SPACES = MM_PLANT.namespaces['plant_uml_grammar']

plant_uml_path = "/root/PycharmProjects/plant2py/test_data.txt"
print("Building a model from {} ...".format(plant_uml_path))
plant_uml_model = MM_PLANT.model_from_file(plant_uml_path, debug=DEBUG)
smart_model = Plant2Smart(plant_uml_model, NAMES_SPACES).parse()

def debug(str):
    if DEBUG:
        print(str)

if __name__ == "__main__" :
    if len(sys.argv) != 2:
        print ("Please enter the plant_uml file path as parameter: \n"
               "./plant2py <plant_um file path>")
    plant_uml_path = sys.argv[1]
    print("Building a model from {} ...".format(plant_uml_path))
    plant_uml_model = MM_PLANT.model_from_file(plant_uml_path, debug=DEBUG)
    smart_model = Plant2Smart(plant_uml_model).parse()
