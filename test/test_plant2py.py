import unittest

from generators.plant2py import *
from parsers.model2model.plant2smart import MM_PLANT


class TestPlant2Py(unittest.TestCase):

    def test_plant2py(self):
        plant = """
                    @startuml
                    package path.to.pack{
                        package element{
                            class Point{
                                + Point(int x, int y)
                                - x
                                - y
                                + get_middle()
                            }
                        }
                    }
                    package geo {
                        class Segment{
                            + Segment( point_a, point_b)
                        }
                    }
                    class Couleur{
                        + Couleur(color)
                        - set_new_color(color)
                        + {static} get_rgb (color)
                    }
                    class Figure
                    class Triangle
                    Triangle --> Figure

                    Figure 1 *-- 1 Couleur : couleur
                    Figure 1 *-- * Segment : contient
                    Point 1..* --* 1 Segment
                    @enduml
        """
        plant_uml_model = MM_PLANT.model_from_str(plant)
        plant2py(plant_uml_model,['output'])