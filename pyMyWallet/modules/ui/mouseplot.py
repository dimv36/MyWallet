__author__ = 'dimv36'
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
import qcustomplot
from qcustomplot.qcustomplot import QCustomPlot, QCPBars, QCPGraph, QCPAbstractItem

class MousePlot(QCustomPlot):
    def __init__(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, event):
        print('MousePlot: mousePressEvent')
        event = QMouseEvent(event)
        if event.button() == Qt.LeftButton:
            print('left button clicked')
            plottable = self.plottableAt(event.pos())
            if plottable is not None:
                print('Plottable is not None')
                x = self.xAxis.pixelToCoord(event.pos().x())
                y = self.yAxis.pixelToCoord(event.pos().y())
                bar = self.plottableBarsAt(event.pos())
                graph = self.plottableGraphAt(event.pos())
                print(bar)
                print(graph)
                if isinstance(plottable, qcustomplot.QCPBars):
                    print('Found bar')
                elif isinstance(plottable, qcustomplot.QCPGraph):
                    print('Found graph')
                print(x, y)
            else:
                print('Plottable is None')

        super().mousePressEvent(event)
