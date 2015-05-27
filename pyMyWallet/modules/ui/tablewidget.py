__author__ = 'dimv36'
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QItemDelegate, QDoubleSpinBox
from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal, Qt, QCoreApplication, QLocale

from modules.ui.ui_tablewidget import Ui_TableWidget


class EditingDelegate(QItemDelegate):
    def __init__(self):
        super().__init__()

    def createEditor(self, parent, style=None, index=None):
        editor = QDoubleSpinBox(parent)
        editor.setMinimum(0.01)
        editor.setMaximum(1000000.00)
        editor.setLocale(QLocale(QLocale.English))
        return editor

    def setModelData(self, editor, model, index):
        text = str(editor.value())
        model.setData(index, text, Qt.EditRole)

    def setEditorData(self, editor, index):
        if index.model().data(index, Qt.EditRole) is None:
            return
        value = float(index.model().data(index, Qt.EditRole))
        editor.setValue(value)


class TableWidget(QWidget, Ui_TableWidget):
    tr = QCoreApplication.translate

    class Communicate(QObject):
        signal_table_was_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.signals = self.Communicate()
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self.signals.signal_table_was_updated.connect(self.__on_update)
        self._table.pyqtConfigure(cellChanged=self.__on_cell_changed)
        self._add_button.pyqtConfigure(clicked=self.__on_add_button_clicked)
        self._delete_button.pyqtConfigure(clicked=self.__on_delete_button_clicked)

    def __is_table_has_rows(self):
        return self._table.rowCount() and self.is_data_correct()

    def set_title(self, title):
        self._group_box.setTitle(self.tr('TableWidget', title))

    def is_data_correct(self):
        for i in range(0, self._table.rowCount()):
            for j in range(0, self._table.columnCount()):
                item = self._table.item(i, j)
                try:
                    if not item.text():
                        return False
                except AttributeError:
                    return False
        return True

    def get_rows(self):
        result = []
        for i in range(0, self._table.rowCount()):
            row = (self._table.item(i, 0).text(), self._table.item(i, 1).text())
            result.append(row)
        return result

    # Слот обработки сигнала на изменение текущей ячейки таблицы
    @pyqtSlot(int, int)
    def __on_cell_changed(self, row, column):
        item = self._table.item(row, column)
        if item is not None:
            item.setSelected(False)
        self.signals.signal_table_was_updated.emit()
        pass

    # Слот обработки сигнала на нажатие кнопки добавления
    @pyqtSlot()
    def __on_add_button_clicked(self):
        current_row = self._table.currentRow()
        self._table.insertRow(current_row + 1)
        for i in range(0, self._table.columnCount()):
            self._table.setItem(current_row, i, QTableWidgetItem())
        self._table.scrollToBottom()
        self._table.setItemDelegateForColumn(0, EditingDelegate())

    # Слот обработки сигнала на нажатие кнопки удаления
    @pyqtSlot()
    def __on_delete_button_clicked(self):
        current_row = self._table.currentRow()
        if current_row < 0:
            return

        item = self._table.item(current_row, 0)
        if item.isSelected():
            self._table.removeRow(current_row)
            self.signals.signal_table_was_updated.emit()

    # Слот обработки сигнала на обновление формы
    @pyqtSlot()
    def __on_update(self):
        self._delete_button.setEnabled(self.__is_table_has_rows())