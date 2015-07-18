__author__ = 'dimv36'
from qcustomplot.qcustomplot import QCustomPlot

class MousePlot(QCustomPlot):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        print('MousePlot: mousePressEvent')