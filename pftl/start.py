from PyQt5.QtWidgets import QApplication

from pftl.model.experiment import Experiment
from pftl.view.scan_window import ScanWindow


exp = Experiment()
exp.load_config('../Examples/config.yml')
exp.load_daq()

app = QApplication([])
win = ScanWindow(exp)
win.show()
app.exec()

exp.finalize()