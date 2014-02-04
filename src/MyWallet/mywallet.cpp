#include "mywallet.h"
#include "ui_mywallet.h"

#include <QDebug>
#define DATE_INDEX 0
#define REST_TOTAL 1
#define REST_DESCRIPTION 2
#define INCOME_TOTAL 3
#define INCOME_DESCRIPTION 4

MyWallet::MyWallet(QWidget *parent) :
    QMainWindow(parent),
    _ui(new Ui::MyWallet) {
    _ui -> setupUi(this);
}

MyWallet::~MyWallet() {
    delete _ui;
}


void MyWallet::CreateTableRow(QDate &date, int total, QString &description, bool isRest) {
    QTableWidgetItem *date_item = new QTableWidgetItem(date.toString("d MMMM yyyy"));
    QTableWidgetItem *total_item = new QTableWidgetItem(QString::number(total));
    QTableWidgetItem *description_item = new QTableWidgetItem(description);
    _ui -> _table -> setRowCount(_ui -> _table -> rowCount() + 1);
    int row_count = _ui -> _table -> rowCount() - 1;
    _ui -> _table -> setItem(row_count, DATE_INDEX, date_item);
    if (true == isRest) {
        _ui -> _table -> setItem(row_count, REST_TOTAL, total_item);
        _ui -> _table -> setItem(row_count, REST_DESCRIPTION, description_item);
    } else {
        _ui -> _table -> setItem(row_count, INCOME_TOTAL, total_item);
        _ui -> _table -> setItem(row_count, INCOME_DESCRIPTION, description_item);
    }
    delete date_item;
    delete total_item;
    delete description_item;
    _ui -> _table -> scrollToBottom();
}


void MyWallet::on__action_add_triggered() {
    AddDialog dialog(this);
    if (QDialog::Accepted == dialog.exec()) {
       bool is_rest_fields_active = dialog.IsRestFieldsActive();
       bool is_income_fields_active = dialog.IsIncomeFieldsActive();
       QDate date = dialog.get_date();
       if (true == is_rest_fields_active) {
           int rest = dialog.get_rest();
           QString rest_description = dialog.get_rest_description();
           CreateTableRow(date, rest, rest_description, true);
       }
       if (true == is_income_fields_active) {
            int income = dialog.get_income();
            QString income_description = dialog.get_income_description();
            CreateTableRow(date, income, income_description, false);
       }
    }
}
