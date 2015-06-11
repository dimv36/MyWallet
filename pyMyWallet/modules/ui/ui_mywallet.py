# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mywallet.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MyWallet(object):
    def setupUi(self, MyWallet):
        MyWallet.setObjectName("MyWallet")
        MyWallet.resize(800, 600)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/kwallet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MyWallet.setWindowIcon(icon)
        self._central_widget = QtWidgets.QWidget(MyWallet)
        self._central_widget.setObjectName("_central_widget")
        self._main_layout = QtWidgets.QGridLayout(self._central_widget)
        self._main_layout.setObjectName("_main_layout")
        self._view = QtWidgets.QTableView(self._central_widget)
        self._view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self._view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._view.setObjectName("_view")
        self._main_layout.addWidget(self._view, 0, 0, 1, 2)
        self._label_balance = QtWidgets.QLabel(self._central_widget)
        self._label_balance.setObjectName("_label_balance")
        self._main_layout.addWidget(self._label_balance, 1, 0, 1, 1)
        self._label_expense_value = QtWidgets.QLabel(self._central_widget)
        self._label_expense_value.setObjectName("_label_expense_value")
        self._main_layout.addWidget(self._label_expense_value, 2, 1, 1, 1)
        self._label_total_value = QtWidgets.QLabel(self._central_widget)
        self._label_total_value.setObjectName("_label_total_value")
        self._main_layout.addWidget(self._label_total_value, 6, 1, 1, 1)
        self._label_incoming = QtWidgets.QLabel(self._central_widget)
        self._label_incoming.setObjectName("_label_incoming")
        self._main_layout.addWidget(self._label_incoming, 3, 0, 1, 1)
        self._label_total = QtWidgets.QLabel(self._central_widget)
        self._label_total.setObjectName("_label_total")
        self._main_layout.addWidget(self._label_total, 6, 0, 1, 1)
        self._label_expense = QtWidgets.QLabel(self._central_widget)
        self._label_expense.setObjectName("_label_expense")
        self._main_layout.addWidget(self._label_expense, 2, 0, 1, 1)
        self._label_incoming_value = QtWidgets.QLabel(self._central_widget)
        self._label_incoming_value.setObjectName("_label_incoming_value")
        self._main_layout.addWidget(self._label_incoming_value, 3, 1, 1, 1)
        self._label_balance_value = QtWidgets.QLabel(self._central_widget)
        self._label_balance_value.setObjectName("_label_balance_value")
        self._main_layout.addWidget(self._label_balance_value, 1, 1, 1, 1)
        self._label_loan = QtWidgets.QLabel(self._central_widget)
        self._label_loan.setObjectName("_label_loan")
        self._main_layout.addWidget(self._label_loan, 4, 0, 1, 1)
        self._label_debt = QtWidgets.QLabel(self._central_widget)
        self._label_debt.setObjectName("_label_debt")
        self._main_layout.addWidget(self._label_debt, 5, 0, 1, 1)
        self._label_loan_value = QtWidgets.QLabel(self._central_widget)
        self._label_loan_value.setObjectName("_label_loan_value")
        self._main_layout.addWidget(self._label_loan_value, 4, 1, 1, 1)
        self._label_debt_value = QtWidgets.QLabel(self._central_widget)
        self._label_debt_value.setObjectName("_label_debt_value")
        self._main_layout.addWidget(self._label_debt_value, 5, 1, 1, 1)
        MyWallet.setCentralWidget(self._central_widget)
        self._main_menu = QtWidgets.QMenuBar(MyWallet)
        self._main_menu.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self._main_menu.setObjectName("_main_menu")
        self._menu_file = QtWidgets.QMenu(self._main_menu)
        self._menu_file.setObjectName("_menu_file")
        self._menu_wallet = QtWidgets.QMenu(self._main_menu)
        self._menu_wallet.setObjectName("_menu_wallet")
        MyWallet.setMenuBar(self._main_menu)
        self._main_tool_bar = QtWidgets.QToolBar(MyWallet)
        self._main_tool_bar.setObjectName("_main_tool_bar")
        MyWallet.addToolBar(QtCore.Qt.TopToolBarArea, self._main_tool_bar)
        self._action_open_wallet = QtWidgets.QAction(MyWallet)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/folder_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._action_open_wallet.setIcon(icon1)
        self._action_open_wallet.setObjectName("_action_open_wallet")
        self._action_exit = QtWidgets.QAction(MyWallet)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._action_exit.setIcon(icon2)
        self._action_exit.setObjectName("_action_exit")
        self._action_add_item = QtWidgets.QAction(MyWallet)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/edit_add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._action_add_item.setIcon(icon3)
        self._action_add_item.setObjectName("_action_add_item")
        self._action_delete_item = QtWidgets.QAction(MyWallet)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/edit_remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._action_delete_item.setIcon(icon4)
        self._action_delete_item.setObjectName("_action_delete_item")
        self._action_settings = QtWidgets.QAction(MyWallet)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/kservices.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._action_settings.setIcon(icon5)
        self._action_settings.setObjectName("_action_settings")
        self._action_show_statistic = QtWidgets.QAction(MyWallet)
        self._action_show_statistic.setObjectName("_action_show_statistic")
        self._action_change_balance = QtWidgets.QAction(MyWallet)
        self._action_change_balance.setObjectName("_action_change_balance")
        self._action_new_wallet = QtWidgets.QAction(MyWallet)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._action_new_wallet.setIcon(icon6)
        self._action_new_wallet.setObjectName("_action_new_wallet")
        self._action_about = QtWidgets.QAction(MyWallet)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/info.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self._action_about.setIcon(icon7)
        self._action_about.setObjectName("_action_about")
        self._menu_file.addAction(self._action_new_wallet)
        self._menu_file.addAction(self._action_open_wallet)
        self._menu_file.addAction(self._action_settings)
        self._menu_file.addSeparator()
        self._menu_file.addAction(self._action_about)
        self._menu_file.addSeparator()
        self._menu_file.addAction(self._action_exit)
        self._menu_wallet.addSeparator()
        self._menu_wallet.addAction(self._action_add_item)
        self._menu_wallet.addAction(self._action_delete_item)
        self._menu_wallet.addAction(self._action_change_balance)
        self._menu_wallet.addSeparator()
        self._menu_wallet.addAction(self._action_show_statistic)
        self._main_menu.addAction(self._menu_file.menuAction())
        self._main_menu.addAction(self._menu_wallet.menuAction())
        self._main_tool_bar.addAction(self._action_add_item)
        self._main_tool_bar.addAction(self._action_delete_item)
        self._main_tool_bar.addSeparator()
        self._main_tool_bar.addAction(self._action_settings)

        self.retranslateUi(MyWallet)
        QtCore.QMetaObject.connectSlotsByName(MyWallet)

    def retranslateUi(self, MyWallet):
        _translate = QtCore.QCoreApplication.translate
        MyWallet.setWindowTitle(_translate("MyWallet", "MyWallet"))
        self._label_balance.setText(_translate("MyWallet", "Balance at the beginning of month:"))
        self._label_expense_value.setText(_translate("MyWallet", "0"))
        self._label_total_value.setText(_translate("MyWallet", "0"))
        self._label_incoming.setText(_translate("MyWallet", "Incoming:"))
        self._label_total.setText(_translate("MyWallet", "In total:"))
        self._label_expense.setText(_translate("MyWallet", "Expense:"))
        self._label_incoming_value.setText(_translate("MyWallet", "0"))
        self._label_balance_value.setText(_translate("MyWallet", "0"))
        self._label_loan.setText(_translate("MyWallet", "Loan:"))
        self._label_debt.setText(_translate("MyWallet", "Debt:"))
        self._label_loan_value.setText(_translate("MyWallet", "0"))
        self._label_debt_value.setText(_translate("MyWallet", "0"))
        self._menu_file.setTitle(_translate("MyWallet", "File"))
        self._menu_wallet.setTitle(_translate("MyWallet", "Wallet"))
        self._main_tool_bar.setWindowTitle(_translate("MyWallet", "toolBar"))
        self._action_open_wallet.setText(_translate("MyWallet", "Open wallet"))
        self._action_exit.setText(_translate("MyWallet", "Exit"))
        self._action_add_item.setText(_translate("MyWallet", "Add item"))
        self._action_delete_item.setText(_translate("MyWallet", "Delete item"))
        self._action_settings.setText(_translate("MyWallet", "Settings"))
        self._action_show_statistic.setText(_translate("MyWallet", "Show statistic"))
        self._action_change_balance.setText(_translate("MyWallet", "Change balance"))
        self._action_new_wallet.setText(_translate("MyWallet", "New wallet"))
        self._action_about.setText(_translate("MyWallet", "About"))

import modules.resources.resource_rc
