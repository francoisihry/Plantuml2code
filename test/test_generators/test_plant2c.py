import unittest
import subprocess
from generators.plant2c import plant2c
from os.path import join, dirname, exists
import os



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
            self.assertTrue(exists(join(dirname(__file__), 'output','test_plant2c_3', 'a.c')))
            a_h_path = join(dirname(__file__), 'output', 'test_plant2c_3', 'a.h')
            self.assertTrue(exists(a_h_path))
            self.assertTrue(exists(join(dirname(__file__), 'output', 'test_plant2c_3', 'b.c')))
            b_h_path = join(dirname(__file__), 'output', 'test_plant2c_3', 'b.h')
            self.assertTrue(exists(b_h_path))
            self.assertTrue(exists(join(dirname(__file__), 'output', 'test_plant2c_3', 'my_pack', 'time_unit.h')))

            # we check that a and b include the time_unit.h:
            enum_include = '#include "{}"'.format(join('my_pack', 'time_unit.h'))
            with open(a_h_path, 'r') as a_h_file:
                self.assertTrue(enum_include in a_h_file.read())
            with open(b_h_path, 'r') as b_h_file:
                self.assertTrue(enum_include in b_h_file.read())

    def test_plant2c_4(self):
        output_path = join(dirname(__file__), 'output', 'test_plant2c_4')
        [os.remove(f) for f in [join(output_path, f) for f in os.listdir(output_path)]]
        # Si un enum est utilise dans 2 classes, alors l'enum doit etre definis
        # dans un .h et importé par les 2 classes
        plant = """
@startuml
class chien{
+ void aboyer()
}
@enduml
        """
        plant_file = join(dirname(__file__), join('data', 'c_test_4.tx'))
        with open(plant_file, 'w') as file:
            file.write(plant)
        plant2c(plant_file, join(dirname(__file__), 'output','test_plant2c_4'),
                debug_enabled=False, todo_enabled=True)
        chien_c_path = join(dirname(__file__), 'output', 'test_plant2c_4', 'chien.c')
        self.assertTrue(exists(chien_c_path))
        main_c_path = join(dirname(__file__), 'output', 'test_plant2c_4', 'main.c')
        main_c = """
#include <stdlib.h>
#include<stdio.h>

#include "chien.h"

int main()
{
    chien toutou = chien_create();
    toutou.vtable->aboyer(&toutou);
    chien* medord = chien_new();
    medord->vtable->aboyer(medord);
    toutou.vtable->destroy(&toutou);
    medord->vtable->destroy(medord);
    return 0;
}
        """
        with open(main_c_path, 'w') as file:
            file.write(main_c)
        makefile_path = join(dirname(__file__), 'output', 'test_plant2c_4', 'Makefile')

        with open(makefile_path, 'r+') as file:
            makefile = file.read()
            makefile = makefile.replace('SRC= ', 'SRC= main.c\\\n')
            file.seek(0)
            file.write(makefile)
            file.truncate()

        with open(chien_c_path, 'r+') as file:
            chien_c_file = file.read()
            chien_c_file = chien_c_file.replace("void chien_aboyer (chien *self)\n{\n}",
                                                'void chien_aboyer (chien *self)\n{\n   printf("OUAF\\n");\n}')
            file.seek(0)
            file.write(chien_c_file)
            file.truncate()

        cmd_make = "cd {};make all".format(output_path)
        make_process = subprocess.Popen(cmd_make, stderr=subprocess.STDOUT, shell=True)
        self.assertEqual(make_process.wait(),0)

        cmd_run = "cd {};./prog".format(output_path)
        run_process = subprocess.Popen(cmd_run, stderr=subprocess.STDOUT, shell=True)
        self.assertEqual(run_process.wait(), 0)








