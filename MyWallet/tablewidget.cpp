#include "tablewidget.h"
#include "ui_tablewidget.h"

TableWidget::TableWidget(QWidget *parent) :
    QWidget(parent),
    _ui(new Ui::TableWidget) {
    _ui -> setupUi(this);
    connect(_ui -> _table, SIGNAL(cellChanged(int, int)), this, SLOT(SlotCellChanged(int, int)));
}


TableWidget::~TableWidget() {
    delete _ui;
}


void TableWidget::set_title(const QString title) {
    _ui -> _group_box -> setTitle(title);
}


void TableWidget::on__add_button_clicked() {
    int current_row = _ui -> _table -> rowCount();
    _ui -> _table -> insertRow(current_row);
    for (int i = 0; i < _ui -> _table -> columnCount(); i++)
        _ui -> _table -> setItem(current_row, i, new QTableWidgetItem());
    _ui -> _table -> setItemDelegateForColumn(INDEX_SUM, new EditingTableDelegate);
}


void TableWidget::on__delete_button_clicked() {
    int current_row = _ui -> _table -> currentRow();
    if (current_row < 0)
        return;

    QTableWidgetItem *item = _ui -> _table -> item(current_row, 0);

    if (true == item -> isSelected())
        _ui -> _table -> removeRow(current_row);
}


bool TableWidget::IsDataCorrect() const {
    for (int i = 0; i < _ui -> _table -> rowCount(); i++) {
        for (int j = 0; j < _ui -> _table -> columnCount(); j++) {
            QTableWidgetItem *item = _ui -> _table -> item(i, j);
            if (true == item -> text().isEmpty())
                return false;
        }
    }
    return true;
}


QPair<QString,QString> TableWidget::get_row(int row) const {
    return QPair<QString, QString>(_ui -> _table -> item(row, INDEX_SUM) -> text(), _ui -> _table -> item(row, INDEX_DESCRIPTION) -> text());
}


QList<QPair<QString, QString> > TableWidget::get_rows() const {
    QList<QPair<QString, QString> > result;
    for (int i = 0; i < _ui -> _table -> rowCount(); i++)
        result.push_back(get_row(i));
    return result;
}


void TableWidget::SlotCellChanged(int row, int column) {
    emit SignalTableWasUpdated();
    _ui -> _table -> item(row, column) -> setSelected(false);
}


bool TableWidget::IsTableEnabled() const {
    return _ui -> _group_box -> isChecked();
}
