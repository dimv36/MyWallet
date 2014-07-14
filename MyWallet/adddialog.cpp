#include "adddialog.h"
#include "ui_adddialog.h"
#include <QDebug>

AddDialog::AddDialog(QWidget *parent) :
    QDialog(parent),
    _ui(new Ui::AddDialog) {
    _ui -> setupUi(this);
    _ui -> _date -> setDate(QDate::currentDate());
//    _ui -> _output_value -> setValidator(new QIntValidator());
//    _ui -> _input_value -> setValidator(new QIntValidator());
    _ui -> _button_box -> button(_ui -> _button_box -> Ok) -> setEnabled(false);
    _ui -> _button_box -> button(_ui -> _button_box -> Cancel) -> setText("Отмена");

//    connect(_ui -> _input_value, SIGNAL(textChanged(QString)), this, SLOT(SlotUpdateForm(QString)));
//    connect(_ui -> _input_description, SIGNAL(textChanged(QString)), this, SLOT(SlotUpdateForm(QString)));
//    connect(_ui -> _output_value, SIGNAL(textChanged(QString)), this, SLOT(SlotUpdateForm(QString)));
//    connect(_ui -> _output_description, SIGNAL(textChanged(QString)), this, SLOT(SlotUpdateForm(QString)));

//    _ui -> _input_table -> setItemDelegate(new EditingTableDelegate());
//    _ui -> _output_table -> setItemDelegate(new EditingTableDelegate());

//    connect(_ui -> _input_add_row_button, SIGNAL(clicked()), this, SLOT(SlotInputAddRow()));
//    connect(_ui -> _output_add_row_button, SIGNAL(clicked()), this, SLOT(SlotOutputAddRow()));

//    connect(_ui -> _input_delete_row_button, SIGNAL(clicked()), this, SLOT(SlotInputDeleteRow()));
//    connect(_ui -> _output_delete_row_button, SIGNAL(clicked()), this, SLOT(SlotOutputDeleteRow()));
}


AddDialog::~AddDialog() {
    delete _ui;
}


QDate AddDialog::get_date() const {
    return _ui -> _date -> date();
}


int AddDialog::get_output() const {
//    return _ui -> _output_value -> text().toInt();
}


QString AddDialog::get_output_description() const {
//    return _ui -> _output_description -> text();
}


int AddDialog::get_input() const {
//    return _ui -> _input_value -> text().toInt();
}


QString AddDialog::get_input_description() const {
//    return _ui -> _input_description -> text();
}


bool AddDialog::IsOutputFieldsActive() const {
    return _ui -> _output_box -> isChecked();
}


bool AddDialog::IsInputFieldsActive() const {
    return _ui -> _input_box -> isChecked();
}


bool AddDialog::IsDataEntered() const {
//    return ((false == _ui -> _output_value -> text().isEmpty() &&
//            false == _ui -> _output_description -> text().isEmpty()) ||
//            (false == _ui -> _input_value -> text().isEmpty() &&
//             false == _ui -> _input_description -> text().isEmpty()));
}


void AddDialog::SlotUpdateForm(QString) {
    _ui -> _button_box -> button(_ui -> _button_box -> Ok) -> setEnabled(IsDataEntered());
}
