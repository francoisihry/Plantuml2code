import sys

from parsers.plant2smart import plant2smart, MM_PLANT
from generators.smart2py import smart2py

DEBUG = False

def plant2py(plant_uml_model,output):
    smart_model = plant2smart(plant_uml_model)
    smart2py(smart_model, output_path=output)


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
    smart_model = plant2smart(plant_uml_model)
