import inspect

def penis():
    print(inspect.currentframe().f_code.co_name)

penis()    


