__author__ = 'dimv36'
from qcustomplot.qcustomplot import QCustomPlot

class MousePlot(QCustomPlot):
    def __init__(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, event):
        print('MousePlot: mousePressEvent')