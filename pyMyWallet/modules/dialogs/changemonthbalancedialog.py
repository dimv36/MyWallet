__author__ = 'dimv36'
from PyQt5.QtWidgets import QDialog

from modules.ui.ui_changemonthbalancedialog import Ui_ChangeMonthDialog


class ChangeMonthBalanceDialog(QDialog, Ui_ChangeMonthDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def set_month_balance(self, balance):
        self._value.setValue(balance)

    def balance(self):
        return float(self._value.text())
