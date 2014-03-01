#include "restmonthdialog.h"
#include "ui_restmonthdialog.h"

RestMonthDialog::RestMonthDialog(QWidget *parent) :
    QDialog(parent),
    _ui(new Ui::RestMonthDialog) {
    _ui -> setupUi(this);
    _ui -> _value -> setValidator(new QIntValidator());
}


RestMonthDialog::~RestMonthDialog() {
    delete _ui;
}


void RestMonthDialog::set_rest_month(int rest) {
    _ui -> _value -> setText(QString::number(rest));
}


int RestMonthDialog::get_rest_month() const {
    return _ui -> _value -> text().toInt();
}
