#include "tablewidget.h"
#include "ui_tablewidget.h"

TableWidget::TableWidget(QWidget *parent) :
    QWidget(parent),
    _ui(new Ui::TableWidget) {
    _ui -> setupUi(this);
    _ui -> _table -> setItemDelegate(new EditingTableDelegate());
    connect(_ui -> _table, SIGNAL(cellPressed(int,int)), this, SLOT(SlotUpdateTable(int, int)));
    _is_enabled = true;
}


TableWidget::~TableWidget() {
    delete _ui;
}


void TableWidget::on__add_button_clicked() {
    _ui -> _table -> insertRow(_ui -> _table -> rowCount());
}


void TableWidget::on__delete_button_clicked() {
    int current_row = _ui -> _table -> currentRow();
    if (current_row < 0)
        return;

    QTableWidgetItem *item = _ui -> _table -> item(current_row, 0);

    if (true == item -> isSelected())
        _ui -> _table -> removeRow(current_row);
}


void TableWidget::SlotUpdateTable(int /*row*/, int /*column*/) {
    for (int i = 0; i < _ui -> _table -> rowCount(); i++) {
        for (int j = 0; j < _ui -> _table -> columnCount(); j++) {
            QTableWidgetItem *item = _ui -> _table -> item(i, j);
            if (true == item -> text().isEmpty()) {
                _ui -> _delete_button -> setEnabled(false);
                return;
            }
        }
    }
    _ui -> _delete_button -> setEnabled(true);
}
