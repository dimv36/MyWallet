__author__ = 'dimv36'
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog

from ui.ui_addsourcesdialog import Ui_AddSourcesDialog


class AddSourcesDialog(Ui_AddSourcesDialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._date.setDate(QDate.currentDate())