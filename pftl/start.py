import click
from PyQt5.QtWidgets import QApplication

from pftl.model.experiment import Experiment
from pftl.view.camera_viewer import CameraViewer
from pftl.view.scan_window import ScanWindow


@click.command()
@click.option('--config', default='config.yml', help='Path to the configuration file.')
def start(config):
    exp = Experiment()
    exp.load_config(config)
    exp.load_daq()
    exp.load_camera()

    app = QApplication([])
    win = ScanWindow(exp)
    win.show()

    camera_window = CameraViewer(exp.camera)
    camera_window.show()

    app.exec()

    exp.finalize()


if __name__ == "__main__":
    start()