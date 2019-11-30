__author__ = 'dimv36'
from PySide2.QtWidgets import QDialog
from mywallet.ui.ui_changemonthbalancedialog import Ui_ChangeMonthBalanceDialog


class ChangeMonthBalanceDialog(QDialog):
    def __init__(self, parent=None):
        super(ChangeMonthBalanceDialog, self).__init__(parent)
        self.ui = Ui_ChangeMonthBalanceDialog()
        self.ui.setupUi(self)

    def set_month_balance(self, balance):
        self.ui.value.setValue(balance)

    def balance(self):
        return float(self.ui.value.text())
