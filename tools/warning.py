from warnings import simplefilter, warn



def warning(msg):
    simplefilter('default', UserWarning)
    warn(msg)