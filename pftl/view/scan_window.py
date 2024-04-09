from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from pftl.view import view_path


class ScanWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        self.experiment = experiment

        uic.loadUi(view_path/'scan_window.ui', self)

        self.button_start.clicked.connect(self.experiment.start_scan)
        self.button_stop.clicked.connect(self.experiment.stop_scan)

        self.line_start.setText(str(self.experiment.config['Scan']['start']))
        self.line_stop.setText(str(self.experiment.config['Scan']['stop']))
        self.line_step.setText(str(self.experiment.config['Scan']['step']))

        self.line_start.editingFinished.connect(self.line_updated)
        self.line_stop.editingFinished.connect(self.line_updated)
        self.line_step.editingFinished.connect(self.line_updated)

        self.plot = self.plot_widget.plot(self.experiment.scan_voltages, self.experiment.measured_voltages)

        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plot)
        self.plot_timer.start(30)

    def update_plot(self):
        self.plot.setData(self.experiment.scan_voltages, self.experiment.measured_voltages)

    def line_updated(self):
        print('Line updated')
        self.experiment.config['Scan'].update({
            'start': float(self.line_start.text()),
            'stop': float(self.line_stop.text()),
            'step': float(self.line_step.text()),
            })

    def button_clicked(self):
        print('Button clicked')
        if self.experiment.scan_running:
            self.experiment.stop_scan()
        else:
            self.experiment.start_scan()

    def closeEvent(self, *args, **kwargs):
        print('Closing')
        self.experiment.finalize()

        super().closeEvent(*args, **kwargs)


if __name__ == "__main__":
    app = QApplication([])
    win = ScanWindow()
    win.show()
    app.exec()
