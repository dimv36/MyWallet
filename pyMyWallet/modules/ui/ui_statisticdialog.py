# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'statisticdialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_StatisticDialog(object):
    def setupUi(self, StatisticDialog):
        StatisticDialog.setObjectName("StatisticDialog")
        StatisticDialog.resize(816, 431)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/kwallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        StatisticDialog.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(StatisticDialog)
        self.gridLayout.setObjectName("gridLayout")
        self._buttons = QtWidgets.QDialogButtonBox(StatisticDialog)
        self._buttons.setOrientation(QtCore.Qt.Horizontal)
        self._buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self._buttons.setObjectName("_buttons")
        self.gridLayout.addWidget(self._buttons, 1, 1, 1, 1)
        self.splitter = QtWidgets.QSplitter(StatisticDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self._periods = QtWidgets.QTreeWidget(self.splitter)
        self._periods.setMinimumSize(QtCore.QSize(50, 0))
        self._periods.setMaximumSize(QtCore.QSize(250, 16777215))
        self._periods.setObjectName("_periods")
        self._graphic = QCustomPlot(self.splitter)
        self._graphic.setObjectName("_graphic")
        self.gridLayout.addWidget(self.splitter, 0, 1, 1, 1)

        self.retranslateUi(StatisticDialog)
        self._buttons.accepted.connect(StatisticDialog.accept)
        self._buttons.rejected.connect(StatisticDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StatisticDialog)

    def retranslateUi(self, StatisticDialog):
        _translate = QtCore.QCoreApplication.translate
        StatisticDialog.setWindowTitle(_translate("StatisticDialog", "Statistics"))
        self._periods.headerItem().setText(0, _translate("StatisticDialog", "Statistic periods"))

from qcustomplot import QCustomPlot
import resource_rc
