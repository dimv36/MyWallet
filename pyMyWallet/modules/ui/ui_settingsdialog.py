# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsdialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName("SettingsDialog")
        SettingsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        SettingsDialog.resize(488, 141)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/kwallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        SettingsDialog.setWindowIcon(icon)
        self._main_layout = QtWidgets.QGridLayout(SettingsDialog)
        self._main_layout.setObjectName("_main_layout")
        self._wallet_box = QtWidgets.QGroupBox(SettingsDialog)
        self._wallet_box.setCheckable(False)
        self._wallet_box.setChecked(False)
        self._wallet_box.setObjectName("_wallet_box")
        self._wallet_box_layout = QtWidgets.QGridLayout(self._wallet_box)
        self._wallet_box_layout.setObjectName("_wallet_box_layout")
        self._directory = QtWidgets.QLineEdit(self._wallet_box)
        self._directory.setObjectName("_directory")
        self._wallet_box_layout.addWidget(self._directory, 0, 1, 1, 2)
        self._wallet_name_label = QtWidgets.QLabel(self._wallet_box)
        self._wallet_name_label.setObjectName("_wallet_name_label")
        self._wallet_box_layout.addWidget(self._wallet_name_label, 1, 0, 1, 1)
        self._directory_label = QtWidgets.QLabel(self._wallet_box)
        self._directory_label.setObjectName("_directory_label")
        self._wallet_box_layout.addWidget(self._directory_label, 0, 0, 1, 1)
        self._directory_button = QtWidgets.QPushButton(self._wallet_box)
        self._directory_button.setObjectName("_directory_button")
        self._wallet_box_layout.addWidget(self._directory_button, 0, 3, 1, 1)
        self._wallet_name = QtWidgets.QLineEdit(self._wallet_box)
        self._wallet_name.setObjectName("_wallet_name")
        self._wallet_box_layout.addWidget(self._wallet_name, 1, 1, 1, 3)
        self._main_layout.addWidget(self._wallet_box, 0, 0, 1, 1)
        self._button_box = QtWidgets.QDialogButtonBox(SettingsDialog)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self._button_box.setObjectName("_button_box")
        self._main_layout.addWidget(self._button_box, 2, 0, 1, 1)

        self.retranslateUi(SettingsDialog)
        self._button_box.accepted.connect(SettingsDialog.accept)
        self._button_box.rejected.connect(SettingsDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        _translate = QtCore.QCoreApplication.translate
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings"))
        self._wallet_box.setTitle(_translate("SettingsDialog", "Wallet Settings"))
        self._wallet_name_label.setText(_translate("SettingsDialog", "Wallet"))
        self._directory_label.setText(_translate("SettingsDialog", "Directory"))
        self._directory_button.setText(_translate("SettingsDialog", "Change..."))

import modules.resources.resource_rc
