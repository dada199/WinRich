import time
from datetime import datetime
from functools import wraps


def time_it(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        start_time = datetime.now()
        print(f'Start time is {start_time}')
        result = fn(*args, **kwargs)
        end_time = datetime.now()
        print(f'End time is {end_time}')
        print(f'Total time is {end_time - start_time}')

        return result
    return inner

