import queue
from queue import Queue

q = Queue()
q.put('a')

while True:
    try:
        q.get(timeout=1)
    except queue.Empty:
        break