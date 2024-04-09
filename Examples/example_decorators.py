from functools import wraps

import numpy as np


def check_positive(func):
    print('Checking positivity')

    @wraps(func)
    def wrapper(x, y):
        print(f'Values: {x}, {y}')
        if x < 0 or y < 0:
            raise Exception('X or Y are negative')
        return func(x, y)

    return wrapper


def above_threshold(threshold):
    print('Checking threshold')

    def inner_decorator(func, threshold=threshold):
        def wrapper(x, y):
            if x < threshold or y < threshold:
                raise Exception('Values below threshold')
            return func(x, y)
        return wrapper
    return inner_decorator


@check_positive
@above_threshold(-5)
def average(x, y):
    """ This is the average Function
    """
    return (x+y) / 2

@check_positive
def geometric_average(x, y):
    return np.sqrt((x*y))


print(average(-1, 2))
print(geometric_average(1, 3))

# print(average(-1, 1))

print(help(average))