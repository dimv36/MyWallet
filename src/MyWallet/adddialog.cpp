#include "adddialog.h"
#include "ui_adddialog.h"

AddDialog::AddDialog(QWidget *parent) :
    QDialog(parent),
    _ui(new Ui::AddDialog) {
    _ui -> setupUi(this);
    _ui -> _date -> setDate(QDate::currentDate());
    _ui -> _output_value -> setValidator(new QIntValidator());
    _ui -> _input_value -> setValidator(new QIntValidator());
    _ui -> _button_box -> button(_ui -> _button_box -> Ok) -> setEnabled(false);
    _ui -> _button_box -> button(_ui -> _button_box -> Cancel) -> setText("Отмена");

    connect(_ui -> _output_value, SIGNAL(textChanged(QString)), this, SLOT(SlotUpdateForm()));
    connect(_ui -> _output_descripton, SIGNAL(textChanged()), this, SLOT(SlotUpdateForm()));
    connect(_ui -> _input_value, SIGNAL(textChanged(QString)), this, SLOT(SlotUpdateForm()));
    connect(_ui -> _input_description, SIGNAL(textChanged()), this, SLOT(SlotUpdateForm()));
}


AddDialog::~AddDialog() {
    delete _ui;
}


QDate AddDialog::get_date() const {
    return _ui -> _date -> date();
}


int AddDialog::get_output() const {
    return _ui -> _output_value -> text().toInt();
}


QString AddDialog::get_output_description() const {
    return _ui -> _output_descripton -> toPlainText();
}


int AddDialog::get_input() const {
    return _ui -> _input_value -> text().toInt();
}


QString AddDialog::get_input_description() const {
    return _ui -> _input_description -> toPlainText();
}


bool AddDialog::IsOutputFieldsActive() const {
    return _ui -> _output_box -> isChecked();
}


bool AddDialog::IsInputFieldsActive() const {
    return _ui -> _input_box -> isChecked();
}


bool AddDialog::IsDataEntered() const {
    return ((false == _ui -> _output_value -> text().isEmpty() &&
            false == _ui -> _output_descripton -> toPlainText().isEmpty()) ||
            (false == _ui -> _input_value -> text().isEmpty() &&
             false == _ui -> _input_description -> toPlainText().isEmpty()));
}


void AddDialog::SlotUpdateForm() {
    _ui -> _button_box -> button(_ui -> _button_box -> Ok) -> setEnabled(IsDataEntered());
}
