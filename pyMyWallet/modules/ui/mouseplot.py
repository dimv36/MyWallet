__author__ = 'dimv36'
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QToolTip
from qcustomplot.qcustomplot import QCustomPlot, QCPBarData

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
                need_tooltip = False
                x = self.xAxis.pixelToCoord(event.pos().x())
                y = self.yAxis.pixelToCoord(event.pos().y())
                bar = self.plottableBarsAt(event.pos())
                graph = self.plottableGraphAt(event.pos())
                if bar:
                    print('bar found')
                    need_tooltip = True
                    data = QCPBarData(bar.data()[3.0])
                    print(data.key, data.value)
                elif graph:
                    print('graph found')
                    need_tooltip = True
                if need_tooltip:
                    QToolTip.showText(event.globalPos(),
                                      QCoreApplication.translate('MousePlot',
                                                                 '<table>'
                                                                 '<tr>'
                                                                 '<th colspan="2">%s</th>'
                                                                 '</tr>'
                                                                 '<tr>'
                                                                 '<td>X: %s</td>'
                                                                 '</tr>'
                                                                 '<tr>'
                                                                 '<td>Y: %s</td>'
                                                                 '</tr>'
                                                                 '</table>' % (plottable.name(), str(x), str(y))))
                print(x, y)
            else:
                print('Plottable is None')

        super().mousePressEvent(event)
