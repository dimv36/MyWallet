__author__ = 'dimv36'
from PyQt5.QtCore import QDate, pyqtSlot, QCoreApplication
from PyQt5.QtWidgets import QDialog

from modules.ui.ui_addsourcesdialog import Ui_AddSourcesDialog


class AddSourcesDialog(Ui_AddSourcesDialog, QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._date.setDate(QDate.currentDate())
        # Делаем неактивной кнопку Ok формы
        self._button_box.button(self._button_box.Ok).setEnabled(False)
        # Устанавливаем заголовки виджетам источников
        self._incoming.set_title(QCoreApplication.translate('AddSourcesDialog', 'Incoming'))
        self._expense.set_title(QCoreApplication.translate('AddSourcesDialog', 'Expense'))
        self._savings.set_title(QCoreApplication.translate('AddSourcesDialog', 'Savings'))
        self._loan.set_title(QCoreApplication.translate('AddSourcesDialog', 'Loan'))
        self._debt.set_title(QCoreApplication.translate('AddSourcesDialog', 'Debt'))
        # Подключаем сигналы к слотам
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self._incoming.signals.signal_table_was_updated.connect(self.__on_update_form)
        self._expense.signals.signal_table_was_updated.connect(self.__on_update_form)
        self._savings.signals.signal_table_was_updated.connect(self.__on_update_form)
        self._loan.signals.signal_table_was_updated.connect(self.__on_update_form)
        self._debt.signals.signal_table_was_updated.connect(self.__on_update_form)

    def date(self):
        return self._date.date()

    def incoming(self):
        return self._incoming.get_rows()

    def expense(self):
        return self._expense.get_rows()

    def savings(self):
        return self._savings.get_rows()

    def loan(self):
        return self._loan.get_rows()

    def debt(self):
        return self._debt.get_rows()

    # Слот обработки изменения формы
    @pyqtSlot()
    def __on_update_form(self):
        enabled = self._incoming.is_data_correct() and self._expense.is_data_correct() \
                  and self._savings.is_data_correct() \
                  and self._loan.is_data_correct() and self._debt.is_data_correct() \
                  and (self._incoming.row_count() or self._expense.row_count()
                       or self._savings.row_count()
                       or self._loan.row_count() or self._debt.row_count())
        self._button_box.button(self._button_box.Ok).setEnabled(enabled)
