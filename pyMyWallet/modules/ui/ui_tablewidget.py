# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tablewidget.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TableWidget(object):
    def setupUi(self, TableWidget):
        TableWidget.setObjectName("TableWidget")
        TableWidget.setEnabled(True)
        TableWidget.resize(396, 291)
        self._main_layout = QtWidgets.QGridLayout(TableWidget)
        self._main_layout.setObjectName("_main_layout")
        self._group_box = QtWidgets.QGroupBox(TableWidget)
        self._group_box.setCheckable(True)
        self._group_box.setChecked(False)
        self._group_box.setObjectName("_group_box")
        self._grid_layout = QtWidgets.QGridLayout(self._group_box)
        self._grid_layout.setObjectName("_grid_layout")
        self._table = QtWidgets.QTableWidget(self._group_box)
        self._table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._table.setShowGrid(True)
        self._table.setObjectName("_table")
        self._table.setColumnCount(2)
        self._table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self._table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self._table.setHorizontalHeaderItem(1, item)
        self._table.horizontalHeader().setDefaultSectionSize(150)
        self._table.horizontalHeader().setStretchLastSection(True)
        self._grid_layout.addWidget(self._table, 0, 0, 1, 1)
        self._layout = QtWidgets.QHBoxLayout()
        self._layout.setObjectName("_layout")
        self._add_button = QtWidgets.QPushButton(self._group_box)
        self._add_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/edit_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._add_button.setIcon(icon)
        self._add_button.setObjectName("_add_button")
        self._layout.addWidget(self._add_button)
        self._delete_button = QtWidgets.QPushButton(self._group_box)
        self._delete_button.setEnabled(False)
        self._delete_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/edit_remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._delete_button.setIcon(icon1)
        self._delete_button.setObjectName("_delete_button")
        self._layout.addWidget(self._delete_button)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self._layout.addItem(spacerItem)
        self._grid_layout.addLayout(self._layout, 1, 0, 1, 1)
        self._main_layout.addWidget(self._group_box, 0, 0, 1, 1)

        self.retranslateUi(TableWidget)
        QtCore.QMetaObject.connectSlotsByName(TableWidget)

    def retranslateUi(self, TableWidget):
        _translate = QtCore.QCoreApplication.translate
        TableWidget.setWindowTitle(_translate("TableWidget", "Form"))
        self._group_box.setTitle(_translate("TableWidget", "GroupBox"))
        item = self._table.horizontalHeaderItem(0)
        item.setText(_translate("TableWidget", "Sum"))
        item = self._table.horizontalHeaderItem(1)
        item.setText(_translate("TableWidget", "Description"))

import modules.resources.resource_rc
