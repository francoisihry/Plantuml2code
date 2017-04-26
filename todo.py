ENABLE_TODO = True

def todo(msg):
    if ENABLE_TODO:
        return msg
    else:
        return ''

def define_params(params):
    return 'TODO define the parameters : {}'.format(' ,'.join(params))