import sys
import datetime
import functools

RED   = "\033[1;31m"  
GREEN = "\033[0;32m"
RESET = "\033[0;0m"

class MyDecorator:
    def __init__(self, function): 
        self.function = function 

    def __call__(self, *args, **kwargs): 
        curr = str(datetime.datetime.now().date())
        if curr > args[0][7]:
            sys.stdout.write(RED)
        else:
            sys.stdout.write(GREEN)

        self.function(*args, **kwargs)
        sys.stdout.write(RESET)

