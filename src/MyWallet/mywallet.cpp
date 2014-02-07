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
    ReadXML();
}

MyWallet::~MyWallet() {
    delete _ui;
}


void MyWallet::CreateTableRow(QDate &date, int total, QString &description, bool isRest) {
    _ui -> _table -> setRowCount(_ui -> _table -> rowCount() + 1);
    int row_count = _ui -> _table -> rowCount() - 1;
    QTableWidgetItem *date_item = new QTableWidgetItem(date.toString("d MMMM yyyy"));
    _ui -> _table -> setItem(row_count, DATE_INDEX, date_item);
    date_item -> setTextAlignment(Qt::AlignCenter);
    QTableWidgetItem *total_item = new QTableWidgetItem(QString::number(total));
    QTableWidgetItem *description_item = new QTableWidgetItem(description);
    total_item -> setTextAlignment(Qt::AlignCenter);
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
    _ui -> _table -> sortItems(DATE_INDEX);
}


void MyWallet::ReadXML() {
    QString file_name = QDir().home().absolutePath() + "/.config/MyWallet/wallet.xml";
    if (true == QFileInfo(file_name).exists()) {
        QFile file(file_name);
        if (false == file.open(QFile::ReadOnly)) {
            QMessageBox::warning(0,
                                 tr("MyWallet"),
                                 tr("Невозможно открыть файл %1 \n%2").arg(file_name).arg(file.errorString()),
                                 QMessageBox::Ok);
            return;
            }
        QXmlStreamReader reader(&file);
        while(false == reader.atEnd()) {
            reader.readNext();
            if ("date" == reader.name()) {
                qDebug() << reader.attributes().value("date");
            }
            if ("in" == reader.name()) {
                qDebug() << reader.attributes().value("value") << " " << reader.attributes().value("description");
            }
            if ("out" == reader.name()) {
                qDebug() << reader.attributes().value("value") << " " << reader.attributes().value("description");
            }
        }
    } else
        return;
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
                            tr("MyWallet"),
                            tr("Невозможно открыть файл %1 \n%2").arg(file_name).arg(file.errorString()),
                            QMessageBox::Ok);
        return;
    }
    QXmlStreamWriter writer(&file);
    writer.setAutoFormatting(true);
    writer.writeStartDocument();
    writer.writeStartElement("mywallet");
    for (int i = 0; i < _ui -> _table -> rowCount(); i++) {
        int same_date_count = _ui -> _table -> findItems(_ui -> _table -> item(DATE_INDEX, i) -> text(), Qt::MatchCaseSensitive).count();
        writer.writeStartElement(_ui -> _table -> item(DATE_INDEX, i) -> text());
        for (int j = 0; j < same_date_count; j++) {

        }
//    for (int i = 0; i < _ui -> _table -> rowCount(); i++) {
//        bool date_is_empty = _ui -> _table -> item(i, DATE_INDEX) -> text().isEmpty();
//        if (false == date_is_empty) {
//            writer.writeStartElement("date");
//            writer.writeAttribute("date", _ui -> _table -> item(i, DATE_INDEX) -> text());
//        }
//        if (false == _ui -> _table -> item(i, REST_TOTAL) -> text().isEmpty()) {
//            writer.writeStartElement("out");
//            writer.writeAttribute("value", _ui -> _table -> item(i, REST_TOTAL) -> text());
//            writer.writeAttribute("description", _ui -> _table -> item(i, REST_DESCRIPTION) -> text());
//            writer.writeEndElement();
//           }
//        if (false == _ui -> _table -> item(i, INCOME_TOTAL) -> text().isEmpty()) {
//            writer.writeStartElement("in");
//            writer.writeAttribute("value", _ui -> _table -> item(i, INCOME_TOTAL) -> text());
//            writer.writeAttribute("description", _ui -> _table -> item(i, INCOME_DESCRIPTION) -> text());
//            writer.writeEndElement();
//           }
//        if (true == date_is_empty)
//            writer.writeEndElement();
//    }
    }
    writer.writeEndElement();
    writer.writeEndDocument();
    file.close();
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


void MyWallet::on__action_exit_triggered() {
    WriteXML();
    exit(0);
}
