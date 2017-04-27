# plant2code
This project aims to allow developpers to generate code from a Plant UML class diagramm.
Languages curently supported :
  - python

# How to use:

- 1) Define a PlantUML class diagram:

 PlantUML is an easy grammar that generates UML drawings : [PlantUML project](https://nodesource.com/products/nsolid)

- 2) Launch plant2code with the specified language and the diagram path as arguments (you can also specify where you want the code to be generated)
```sh
$ plant2code python path/to/plantuml_diagram.txt /tmp/output
```

- 3) That's it ! Your code as been generated, now you should follow the todo indications (printed as comment inside the code) to complete the code.

# Documentation:

Usage: plant2code <python|c> PLANT_UML_FILE [OPTION]...         (1st form)

  or:  plant2code <python|c> PLANT_UML_FILE OUTPUT [OPTION]...  (2nd form)

In the 1st form, generate code from the PLANT_UML_FILE in the current directory.

In the 2nd form, generate code from the PLANT_UML_FILE and output it in the OUPUT path.

Mandatory arguments to long options are mandatory for short options too.

  -h, --help            display this help and exit
  
  -d, --debug           enable debug
  
      --disable-todo    disable todo indications

# Feedbacks:

Interested in that project ? You found a bug ? An improvement idea ?
Please feel free to contact me: francois.ihry@gmail.com
