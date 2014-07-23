#include "adddialog.h"
#include "ui_adddialog.h"
#include <QDebug>

AddDialog::AddDialog(QWidget *parent) :
    QDialog(parent),
    _ui(new Ui::AddDialog) {
    _ui -> setupUi(this);
    _ui -> _date -> setDate(QDate::currentDate());

    _ui -> _button_box -> button(_ui -> _button_box -> Ok) -> setEnabled(false);
    _ui -> _button_box -> button(_ui -> _button_box -> Cancel) -> setText("Отмена");

    _ui -> _table_input -> set_title(tr("Доходы"));
    _ui -> _table_output -> set_title(tr("Расходы"));

    connect(_ui -> _table_input, SIGNAL(SignalTableWasUpdated()), this, SLOT(SlotUpdateForm()));
    connect(_ui -> _table_output, SIGNAL(SignalTableWasUpdated()), this, SLOT(SlotUpdateForm()));
}


AddDialog::~AddDialog() {
    delete _ui;
}


QDate AddDialog::get_date() const {
    return _ui -> _date -> date();
}


QList<QPair<QString, QString> > AddDialog::get_outputs() const {
    return _ui -> _table_output -> get_rows();
}


QList<QPair<QString, QString> > AddDialog::get_inputs() const {
    return _ui -> _table_input -> get_rows();
}


bool AddDialog::IsInputFieldsActive() const {
    return _ui -> _table_input -> IsTableEnabled();
}


bool AddDialog::IsOutputFieldsActive() const {
    return _ui -> _table_output -> IsTableEnabled();
}


void AddDialog::SlotUpdateForm() {
    bool is_enabled = _ui -> _table_input -> IsDataCorrect() && _ui -> _table_output -> IsDataCorrect();
    _ui -> _button_box -> button(_ui -> _button_box -> Ok) -> setEnabled(is_enabled);
}
