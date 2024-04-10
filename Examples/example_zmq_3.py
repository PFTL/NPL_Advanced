import numpy as np
import zmq


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt(zmq.SUBSCRIBE, b'data')  # Set the topic filter

while True:
    topic = socket.recv_string()
    data = socket.recv_pyobj()
    if isinstance(data, str):
        break
    print(np.min(data), np.max(data))