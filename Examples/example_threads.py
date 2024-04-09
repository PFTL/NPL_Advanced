from threading import Thread
import numpy as np


def increase_values(var):
    for j in range(len(var)):
        for i in range(10000):
            var[j] += 1

def decrease_values(var):
    for j in range(len(var)):
        for i in range(10000):
            var[j] = var[j] - 1


my_array = np.zeros((10000, ))

increase_thread = Thread(target=increase_values, args=(my_array, ))
decrease_thread = Thread(target=decrease_values, args=(my_array, ))
increase_thread.start()
decrease_thread.start()

increase_thread.join()
decrease_thread.join()

print(f'Min: {np.min(my_array)}, Max: {np.max(my_array)}')