__author__ = 'dimv36'
from PySide2.QtCore import Slot
from PySide2.QtWidgets import QDialog
from mywallet.ui.ui_savingstoincomingdialog import Ui_SavingsToIncomingDialog


class SavingsToIncomingDialog(QDialog, Ui_SavingsToIncomingDialog):
    def __init__(self, savings, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._available_savings_value.setText(str(savings))
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
            'value': -1 * self._convert_to_incoming_combo_box.value(),
            'description': self._comments_lineedit.text()
        }
