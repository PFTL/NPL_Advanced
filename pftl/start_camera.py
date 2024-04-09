from PyQt5.QtWidgets import QApplication

from pftl.model.camera import ModelCamera
from pftl.view.camera_viewer import CameraViewer


camera = ModelCamera(0)
camera.initialize()

app = QApplication([])

camera_window = CameraViewer(camera)
camera_window.show()
app.exec()

camera.finalize()