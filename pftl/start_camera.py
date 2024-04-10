import time

from PyQt5.QtWidgets import QApplication

from pftl.model.camera import ModelCamera
from pftl.view.camera_viewer import CameraViewer




camera = ModelCamera(0)
camera.initialize()
print(camera.frame_size[2])
camera.start_free_run()
time.sleep(1)
camera.stop_free_run()
# camera.exposure = -10
# app = QApplication([])
#
# camera_window = CameraViewer(camera)
# camera_window.show()
# app.exec()
print(camera.is_acquiring)
camera.finalize()
print(camera.is_acquiring)