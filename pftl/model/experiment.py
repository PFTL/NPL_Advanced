import queue
from pathlib import Path
import datetime

from threading import Thread, Lock

from time import sleep

import h5py
import numpy as np
import yaml

from pftl.model.camera import ModelCamera
from pftl.model.daq import ModelDAQ


class Experiment:
    def __init__(self):
        self.config = {}
        self.daq = None
        self.camera = None

        self.scan_lock = Lock()
        self.scan_running = False
        self.keep_runing = True
        self.saving_running = False
        self.keep_saving = True

        self.measured_voltages = np.empty((1, ))
        self.scan_voltages = np.empty((1, ))

    def load_config(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def load_daq(self):
        self.daq = ModelDAQ(self.config['DAQ']['port'])

    def load_camera(self):
        self.camera = ModelCamera(self.config['Camera']['number'])
        self.camera.initialize()

    def do_scan(self):
        self.scan_voltages = np.arange(self.config['Scan']['start'],
                                    self.config['Scan']['stop'],
                                    self.config['Scan']['step']
                                    )
        self.measured_voltages = np.zeros_like(self.scan_voltages)

        self.measured_images = np.zeros((
                self.camera.frame_size[0],
                self.camera.frame_size[1],
                self.camera.frame_size[2],
                len(self.scan_voltages)
        ))
        with self.scan_lock as l:
            self.scan_running = True
            self.keep_runing = True

            for i in range(len(self.scan_voltages)):
                self.daq.set_voltage(
                    self.config['Scan']['channel_out'],
                    self.scan_voltages[i]
                    )
                self.measured_voltages[i] = self.daq.read_voltage(
                    self.config['Scan']['channel_in']
                    )
                self.measured_images[:, :, :, i] = self.camera.read_frame()
                sleep(self.config['Scan']['delay'])
                if not self.keep_runing:
                    break
            self.scan_running = False

    def start_scan(self):
        if self.scan_running:
            print('Scan already running')
            return

        self.scan_thread = Thread(target=self.do_scan)
        self.scan_thread.start()

    def continuous_save(self):
        if self.saving_running:
            print('Saving already running')
            return

        base_folder = Path(self.config['Data']['saving_folder'])
        today_folder = f'{datetime.date.today()}'
        folder = base_folder/today_folder

        folder.mkdir(parents=True, exist_ok=True)
        base_filename = Path(self.config['Data']['movie_filename'])

        filename = folder/base_filename
        i = 0
        while filename.exists():
            i += 1
            new_filename = f'{base_filename.stem}_{i}{base_filename.suffix}'
            filename = folder/new_filename

        with h5py.File(filename, 'w') as f:
            dset = f.create_dataset('Movie',
                                    (self.camera.frame_size[0],
                                     self.camera.frame_size[1],
                                     self.camera.frame_size[2],
                                     1
                                     ),
                                    maxshape=(self.camera.frame_size[0],
                                             self.camera.frame_size[1],
                                             self.camera.frame_size[2],
                                             None
                                             ),
                                    dtype=np.uint8)
            i = 0
            self.saving_running = True
            while self.keep_saving:
                try:
                    dset[:, :, :, i] = self.camera.image_queue.get(timeout=1)
                except queue.Empty:
                    break
                i += 1
                dset.resize((self.camera.frame_size[0],
                             self.camera.frame_size[1],
                             self.camera.frame_size[2],
                             i+1))

            self.saving_running = False

    def start_saving_images(self):
        self.camera.save_images = True
        self.saving_thread = Thread(target=self.continuous_save)
        self.saving_thread.start()

    def stop_saving_images(self):
        self.camera.save_images = False
        self.keep_saving = False
        print(f'Remaining images in queue: {self.camera.image_queue.qsize()}')


    def stop_scan(self):
        self.keep_runing = False

    def save_data(self):
        base_folder = Path(self.config['Data']['saving_folder'])
        today_folder = f'{datetime.date.today()}'
        folder = base_folder/today_folder

        folder.mkdir(parents=True, exist_ok=True)
        base_filename = Path(self.config['Data']['filename'])

        filename = folder/base_filename
        i = 0
        while filename.exists():
            i += 1
            new_filename = f'{base_filename.stem}_{i}{base_filename.suffix}'
            filename = folder/new_filename

        with h5py.File(filename, 'w') as f:
            dset_iv = f.create_dataset('IV',
                                       data=np.vstack((self.scan_voltages, self.measured_voltages)))
            dset_images = f.create_dataset('Images', data=self.measured_images)


    def save_metadata(self):
        pass

    def finalize(self):
        self.daq.finalize()
        self.camera.finalize()


if __name__ == "__main__":
    exp = Experiment()
    exp.load_config('../../Examples/config.yml')
    exp.load_daq()
    V, I = exp.do_scan()
    print(I)
    exp.finalize()