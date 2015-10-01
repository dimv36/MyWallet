# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'savingstoincomingdialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SavingsToIncomingDialog(object):
    def setupUi(self, SavingsToIncomingDialog):
        SavingsToIncomingDialog.setObjectName("SavingsToIncomingDialog")
        SavingsToIncomingDialog.resize(400, 121)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../resources/kwallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SavingsToIncomingDialog.setWindowIcon(icon)
        self._main_layout = QtWidgets.QFormLayout(SavingsToIncomingDialog)
        self._main_layout.setObjectName("_main_layout")
        self._convert_to_incoming_combo_box = QtWidgets.QDoubleSpinBox(SavingsToIncomingDialog)
        self._convert_to_incoming_combo_box.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self._convert_to_incoming_combo_box.setSuffix("")
        self._convert_to_incoming_combo_box.setMinimum(0.01)
        self._convert_to_incoming_combo_box.setMaximum(100000.0)
        self._convert_to_incoming_combo_box.setObjectName("_convert_to_incoming_combo_box")
        self._main_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self._convert_to_incoming_combo_box)
        self._comments_label = QtWidgets.QLabel(SavingsToIncomingDialog)
        self._comments_label.setObjectName("_comments_label")
        self._main_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._comments_label)
        self._comments_lineedit = QtWidgets.QLineEdit(SavingsToIncomingDialog)
        self._comments_lineedit.setObjectName("_comments_lineedit")
        self._main_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self._comments_lineedit)
        self._button_box = QtWidgets.QDialogButtonBox(SavingsToIncomingDialog)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self._button_box.setObjectName("_button_box")
        self._main_layout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self._button_box)
        self._available_savings_value = QtWidgets.QLabel(SavingsToIncomingDialog)
        self._available_savings_value.setText("")
        self._available_savings_value.setObjectName("_available_savings_value")
        self._main_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self._available_savings_value)
        self._available_savings_label = QtWidgets.QLabel(SavingsToIncomingDialog)
        self._available_savings_label.setObjectName("_available_savings_label")
        self._main_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._available_savings_label)
        self._convert_to_incoming_label = QtWidgets.QLabel(SavingsToIncomingDialog)
        self._convert_to_incoming_label.setObjectName("_convert_to_incoming_label")
        self._main_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._convert_to_incoming_label)

        self.retranslateUi(SavingsToIncomingDialog)
        self._button_box.accepted.connect(SavingsToIncomingDialog.accept)
        self._button_box.rejected.connect(SavingsToIncomingDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SavingsToIncomingDialog)

    def retranslateUi(self, SavingsToIncomingDialog):
        _translate = QtCore.QCoreApplication.translate
        SavingsToIncomingDialog.setWindowTitle(_translate("SavingsToIncomingDialog", "Savings to incoming"))
        self._comments_label.setText(_translate("SavingsToIncomingDialog", "Comments:"))
        self._available_savings_label.setText(_translate("SavingsToIncomingDialog", "Available savings:"))
        self._convert_to_incoming_label.setText(_translate("SavingsToIncomingDialog", "Convert to incoming:"))

