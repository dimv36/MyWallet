__author__ = 'dimv36'
from PyQt5.QtWidgets import QDialog

from ui.ui_changemonthbalance import Ui_ChangeMonthDialog


class ChangeMonthBalance(QDialog, Ui_ChangeMonthDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def set_month_balance(self, balance):
        self._value.setValue(balance)

    def balance(self):
        return self._value.text()