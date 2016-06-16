# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addsourcesdialog.ui'
#
# Created by: PyQt5 UI code generator 5.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddSourcesDialog(object):
    def setupUi(self, AddSourcesDialog):
        AddSourcesDialog.setObjectName("AddSourcesDialog")
        AddSourcesDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        AddSourcesDialog.resize(656, 520)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddSourcesDialog.sizePolicy().hasHeightForWidth())
        AddSourcesDialog.setSizePolicy(sizePolicy)
        AddSourcesDialog.setMinimumSize(QtCore.QSize(0, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/kwallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        AddSourcesDialog.setWindowIcon(icon)
        AddSourcesDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(AddSourcesDialog)
        self.gridLayout.setObjectName("gridLayout")
        self._button_box = QtWidgets.QDialogButtonBox(AddSourcesDialog)
        self._button_box.setOrientation(QtCore.Qt.Horizontal)
        self._button_box.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self._button_box.setCenterButtons(False)
        self._button_box.setObjectName("_button_box")
        self.gridLayout.addWidget(self._button_box, 7, 3, 1, 1)
        self._incoming = TableWidget()
        self._incoming.setObjectName("_incoming")
        self.gridLayout.addWidget(self._incoming, 4, 1, 1, 3)
        self._expense = TableWidget()
        self._expense.setObjectName("_expense")
        self.gridLayout.addWidget(self._expense, 2, 1, 1, 3)
        self._debt = TableWidget()
        self._debt.setObjectName("_debt")
        self.gridLayout.addWidget(self._debt, 6, 1, 1, 3)
        self._date = QtWidgets.QDateEdit(AddSourcesDialog)
        self._date.setObjectName("_date")
        self.gridLayout.addWidget(self._date, 0, 2, 1, 1)
        self._label_date = QtWidgets.QLabel(AddSourcesDialog)
        self._label_date.setObjectName("_label_date")
        self.gridLayout.addWidget(self._label_date, 0, 1, 1, 1)
        self._savings = TableWidget()
        self._savings.setObjectName("_savings")
        self.gridLayout.addWidget(self._savings, 3, 1, 1, 3)

        self.retranslateUi(AddSourcesDialog)
        self._button_box.accepted.connect(AddSourcesDialog.accept)
        self._button_box.rejected.connect(AddSourcesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddSourcesDialog)

    def retranslateUi(self, AddSourcesDialog):
        _translate = QtCore.QCoreApplication.translate
        AddSourcesDialog.setWindowTitle(_translate("AddSourcesDialog", "Add sources"))
        self._date.setDisplayFormat(_translate("AddSourcesDialog", "d MMMM yyyy"))
        self._label_date.setText(_translate("AddSourcesDialog", "Date:"))

from modules.ui.tablewidget import TableWidget
import modules.resources.resource_rc
