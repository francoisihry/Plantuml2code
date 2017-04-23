import unittest

from plant2py import *


class TestPlant2Py(unittest.TestCase):

    def test_plant2py(self):
        plant = """
                        @startuml
                        package path.to.pack{
                            package element{
                                class Point{
                                    - x
                                    - y
                                    + get_middle()
                                }
                            }
                        }
                        package geo {
                            class segment
                        }
                        class Figure

                        Figure *-- segment
                        Point --* segment
                        @enduml
        """
        plant_uml_model = MM_PLANT.model_from_str(plant)
        plant2py(plant_uml_model,['output'])