#include "adddialog.h"
#include "ui_adddialog.h"

AddDialog::AddDialog(QWidget *parent) :
    QDialog(parent),
    _ui(new Ui::AddDialog) {
    _ui -> setupUi(this);
    _ui -> _date -> setDate(QDate::currentDate());
    _ui -> _rest_value -> setValidator(new QIntValidator());
    _ui -> _income_value -> setValidator(new QIntValidator());
    _ui -> _button_box -> button(_ui -> _button_box -> Ok) -> setEnabled(false);

    connect(_ui -> _rest_value, SIGNAL(textChanged(QString)), this, SLOT(SlotUpdateForm()));
    connect(_ui -> _rest_descripton, SIGNAL(textChanged()), this, SLOT(SlotUpdateForm()));
    connect(_ui -> _income_value, SIGNAL(textChanged(QString)), this, SLOT(SlotUpdateForm()));
    connect(_ui -> _income_description, SIGNAL(textChanged()), this, SLOT(SlotUpdateForm()));
}


AddDialog::~AddDialog() {
    delete _ui;
}


QDate AddDialog::get_date() const {
    return _ui -> _date -> date();
}


int AddDialog::get_rest() const {
    return _ui -> _rest_value -> text().toInt();
}


QString AddDialog::get_rest_description() const {
    return _ui -> _rest_descripton -> toPlainText();
}


int AddDialog::get_income() const {
    return _ui -> _income_value -> text().toInt();
}


QString AddDialog::get_income_description() const {
    return _ui -> _income_description -> toPlainText();
}


bool AddDialog::IsRestFieldsActive() const {
    return _ui -> _rest_box -> isChecked();
}


bool AddDialog::IsIncomeFieldsActive() const {
    return _ui -> _income_box -> isChecked();
}


bool AddDialog::IsDataEntered() const {
    return ((false == _ui -> _rest_value -> text().isEmpty() &&
            false == _ui -> _rest_descripton -> toPlainText().isEmpty()) ||
            (false == _ui -> _income_value -> text().isEmpty() &&
             false == _ui -> _income_description -> toPlainText().isEmpty()));
}


void AddDialog::SlotUpdateForm() {
    _ui -> _button_box -> button(_ui -> _button_box -> Ok) -> setEnabled(IsDataEntered());
}
