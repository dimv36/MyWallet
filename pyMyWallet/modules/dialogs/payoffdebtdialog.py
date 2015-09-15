__author__ = 'dimv36'
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from modules.ui.ui_payoffdebtdialog import Ui_PayOffDebtDialog


class PayOffDebtDialog(QDialog, Ui_PayOffDebtDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._button_box.button(self._button_box.Ok).setEnabled(False)
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self._comments_lineedit.pyqtConfigure(textChanged=self.__on_comments_changed)

    @pyqtSlot()
    def __on_comments_changed(self):
        if self._comments_lineedit.text():
            self._button_box.button(self._button_box.Ok).setEnabled(True)

    def data(self):
        return [-1 * self._pay_off_combo_box.value(), self._comments_lineedit.text()]
