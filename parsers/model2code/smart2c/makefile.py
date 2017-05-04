from os.path import join

def _gen_src(pack):
    src_paths = ''
    for c in pack.classes.values():
        if len(c.path):
            src_path = join(join(*(c.path))
                          , c.c_class.c_file_name)

        else:
            src_path = join(c.c_class.c_file_name)
        src_paths += "\ " \
                     "\n    {}".format(src_path)
    for p in pack.packages:
        src_paths += _gen_src(p)
    return src_paths

def gen(smart_model):
    src_paths = _gen_src(smart_model)
    make_file = """
CC=gcc
CFLAGS=-W -Wall -ansi -pedantic
LDFLAGS=
EXEC=hello
SRC= {}
OBJS = $(SRC:.c=.o)
AOUT = prog

all : $(AOUT)

prog : $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^
%.o : %.c
	$(CC) $(CFLAGS) -o $@ -c $<
clean :
	@rm *.o
cleaner : clean
	@rm $(AOUT)
    """.format(src_paths)
    return make_file