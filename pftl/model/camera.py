from threading import Thread

import cv2
import numpy as np


class ModelCamera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self._driver = None
        self.last_frame = np.empty((50, 50))
        self.is_acquiring = False
        self.keep_acquiring = True

    def initialize(self):
        self._driver = cv2.VideoCapture(self.cam_num)

    def read_frame(self):
        ret, frame = self._driver.read()
        self.last_frame = frame
        return frame

    def free_run(self):
        if self.is_acquiring:
            print('Already acquiring!')
            return
        self.is_acquiring = True
        self.keep_acquiring = True
        while self.keep_acquiring:
            frame = self.read_frame()
        self.is_acquiring = False

    def start_free_run(self):
        self.acquire_thread = Thread(target=self.free_run)
        self.acquire_thread.start()

    def stop_free_run(self):
        self.keep_acquiring = False

    @property
    def exposure(self):
        return self._driver.get(cv2.CAP_PROP_EXPOSURE)

    @exposure.setter
    def exposure(self, value):
        self._driver.set(cv2.CAP_PROP_EXPOSURE, value)

    @property
    def brightness(self):
        return self._driver.get(cv2.CAP_PROP_BRIGHTNESS)

    def get_exposure(self):
        return self._driver.get(cv2.CAP_PROP_EXPOSURE)

    def set_exposure(self, value):
        self._driver.set(cv2.CAP_PROP_EXPOSURE, value)

    def finalize(self):
        self._driver.release()


if __name__ == "__main__":
    cam = ModelCamera(0)
    cam.initialize()
    print(cam.get_exposure())
    print(cam.exposure)
    cam.exposure = -3
    print(cam.read_frame())
    cam.set_exposure(-10)
    print(cam.read_frame())
    cam.finalize()