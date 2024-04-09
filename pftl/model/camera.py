from time import sleep

import cv2


class ModelCamera:
    def __init__(self, cam_num):
        self.cam_num = cam_num
        self._driver = None

    def initialize(self):
        self._driver = cv2.VideoCapture(self.cam_num)

    def read_frame(self):
        ret, frame = self._driver.read()
        return frame

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