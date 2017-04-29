from parsers.model2model.plant2smart import plant2smart
from parsers.model2code.smart2c.smart2c import smart2c
from parsers.model2model.plant2smart import MM_PLANT
from tools import todo


def plant2c(plant_uml_model,output, debug_enabled, todo_enabled):
    todo.enable = todo_enabled
    plant_model= MM_PLANT.model_from_file(plant_uml_model, debug=debug_enabled)
    smart_model = plant2smart(plant_model)
    smart2c(smart_model, output_path=output)