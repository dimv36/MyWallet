__author__ = 'dimv36'
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QDialog
from mywallet.ui.ui_payoffdebtdialog import Ui_PayOffDebtDialog


class PayOffDebtDialog(QDialog):
    def __init__(self, current_debt, parent=None):
        super(PayOffDebtDialog, self).__init__(parent)
        self.ui = Ui_PayOffDebtDialog()
        self.ui.setupUi(self)
        self.ui.current_debt_value.setText(str(current_debt))
        self.ui.button_box.button(self.ui.button_box.Ok).setEnabled(False)
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self.ui.comments_lineedit.textChanged.connect(self._on_comments_changed)

    @Slot()
    def _on_comments_changed(self):
        if self.ui.comments_lineedit.text():
            self.ui.button_box.button(self.ui.button_box.Ok).setEnabled(True)

    def data(self):
        """
        :return: dict
        """
        return {
            'value': -1 * self.ui.pay_off_combo_box.value(),
            'description': self.ui.comments_lineedit.text()
        }
