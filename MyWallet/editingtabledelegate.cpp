#include "editingtabledelegate.h"

EditingTableDelegate::EditingTableDelegate(QObject *parent) :
    QItemDelegate(parent) {

}


QWidget* EditingTableDelegate::createEditor(QWidget *parent, const QStyleOptionViewItem &/*option*/, const QModelIndex &/*index*/) const {
    QLineEdit *editor = new QLineEdit(parent);
    editor -> setValidator(new QIntValidator());
    return editor;
}


void EditingTableDelegate::setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const {
    QLineEdit *line = static_cast<QLineEdit*>(editor);
    QString text = line -> text();
    model -> setData(index, text, Qt::EditRole);
}


void EditingTableDelegate::setEditorData(QWidget *editor, const QModelIndex &index) const {
    QString text = index.model() -> data(index, Qt::EditRole).toString();
    if (true == text.isEmpty())
        return;
    QLineEdit *line = static_cast<QLineEdit*>(editor);
    line -> setText(text);
}
