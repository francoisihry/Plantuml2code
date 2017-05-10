import unittest

from generators.plant2py import *
from os.path import join, dirname


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
        plant_file=join(dirname(__file__), join('data','diagram_1.tx'))
        with open(plant_file, 'w') as file:
            file.write(plant)
        plant2py(plant_file,join(dirname(__file__),'output','test_plant2py'),
                 debug_enabled=False,todo_enabled=True)