import time

import numpy as np
import zmq


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind('tcp://*:5555')
while True:
    try:
        data = np.random.random((2, 2))
        socket.send_string('data', zmq.SNDMORE)
        socket.send_pyobj(data)
        time.sleep(0.01)
    except KeyboardInterrupt:
        break

socket.send_string('data', zmq.SNDMORE)
socket.send_pyobj('stop')