import numpy as np
import zmq


def movie_saver(port, topic):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://localhost:{port}")
    socket.setsockopt(zmq.SUBSCRIBE, topic.encode('ascii'))  # Set the topic filter

    while True:
        topic = socket.recv_string()
        data = socket.recv_pyobj()
        if isinstance(data, str):
            break
        print(np.min(data), np.max(data))