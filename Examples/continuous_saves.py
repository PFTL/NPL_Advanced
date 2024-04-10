import time
from multiprocessing import Process
from pathlib import Path
from threading import Thread

from pftl.model.experiment import Experiment
from pftl.model.movie_saver import movie_saver

base_dir = Path(__file__).parent

if __name__ == "__main__":
    exp = Experiment()
    exp.load_config(base_dir/'config.yml')
    exp.load_camera()

    exp.camera.start_free_run()
    print(f'Free run running: {exp.camera.is_acquiring}')
    # exp.start_saving_images()
    # print(f'Continous saves running: {exp.saving_running}')
    t = Process(target=movie_saver, args=(5555, 'data'))
    t.start()
    while True:
        try:
            time.sleep(0.01)
        except KeyboardInterrupt:
            break
    exp.stop_saving_images()
    exp.camera.stop_free_run()
    exp.camera.finalize()
