__author__ = 'dimv36'
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from modules.ui.ui_savingstoincomingdialog import Ui_SavingsToIncomingDialog


class SavingsToIncomingDialog(QDialog, Ui_SavingsToIncomingDialog):
    def __init__(self, savings, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._available_savings_value.setText(str(savings))
        self._button_box.button(self._button_box.Ok).setEnabled(False)
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self._comments_lineedit.pyqtConfigure(textChanged=self.__on_comments_changed)

    @pyqtSlot()
    def __on_comments_changed(self):
        if self._comments_lineedit.text():
            self._button_box.button(self._button_box.Ok).setEnabled(True)

    def data(self):
        """
        :return: dict
        """
        return {
            'value': -1 * self._convert_to_incoming_combo_box.value(),
            'description': self._comments_lineedit.text()
        }
