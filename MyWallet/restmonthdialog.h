#ifndef RESTMONTHDIALOG_H
#define RESTMONTHDIALOG_H

#include <QDialog>
#include <QPushButton>

namespace Ui {
class RestMonthDialog;
}

class RestMonthDialog : public QDialog
{
    Q_OBJECT

private:
    Ui::RestMonthDialog *_ui;

public:
    explicit RestMonthDialog(QWidget *parent = 0);
    ~RestMonthDialog();

    int get_rest_month() const;
    void set_rest_month(int rest);

};

#endif // RESTMONTHDIALOG_H
