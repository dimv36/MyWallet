#ifndef EDITINGTABLEDELEGATE_H
#define EDITINGTABLEDELEGATE_H

#include <QItemDelegate>
#include <QLineEdit>

#define SUM_INDEX 0
#define DESCRIPTION_INDEX 1

class EditingTableDelegate : public QItemDelegate
{
    Q_OBJECT
public:
    explicit EditingTableDelegate(QObject *parent = 0);

    QWidget* createEditor(QWidget *parent, const QStyleOptionViewItem &, const QModelIndex &) const;
    void setEditorData(QWidget *editor, const QModelIndex &index) const;
    void setModelData(QWidget *editor, QAbstractItemModel *model, const QModelIndex &index) const;
signals:

public slots:

};

#endif // EDITINGTABLEDELEGATE_H
