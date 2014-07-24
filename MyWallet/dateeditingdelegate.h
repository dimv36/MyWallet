#ifndef DATEEDITINGDELEGATE_H
#define DATEEDITINGDELEGATE_H

#include <QItemDelegate>
#include <QDateEdit>
#define DATE_FORMAT "d MMMM yyyy"

class DateEditingDelegate : public QItemDelegate
{
    Q_OBJECT
public:
    explicit DateEditingDelegate(QObject *parent = 0);

    QWidget* createEditor(QWidget *parent, const QStyleOptionViewItem &, const QModelIndex &) const;
    void setEditorData(QWidget *editor, const QModelIndex &index) const;
    void setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const;
signals:

public slots:

};

#endif // DATEEDITINGDELEGATE_H
