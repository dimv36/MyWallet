#ifndef TABLEWIDGET_H
#define TABLEWIDGET_H

#include <QWidget>
#include <QPushButton>
#include "editingtabledelegate.h"

namespace Ui {
class TableWidget;
}

class TableWidget : public QWidget {
    Q_OBJECT

private:
    Ui::TableWidget *_ui;
    bool _is_enabled;

public:
    explicit TableWidget(QWidget *parent = 0);
    ~TableWidget();

private slots:
    void on__add_button_clicked();
    void on__delete_button_clicked();
    void SlotUpdateTable(int, int);

signals:
    void SignalTableWasChanged();

};

#endif // TABLEWIDGET_H
