import os
from smart_model.smart_model import SmartModel

# class PyModel(SmartModel):
#     def __init__(self, smart_model):
#         super(PyModel, self).__init__(smart_model.classes, smart_model.packages)
#         # renaming paths to python convention:
#         for c in self.classes:
#             c.path = [e.lower() for e in c.path]



def smart2py(smart_model, output_path = []):
    # py_model = PyModel(smart_model)
    for c in smart_model.classes:
        c.extension='.py'
        path = c.make_file_path(output_path)
        dir = os.path.dirname(path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(path, 'w'):
            ...
