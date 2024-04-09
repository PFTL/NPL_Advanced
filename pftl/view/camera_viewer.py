import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow

from pftl.view import view_path

import pyqtgraph as pg


class CameraViewer(QMainWindow):
    def __init__(self, camera, parent=None):
        super().__init__(parent=parent)
        uic.loadUi(view_path/'camera_viewer.ui', self)

        self.camera = camera

        self.image_widget = pg.ImageView()

        layout = self.centralwidget.layout()
        layout.addWidget(self.image_widget)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_image)
        self.update_timer.start(30)

        self.button_acquire.clicked.connect(self.camera.read_frame)
        self.button_start.clicked.connect(self.camera.start_free_run)
        self.button_stop.clicked.connect(self.camera.stop_free_run)

        self.line_exposure.editingFinished.connect(self.update_exposure)

    def update_exposure(self):
        # self.camera.exposure = int(self.line_exposure.text())  # Option 1
        self.camera.set_exposure(int(self.line_exposure.text()))  # Option 2

    def update_image(self):
        self.image_widget.setImage(np.sum(self.camera.last_frame, 2), autoRange=False, autoLevels=False)




