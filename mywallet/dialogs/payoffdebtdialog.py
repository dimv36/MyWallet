__author__ = 'dimv36'
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QDialog
from mywallet.ui.ui_payoffdebtdialog import Ui_PayOffDebtDialog


class PayOffDebtDialog(QDialog, Ui_PayOffDebtDialog):
    def __init__(self, current_debt, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._current_debt_value.setText(str(current_debt))
        self._button_box.button(self._button_box.Ok).setEnabled(False)
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self._comments_lineedit.textChanged.connect(self._on_comments_changed)

    @Slot()
    def _on_comments_changed(self):
        if self._comments_lineedit.text():
            self._button_box.button(self._button_box.Ok).setEnabled(True)

    def data(self):
        """
        :return: dict
        """
        return {
            'value': -1 * self._pay_off_combo_box.value(),
            'description': self._comments_lineedit.text()
        }
