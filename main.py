import getopt
from os import getcwd
from os.path import exists, isdir
from os.path import join
from sys import argv, exit

from generators.plant2py import plant2py
from generators.plant2c import plant2c


def get_path(path):
    if exists(join(getcwd(),path)):
        return join(getcwd(),path)
    else:
        return path

def usage():
    print(
"""
Usage: plant2code <python|c> PLANT_UML_FILE [OPTION]...         (1st form)
  or:  plant2code <python|c> PLANT_UML_FILE OUTPUT [OPTION]...  (2nd form)

In the 1st form, generate code from the PLANT_UML_FILE in the current directory.
In the 2nd form, generate code from the PLANT_UML_FILE and output it in the OUPUT path.

Mandatory arguments to long options are mandatory for short options too.
  -h, --help            display this help and exit
  -d, --debug           enable debug
      --disable-todo    disable todo indications
 """
    )

def generate(language, plantuml_file, output, debug_enabled, todo_enabled):
    print("generating...")
    print('language ={}'.format(language))
    print('output dir ={}'.format(output))
    print('plant uml file ={}'.format(plantuml_file))
    print('debug ={}'.format(debug_enabled))
    print('todo enabled ={}'.format(todo_enabled))
    if language == 'python':
        plant2py(plantuml_file,output,debug_enabled,todo_enabled)
    elif language == 'c':
        plant2c(plantuml_file,output,debug_enabled,todo_enabled)


def main(argv):
    if len(argv)<3:
        print('Not enough arguments.')
        usage()
        exit(2)
    language = argv[1]
    if language not in ['python','c']:
        print('{} is not a correct language.'.format(language))
        usage()
        exit(2)
    plant_uml_path = get_path(argv[2])
    if not exists(plant_uml_path) or isdir(plant_uml_path):
        print('PlantUml file note found : {}'.format(plant_uml_path))
        usage()
        exit(2)

    global output
    debug = False
    enable_todo = True
    output = getcwd()
    if len(argv)==3:
        generate(language,plant_uml_path, output, debug, enable_todo)
        exit(2)
    expected_opts = ("hd", ["help", "debug","disable-todo"])

    if len(getopt.getopt([argv[3]], expected_opts[0], expected_opts[1])[0])>0:
        argv_start=3
    elif exists(argv[3]) and isdir(argv[3]):

        output = get_path(argv[3])
        argv_start=4
    else:
        print('Incorrect output path : {}'.format(argv[3]))
        usage()
        exit(2)

    try:
        opts, args = getopt.getopt(argv[argv_start:], expected_opts[0], expected_opts[1])
    except getopt.GetoptError as e:
        print(str(e))
        usage()
        exit(2)
    if len(args)>0:
        print('Unexpected argument : {}'.format(', '.join(args)))
        usage()
        exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            exit()
        elif opt in ("-d", "--debug"):
            debug = True
        elif opt == "--disable-todo":
            enable_todo = False
        else:
            print("Incorrect argument : {}\n".format(opt))
            usage()
            exit(2)
    generate(language, plant_uml_path, output, debug, enable_todo)

# main(['1','c','LICENSE','-d'])
if __name__ == "__main__" :
    main(argv)