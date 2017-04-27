from parsers.model2model.plant2smart import plant2smart
from parsers.model2code.smart2py.smart2py import smart2py
from parsers.model2model.plant2smart import MM_PLANT
from tools import todo

def plant2py(plant_uml_model,output, debug_enabled, todo_enabled):
    todo.enable = todo_enabled
    plant_model= MM_PLANT.model_from_file(plant_uml_model, debug=debug_enabled)
    smart_model = plant2smart(plant_model)
    smart2py(smart_model, output_path=output)

