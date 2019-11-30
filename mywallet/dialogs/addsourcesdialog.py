__author__ = 'dimv36'
from PySide2.QtCore import QDate, Slot
from PySide2.QtWidgets import QDialog
from mywallet.ui.ui_addsourcesdialog import Ui_AddSourcesDialog


class AddSourcesDialog(QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(AddSourcesDialog, self).__init__(parent)
        self.ui = Ui_AddSourcesDialog()
        self.ui.setupUi(self)
        self.ui.date.setDate(QDate.currentDate())
        # Делаем неактивной кнопку Ok формы
        self.ui.button_box.button(self.ui.button_box.Ok).setEnabled(False)
        # Устанавливаем заголовки виджетам источников
        self.ui.incoming.set_title(self.tr('Incoming'))
        self.ui.expense.set_title(self.tr('Expense'))
        self.ui.savings.set_title(self.tr('Savings'))
        self.ui.debt.set_title(self.tr('Debt'))
        # Подключаем сигналы к слотам
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self.ui.incoming.signal_table_was_updated.connect(self._on_update_form)
        self.ui.expense.signal_table_was_updated.connect(self._on_update_form)
        self.ui.savings.signal_table_was_updated.connect(self._on_update_form)
        self.ui.debt.signal_table_was_updated.connect(self._on_update_form)

    def date(self):
        return self.ui.date.date()

    def incoming(self):
        return self.ui.incoming.get_rows()

    def expense(self):
        return self.ui.expense.get_rows()

    def savings(self):
        return self.ui.savings.get_rows()

    def debt(self):
        return self.ui.debt.get_rows()

    # Слот обработки изменения формы
    @Slot()
    def _on_update_form(self):
        enabled = (self.ui.incoming.is_data_correct() and
                   self.ui.expense.is_data_correct() and
                   self.ui.savings.is_data_correct() and
                   self.ui.debt.is_data_correct() and
                   (self.ui.incoming.row_count() or
                    self.ui.expense.row_count() or
                    self.ui.savings.row_count() or
                    self.ui.debt.row_count()))
        self.ui.button_box.button(self.ui.button_box.Ok).setEnabled(enabled)
