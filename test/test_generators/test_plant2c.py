import unittest

from generators.plant2c import plant2c
from os.path import join, dirname


class TestPlant2C(unittest.TestCase):

    def test_plant2c(self):
        plant = """
@startuml
package my.package{
    class Hello{
        + void hello()
    }
}

@enduml
        """
        plant_file=join(dirname(__file__), join('data','c_test.tx'))
        with open(plant_file, 'w') as file:
            file.write(plant)
        plant2c(plant_file,join(dirname(__file__),'output'),
                 debug_enabled=False,todo_enabled=True)