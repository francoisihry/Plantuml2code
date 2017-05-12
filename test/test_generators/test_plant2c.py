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
        plant2c(plant_file,join(dirname(__file__),'output','test_plant2c'),
                 debug_enabled=False,todo_enabled=True)

    def test_plant2c_2(self):
        # Si un enum est utilise dans 2 classes, alors l'enum doit etre definis
        # dans un .h et importé par les 2 classes
        plant = """
@startuml
class A{
    + B at_b
    + C at_c
    + D at_d
    + F met_f()
    + E met_e(G param_g)
}
class B{
    + C at_c
}
class C
class D{
    + B at_b
    + D at_d
    + C met_c()
    + G met_g()
}
class E{
    + C met_c(F param_f)
}
class F
class G
@enduml
            """
        plant_file = join(dirname(__file__), join('data', 'c_test_2.tx'))
        with open(plant_file, 'w') as file:
            file.write(plant)
        plant2c(plant_file, join(dirname(__file__), 'output', 'test_plant2c_2'),
                debug_enabled=False, todo_enabled=True)

    def test_plant2c_3(self):
        # Si un enum est utilise dans 2 classes, alors l'enum doit etre definis
        # dans un .h et importé par les 2 classes
            plant = """
@startuml

package my_pack{
    enum TimeUnit {
      DAYS
      HOURS
      MINUTES
    }
}

class A{
    + TimeUnit t_a
}
class B{
    + TimeUnit t_b
}


@enduml
            """
            plant_file = join(dirname(__file__), join('data', 'c_test_3.tx'))
            with open(plant_file, 'w') as file:
                file.write(plant)
            plant2c(plant_file, join(dirname(__file__), 'output','test_plant2c_3'),
                    debug_enabled=False, todo_enabled=True)