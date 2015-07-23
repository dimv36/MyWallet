__author__ = 'dimv36'
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QToolTip
from qcustomplot.qcustomplot import QCustomPlot, QCPBarData


class MousePlot(QCustomPlot):
    def __init__(self, parent):
        super().__init__(parent)

    def mousePressEvent(self, event):
        event = QMouseEvent(event)
        if event.button() == Qt.LeftButton:
            plottable = self.plottableAt(event.pos())
            if plottable is not None:
                x = self.xAxis.pixelToCoord(event.pos().x())
                y = self.yAxis.pixelToCoord(event.pos().y())
                bar = self.plottableBarsAt(event.pos())
                graph = self.plottableGraphAt(event.pos())
                if bar:
                    data = QCPBarData(bar.data()[3.0])
                    y = data.value
                    QToolTip.showText(event.globalPos(),
                                      QCoreApplication.translate('MousePlot',
                                                                 '<table>'
                                                                 '<tr>'
                                                                 '<th colspan="2">%s</th>'
                                                                 '</tr>'
                                                                 '<tr>'
                                                                 '<td>%s rub.</td>'
                                                                 '</tr>'
                                                                 '</table>' % (plottable.name(), str(y))))
                elif graph:
                    labels = self.xAxis.tickVectorLabels()
                    label_x = str(labels[int(x)])
                    y = round(y, 2)
                    QToolTip.showText(event.globalPos(),
                                      QCoreApplication.translate('MousePlot',
                                                                 '<table>'
                                                                 '<tr>'
                                                                 '<th colspan="2">%s</th>'
                                                                 '</tr>'
                                                                 '<tr>'
                                                                 '<td>%s: %s rub.</td>'
                                                                 '</tr>'
                                                                 '</table>' % (plottable.name(), label_x, str(y))))
        super().mousePressEvent(event)
