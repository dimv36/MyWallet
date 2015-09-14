# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'changemonthbalancedialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ChangeMonthDialog(object):
    def setupUi(self, ChangeMonthDialog):
        ChangeMonthDialog.setObjectName("ChangeMonthDialog")
        ChangeMonthDialog.resize(368, 71)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/kwallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ChangeMonthDialog.setWindowIcon(icon)
        self._main_layout = QtWidgets.QGridLayout(ChangeMonthDialog)
        self._main_layout.setObjectName("_main_layout")
        self._button_box = QtWidgets.QDialogButtonBox(ChangeMonthDialog)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self._button_box.setObjectName("_button_box")
        self._main_layout.addWidget(self._button_box, 1, 0, 1, 1)
        self._value = QtWidgets.QDoubleSpinBox(ChangeMonthDialog)
        self._value.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self._value.setMaximum(1000000.0)
        self._value.setObjectName("_value")
        self._main_layout.addWidget(self._value, 0, 0, 1, 1)

        self.retranslateUi(ChangeMonthDialog)
        self._button_box.accepted.connect(ChangeMonthDialog.accept)
        self._button_box.rejected.connect(ChangeMonthDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChangeMonthDialog)

    def retranslateUi(self, ChangeMonthDialog):
        _translate = QtCore.QCoreApplication.translate
        ChangeMonthDialog.setWindowTitle(_translate("ChangeMonthDialog", "Change month balance"))

import modules.resources.resource_rc
