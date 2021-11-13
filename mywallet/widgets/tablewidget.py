__author__ = 'dimv36'
from PySide2.QtWidgets import QWidget, QTableWidgetItem, QItemDelegate, QDoubleSpinBox
from PySide2.QtCore import Qt, QLocale, Signal, Slot
from mywallet.ui.ui_tablewidget import Ui_TableWidget


class EditingDelegate(QItemDelegate):
    def __init__(self):
        super().__init__()
        self.__locale = QLocale(QLocale.English)

    def createEditor(self, parent, style=None, index=None):
        editor = QDoubleSpinBox(parent)
        editor.setMinimum(0.01)
        editor.setMaximum(10000000.00)
        editor.setLocale(self.__locale)
        return editor

    def setModelData(self, editor, model, index):
        text = str(editor.value())
        text += '0' if len(text.split(self.__locale.decimalPoint())[-1]) == 1 else ''
        model.setData(index, text, Qt.EditRole)

    def setEditorData(self, editor, index):
        if index.model().data(index, Qt.EditRole) is None:
            return
        value = float(index.model().data(index, Qt.EditRole))
        editor.setValue(value)


class TableWidget(QWidget):
    signal_table_was_updated = Signal()

    def __init__(self, parent=None, *args, **kwargs):
        super(TableWidget, self).__init__(parent)
        self.ui = Ui_TableWidget()
        self.ui.setupUi(self)
        self.__init_signal_slots()

    def __init_signal_slots(self):
        self.signal_table_was_updated.connect(self._on_update)
        self.ui.table.cellChanged.connect(self._on_cell_changed)
        self.ui.add_button.clicked.connect(self._on_add_button_clicked)
        self.ui.delete_button.clicked.connect(self._on_delete_button_clicked)

    def __is_table_has_rows(self):
        return self.ui.table.rowCount()

    def set_title(self, title):
        self.ui.group_box.setTitle(title)

    def is_data_correct(self):
        for i in range(0, self.ui.table.rowCount()):
            for j in range(0, self.ui.table.columnCount()):
                item = self.ui.table.item(i, j)
                try:
                    if not item.text():
                        return False
                except AttributeError:
                    return False
        return True

    def get_rows(self):
        result = []
        for i in range(0, self.ui.table.rowCount()):
            row = {
                'value': float(self.ui.table.item(i, 0).text()),
                'description': self.ui.table.item(i, 1).text()
            }
            result.append(row)
        return result

    # Получить число строк виджета
    def row_count(self):
        return self.ui.table.rowCount()

    # Слот обработки сигнала на изменение текущей ячейки таблицы
    @Slot(int, int)
    def _on_cell_changed(self, row, column):
        item = self.ui.table.item(row, column)
        if item is not None:
            item.setSelected(False)
        self.signal_table_was_updated.emit()

    # Слот обработки сигнала на нажатие кнопки добавления
    @Slot()
    def _on_add_button_clicked(self):
        self.ui.table.clearSelection()
        current_row = self.ui.table.currentRow()
        self.ui.table.insertRow(current_row + 1)
        current_row += 1
        for i in range(0, self.ui.table.columnCount()):
            self.ui.table.setItem(current_row, i, QTableWidgetItem())
        self.ui.table.scrollToBottom()
        self.ui.table.setItemDelegateForColumn(0, EditingDelegate())
        self.signal_table_was_updated.emit()

    # Слот обработки сигнала на нажатие кнопки удаления
    @Slot()
    def _on_delete_button_clicked(self):
        selected_items = self.ui.table.selectedItems()
        if not selected_items:
            self.ui.table.clearSelection()
            return

        item = selected_items[0]
        if item.isSelected():
            self.ui.table.removeRow(item.row())
            self.ui.table.clearSelection()
            self.signal_table_was_updated.emit()

    # Слот обработки сигнала на обновление формы
    @Slot()
    def _on_update(self):
        self.ui.delete_button.setEnabled(self.__is_table_has_rows())
