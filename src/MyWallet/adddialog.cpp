#include "adddialog.h"
#include "ui_adddialog.h"

AddDialog::AddDialog(QWidget *parent) :
    QDialog(parent),
    _ui(new Ui::AddDialog) {
    _ui -> setupUi(this);
    _ui -> _date -> setDate(QDate::currentDate());
    _ui -> _button_box -> button(_ui -> _button_box -> Ok) -> setEnabled(false);
}


AddDialog::~AddDialog() {
    delete _ui;
}

