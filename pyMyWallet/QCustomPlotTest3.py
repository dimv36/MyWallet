#!/usr/bin/python3
__author__ = 'dimv36'

import sys
from PyQt5.QtCore import Qt, QLocale, QDateTime, qrand
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor, QPen, QBrush, QFont
from qcustomplot.qcustomplot import QCustomPlot, QCPGraph, QCPAxis

if __name__ == '__main__':

    app = QApplication(sys.argv)

    w = QCustomPlot()

    # set locale to english, so we get english month names:
    w.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
    # seconds of current time, we'll use it as starting point in time for data:
    # create multiple graphs:
    w.addGraph()
    w.graph(0).setData([1420059600, 1422738000, 1425157200, 1427835600, 1430427600, 1433106000],
                      [1, 2, 3, 4, 5, 6])
    # configure bottom axis to show date and time instead of number:
    w.xAxis.setTickLabelType(QCPAxis.ltDateTime)
    w.xAxis.setDateTimeFormat("MMMM\nyyyy")
    # set a fixed tick-step to one tick per month:
    w.xAxis.setAutoTickStep(False)
    w.xAxis.setTickStep(2628000) # one month in seconds
    w.xAxis.setSubTickCount(3)
    # apply manual tick and tick label for left axis:
    w.yAxis.setAutoTicks(False)
    w.yAxis.setAutoTickLabels(False)
    w.yAxis.setTickVector([5, 55])
    w.yAxis.setTickVectorLabels(["Not so\nhigh", "Very\nhigh"])
    # set axis labels:
    w.xAxis.setLabel("Date")
    w.yAxis.setLabel("Random wobbly lines value")
    # make top and right axes visible but without ticks and labels:
    # set axis ranges to show all data:
    w.xAxis.setRange(1420059600, 1433106000)
    w.yAxis.setRange(0, 60)
    # show legend:
    w.legend.setVisible(True)
    w.show()

    sys.exit(app.exec())
