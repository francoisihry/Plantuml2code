from sys import argv, exit
from os.path import exists, isdir
import getopt

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
    plant_uml_path = argv[2]
    if not exists(plant_uml_path) or isdir(plant_uml_path):
        print('PlantUml file note found : {}'.format(plant_uml_path))
        usage()
        exit(2)

    try:
        print(argv)
        ar = argv[3:]
        opts, args = getopt.getopt(argv[3:], "hd", ["help", "debug","disable-todo"])
        print(opts)
    except getopt.GetoptError as e:
        print(str(e))
        usage()
        exit(2)
    if len(args)>0:
        print('Unexpected argument : {}'.format(', '.join(args)))
        usage()
        exit(2)
    debug = False
    enable_todo = True
    for opt, arg in opts:
        print("opt={}".format(opt))
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
# main(['1','c','LICENSE','-h','-e'])
if __name__ == "__main__" :
    main(argv)