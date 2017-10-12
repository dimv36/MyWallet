# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'payoffdebtdialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_PayOffDebtDialog(object):
    def setupUi(self, PayOffDebtDialog):
        PayOffDebtDialog.setObjectName("PayOffDebtDialog")
        PayOffDebtDialog.resize(400, 121)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/kwallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PayOffDebtDialog.setWindowIcon(icon)
        self._main_layout = QtWidgets.QFormLayout(PayOffDebtDialog)
        self._main_layout.setObjectName("_main_layout")
        self._pay_off_label = QtWidgets.QLabel(PayOffDebtDialog)
        self._pay_off_label.setObjectName("_pay_off_label")
        self._main_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self._pay_off_label)
        self._pay_off_combo_box = QtWidgets.QDoubleSpinBox(PayOffDebtDialog)
        self._pay_off_combo_box.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self._pay_off_combo_box.setMinimum(0.01)
        self._pay_off_combo_box.setMaximum(100000.0)
        self._pay_off_combo_box.setObjectName("_pay_off_combo_box")
        self._main_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self._pay_off_combo_box)
        self._comments_label = QtWidgets.QLabel(PayOffDebtDialog)
        self._comments_label.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self._comments_label.setObjectName("_comments_label")
        self._main_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self._comments_label)
        self._comments_lineedit = QtWidgets.QLineEdit(PayOffDebtDialog)
        self._comments_lineedit.setObjectName("_comments_lineedit")
        self._main_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self._comments_lineedit)
        self._button_box = QtWidgets.QDialogButtonBox(PayOffDebtDialog)
        self._button_box.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self._button_box.setObjectName("_button_box")
        self._main_layout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self._button_box)
        self._current_debt_label = QtWidgets.QLabel(PayOffDebtDialog)
        self._current_debt_label.setObjectName("_current_debt_label")
        self._main_layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._current_debt_label)
        self._current_debt_value = QtWidgets.QLabel(PayOffDebtDialog)
        self._current_debt_value.setText("")
        self._current_debt_value.setObjectName("_current_debt_value")
        self._main_layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self._current_debt_value)

        self.retranslateUi(PayOffDebtDialog)
        self._button_box.accepted.connect(PayOffDebtDialog.accept)
        self._button_box.rejected.connect(PayOffDebtDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PayOffDebtDialog)

    def retranslateUi(self, PayOffDebtDialog):
        _translate = QtCore.QCoreApplication.translate
        PayOffDebtDialog.setWindowTitle(_translate("PayOffDebtDialog", "Pay off debt"))
        self._pay_off_label.setText(_translate("PayOffDebtDialog", "Pay off value:"))
        self._comments_label.setText(_translate("PayOffDebtDialog", "Comments:"))
        self._current_debt_label.setText(_translate("PayOffDebtDialog", "Current debt:"))
