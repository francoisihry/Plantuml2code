from parsers.model2model.plant2smart import plant2smart
from parsers.model2code.smart2py.smart2py import smart2py


def plant2py(plant_uml_model,output):
    smart_model = plant2smart(plant_uml_model)
    smart2py(smart_model, output_path=output)


