
import sys
from textx.metamodel import metamodel_from_file
from os.path import join, dirname

DEBUG = False
mm_plant = metamodel_from_file(join(dirname(__file__) , 'plant_uml_grammar.tx'), debug=DEBUG)


def debug(str):
    if DEBUG:
        print(str)

if __name__ == "__main__" :
    if len(sys.argv) != 2:
        print ("Please enter the plant_uml file path as parameter: \n"
               "./plant2py <plant_um file path>")
    plant_uml_path = sys.argv[1]
    print("Building a model from {} ...".format(plant_uml_path))
    plant_uml_model = mm_plant.model_from_file(plant_uml_path, debug=DEBUG)

