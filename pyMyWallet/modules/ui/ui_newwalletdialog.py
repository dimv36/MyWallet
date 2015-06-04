# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newwalletdialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewWalletDialog(object):
    def setupUi(self, NewWalletDialog):
        NewWalletDialog.setObjectName("NewWalletDialog")
        NewWalletDialog.resize(434, 101)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/kwallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NewWalletDialog.setWindowIcon(icon)
        self._main_layout = QtWidgets.QVBoxLayout(NewWalletDialog)
        self._main_layout.setObjectName("_main_layout")
        self._grid_layout = QtWidgets.QGridLayout()
        self._grid_layout.setObjectName("_grid_layout")
        self._label_directory = QtWidgets.QLabel(NewWalletDialog)
        self._label_directory.setObjectName("_label_directory")
        self._grid_layout.addWidget(self._label_directory, 1, 0, 1, 1)
        self._label_wallet = QtWidgets.QLabel(NewWalletDialog)
        self._label_wallet.setObjectName("_label_wallet")
        self._grid_layout.addWidget(self._label_wallet, 0, 0, 1, 1)
        self._edit_directory = QtWidgets.QLineEdit(NewWalletDialog)
        self._edit_directory.setEnabled(False)
        self._edit_directory.setObjectName("_edit_directory")
        self._grid_layout.addWidget(self._edit_directory, 1, 1, 1, 1)
        self._edit_wallet = QtWidgets.QLineEdit(NewWalletDialog)
        self._edit_wallet.setObjectName("_edit_wallet")
        self._grid_layout.addWidget(self._edit_wallet, 0, 1, 1, 2)
        self._button_directory = QtWidgets.QPushButton(NewWalletDialog)
        self._button_directory.setObjectName("_button_directory")
        self._grid_layout.addWidget(self._button_directory, 1, 2, 1, 1)
        self._main_layout.addLayout(self._grid_layout)
        self._button_box = QtWidgets.QDialogButtonBox(NewWalletDialog)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self._button_box.setObjectName("_button_box")
        self._main_layout.addWidget(self._button_box)

        self.retranslateUi(NewWalletDialog)
        self._button_box.rejected.connect(NewWalletDialog.reject)
        self._button_box.accepted.connect(NewWalletDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(NewWalletDialog)

    def retranslateUi(self, NewWalletDialog):
        _translate = QtCore.QCoreApplication.translate
        NewWalletDialog.setWindowTitle(_translate("NewWalletDialog", "New wallet"))
        self._label_directory.setText(_translate("NewWalletDialog", "Directory"))
        self._label_wallet.setText(_translate("NewWalletDialog", "Wallet name"))
        self._button_directory.setText(_translate("NewWalletDialog", "Change..."))

import modules.resources.resource_rc