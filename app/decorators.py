import sys
import datetime
import functools

RED   = "\033[1;31m"  
GREEN = "\033[0;32m"
RESET = "\033[0;0m"

def report(func):
    @functools.wraps(func)
    def report_wrapper(*args, **kwargs):
        curr = str(datetime.datetime.now().date())
        if curr > args[0][7]:
            sys.stdout.write(RED)
        else:
            sys.stdout.write(GREEN)

        func(*args, **kwargs)
        sys.stdout.write(RESET)
    return report_wrapper

