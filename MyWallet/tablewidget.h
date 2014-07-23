#ifndef TABLEWIDGET_H
#define TABLEWIDGET_H

#include <QWidget>
#include <QPushButton>
#include "editingtabledelegate.h"
#include <QDebug>

#define INDEX_SUM 0
#define INDEX_DESCRIPTION 1

namespace Ui {
class TableWidget;
}

class TableWidget : public QWidget {
    Q_OBJECT

private:
    Ui::TableWidget *_ui;

public:
    explicit TableWidget(QWidget *parent = 0);
    ~TableWidget();
    bool IsDataCorrect() const;
    bool IsTableEnabled() const;

    void set_title(const QString title);
    QList<QPair<QString, QString> > get_rows() const;

private:
    QPair<QString, QString> get_row(int row) const;

private slots:
    void on__add_button_clicked();
    void on__delete_button_clicked();
    void SlotCellChanged(int row, int column);

signals:
    void SignalTableWasUpdated();
};

#endif // TABLEWIDGET_H
