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
    date_item -> setTextAlignment(Qt::AlignCenter);
    total_item -> setTextAlignment(Qt::AlignCenter);
    description_item -> setTextAlignment(Qt::AlignCenter);
    _ui -> _table -> setRowCount(_ui -> _table -> rowCount() + 1);
    int row_count = _ui -> _table -> rowCount() - 1;
    _ui -> _table -> setItem(row_count, DATE_INDEX, date_item);
    if (true == isRest) {
        _ui -> _table -> setItem(row_count, REST_TOTAL, total_item);
        _ui -> _table -> setItem(row_count, REST_DESCRIPTION, description_item);
        _ui -> _table -> setItem(row_count, INCOME_TOTAL, new QTableWidgetItem());
        _ui -> _table -> setItem(row_count, INCOME_DESCRIPTION, new QTableWidgetItem());
    } else {
        _ui -> _table -> setItem(row_count, REST_TOTAL, new QTableWidgetItem());
        _ui -> _table -> setItem(row_count, REST_DESCRIPTION, new QTableWidgetItem());
        _ui -> _table -> setItem(row_count, INCOME_TOTAL, total_item);
        _ui -> _table -> setItem(row_count, INCOME_DESCRIPTION, description_item);
    }
    _ui -> _table -> scrollToBottom();
    WriteXML();
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


void MyWallet::WriteXML() const {
    QString dir_path = QDir().home().absolutePath() + "/.config/MyWallet";
    if (false == QDir(dir_path).exists())
        QDir().mkdir(dir_path);
    QDir().setCurrent(dir_path);
    QString file_name("wallet.xml");
    QFile file(file_name);
    if (false == file.open(QFile::WriteOnly)) {
       QMessageBox::warning(0,
                            "MyWallet",
                            QString("Невозможно открыть файл 1 \n%2").arg(file_name).arg(file.errorString()),
                            QMessageBox::Ok);
        return;
    }
    QString file_content;
    QXmlStreamWriter stream_writer(&file_content);
    stream_writer.setAutoFormatting(true);
    stream_writer.writeStartDocument();
    stream_writer.writeStartElement("mywallet");
    for (int i = 0; i < _ui -> _table -> rowCount(); i++) {
        stream_writer.writeStartElement("data");
        stream_writer.writeAttribute("date", _ui -> _table -> item(i, DATE_INDEX) -> text());
        if (false == _ui -> _table -> item(i, REST_TOTAL) -> text().isEmpty()) {
            stream_writer.writeAttribute("out", _ui -> _table -> item(i, REST_TOTAL) -> text());
            stream_writer.writeAttribute("out_description", _ui -> _table -> item(i, REST_DESCRIPTION) -> text());
        }
        if (false == _ui -> _table -> item(i, INCOME_TOTAL) -> text().isEmpty()) {
            stream_writer.writeAttribute("input", _ui -> _table -> item(i, INCOME_TOTAL) -> text());
            stream_writer.writeAttribute("input_description", _ui -> _table -> item(i, INCOME_DESCRIPTION) -> text());
        }
        stream_writer.writeEndElement();
    }
    stream_writer.writeEndElement();
    stream_writer.writeEndDocument();
    qDebug() << file_content;
}
