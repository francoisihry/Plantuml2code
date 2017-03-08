from smart_model.smart_model import SmartModel

class Plant2Smart:
    def __init__(self, plant):
        self._plant = plant
        self._smart_model = SmartModel()

    def parse(self):

        for c in self._plant.classes:
            self._create_class(c)


    def _create_class(self, c):
        pass
