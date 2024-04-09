from threading import Thread, Lock

from time import sleep

import numpy as np
import yaml

from pftl.model.daq import ModelDAQ


class Experiment:
    def __init__(self):
        self.config = {}
        self.daq = None
        self.scan_lock = Lock()
        self.scan_running = False
        self.keep_runing = True
        self.measured_voltages = np.empty((1, ))
        self.scan_voltages = np.empty((1, ))

    def load_config(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)

    def load_daq(self):
        self.daq = ModelDAQ(self.config['DAQ']['port'])

    def do_scan(self):
        self.scan_voltages = np.arange(self.config['Scan']['start'],
                                    self.config['Scan']['stop'],
                                    self.config['Scan']['step']
                                    )
        self.measured_voltages = np.zeros_like(self.scan_voltages)

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

    def stop_scan(self):
        self.keep_runing = False

    def save_data(self):
        pass

    def save_metadata(self):
        pass

    def finalize(self):
        pass


if __name__ == "__main__":
    exp = Experiment()
    exp.load_config('../../Examples/config.yml')
    exp.load_daq()
    V, I = exp.do_scan()
    print(I)
    exp.finalize()