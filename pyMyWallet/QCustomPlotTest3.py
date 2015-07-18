#!/usr/bin/python3
__author__ = 'dimv36'

import sys
from PyQt5.QtCore import Qt, QLocale, QDateTime, qrand
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor, QPen, QBrush, QFont
from qcustomplot.qcustomplot import QCustomPlot, QCPGraph, QCPAxis, QCPScatterStyle

if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = QCustomPlot()

    # set locale to english, so we get english month names:
    w.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
    # seconds of current time, we'll use it as starting point in time for data:
    # create multiple graphs:
    w.addGraph()
    datax = [1414789200, 1417381200]
    datay = [15860.0, 23042.0, 13550.0, 33285.0, 39097.0, 39097.0, 28854.91]
    labels = ['', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul']
    w.graph(0).setData(datax,
                      datay)
    w.xAxis.setTickVectorLabels(labels)
    # configure bottom axis to show date and time instead of number:
    # set a fixed tick-step to one tick per month:
    # w.xAxis.setAutoTickStep(False)
    # w.xAxis.setAutoTicks(False)
    w.xAxis.setAutoTickLabels(False)
    # w.xAxis.setTickLabelPadding(0)
    # w.xAxis.setSubTickCount(0)
    # set axis labels:
    w.xAxis.setLabel("Date")
    w.yAxis.setLabel("Random wobbly lines value")
    # make top and right axes visible but without ticks and labels:
    # set axis ranges to show all data:
    w.xAxis.setRange(0, 7.1)
    w.yAxis.setRange(0, 50000)
    w.graph().setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCrossCircle, 4))
    # show legend:
    w.legend.setVisible(True)
    w.show()

    sys.exit(app.exec())
