#include "dateeditingdelegate.h"

DateEditingDelegate::DateEditingDelegate(QObject *parent) :
    QItemDelegate(parent) {

}


QWidget* DateEditingDelegate::createEditor(QWidget *parent, const QStyleOptionViewItem &/*option*/, const QModelIndex &/*index*/) const {
    QDateEdit *editor = new QDateEdit(parent);
    return editor;
}


void DateEditingDelegate::setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const {
    QDateEdit *date_edit = static_cast<QDateEdit*>(editor);
    QString date = date_edit -> date().toString(DATE_FORMAT);
    model -> setData(index, date, Qt::EditRole);
}


void DateEditingDelegate::setEditorData(QWidget *editor, const QModelIndex &index) const {
    QString text = index.model() -> data(index, Qt::EditRole).toString();
    if (true == text.isEmpty())
        return;
    QDateEdit *date_edit = static_cast<QDateEdit*>(editor);
    date_edit -> setDate(QDate::fromString(text, DATE_FORMAT));
}
