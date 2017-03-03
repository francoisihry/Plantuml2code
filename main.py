
import sys
from textx.metamodel import metamodel_from_file
from os.path import join, dirname

DEBUG = False

def debug(str):
    if DEBUG:
        print(str)

def plant2model(plant_uml_path):
    print("Building a model from {} ...".format(plant_uml_path))
    this_folder = dirname(__file__)
    mm_plant = metamodel_from_file(join(this_folder, 'meta_model.tx'), debug=False)

    return mm_plant.model_from_file(plant_uml_path,debug=DEBUG)


if __name__ == "__main__" :
    print(len(sys.argv))
    if len(sys.argv) != 2:
        print ("Please enter the plant_uml file path as parameter: \n"
               "./plant2py <plant_um file path>")

    plant_uml_model = plant2model(sys.argv[1])


