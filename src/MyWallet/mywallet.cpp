#include "mywallet.h"
#include "ui_mywallet.h"

#include <QDebug>
#define DATE_INDEX 0
#define OUTPUT_INDEX 1
#define OUTPUT_DESCRIPTION_INDEX 2
#define INPUT_INDEX 3
#define INPUT_DESCRIPTION_INDEX 4

MyWallet::MyWallet(QWidget *parent) :
    QMainWindow(parent),
    _ui(new Ui::MyWallet) {
    _ui -> setupUi(this);
    ReadXML();
}

MyWallet::~MyWallet() {
    WriteXML();
    delete _ui;
}


void MyWallet::CreateTableRow(QDate &date, int total, QString &description, bool isRest) {
    _ui -> _table -> setRowCount(_ui -> _table -> rowCount() + 1);
    int row_count = _ui -> _table -> rowCount() - 1;
    CreateNewItem(row_count, DATE_INDEX, date.toString("d MMMM yyyy"));
    QTableWidgetItem *total_item = new QTableWidgetItem(QString::number(total));
    QTableWidgetItem *description_item = new QTableWidgetItem(description);
    total_item -> setTextAlignment(Qt::AlignCenter);
    if (true == isRest) {
        _ui -> _table -> setItem(row_count, OUTPUT_INDEX, total_item);
        _ui -> _table -> setItem(row_count, OUTPUT_DESCRIPTION_INDEX, description_item);
        _ui -> _table -> setItem(row_count, INPUT_INDEX, new QTableWidgetItem());
        _ui -> _table -> setItem(row_count, INPUT_DESCRIPTION_INDEX, new QTableWidgetItem());
    } else {
        _ui -> _table -> setItem(row_count, OUTPUT_INDEX, new QTableWidgetItem());
        _ui -> _table -> setItem(row_count, OUTPUT_DESCRIPTION_INDEX, new QTableWidgetItem());
        _ui -> _table -> setItem(row_count, INPUT_INDEX, total_item);
        _ui -> _table -> setItem(row_count, INPUT_DESCRIPTION_INDEX, description_item);
    }
    _ui -> _table -> scrollToBottom();
}


void MyWallet::AddNewRowInTable() {
    _ui -> _table -> setRowCount(_ui -> _table -> rowCount() + 1);
}


void MyWallet::CreateNewItem(int row, int column, QString text) {
    QTableWidgetItem *item = new QTableWidgetItem(text);
    _ui -> _table -> setItem(row, column, item);
    item -> setTextAlignment(Qt::AlignCenter);
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
        QString date;
        while(false == reader.atEnd()) {
            if (true == reader.readNextStartElement()) {
                if ("note" == reader.name())
                    date = reader.attributes().value("date").toString();
                if ("in" == reader.name()) {
                    QString input = reader.attributes().value("value").toString();
                    QString description = reader.attributes().value("description").toString();
                    AddNewRowInTable();
                    CreateNewItem(_ui -> _table -> rowCount() - 1, DATE_INDEX, date);
                    CreateNewItem(_ui -> _table -> rowCount() - 1, OUTPUT_INDEX, QString());
                    CreateNewItem(_ui -> _table -> rowCount() - 1, OUTPUT_DESCRIPTION_INDEX, QString());
                    CreateNewItem(_ui -> _table -> rowCount() - 1, INPUT_INDEX, input);
                    CreateNewItem(_ui -> _table -> rowCount() - 1, INPUT_DESCRIPTION_INDEX, description);
                }
                if ("out" == reader.name()) {
                    QString OUTPUT_INDEXput = reader.attributes().value("value").toString();
                    QString description = reader.attributes().value("description").toString();
                    AddNewRowInTable();
                    CreateNewItem(_ui -> _table -> rowCount() - 1, DATE_INDEX, date);
                    CreateNewItem(_ui -> _table -> rowCount() - 1, OUTPUT_INDEX, OUTPUT_INDEXput);
                    CreateNewItem(_ui -> _table -> rowCount() - 1, OUTPUT_DESCRIPTION_INDEX, description);
                    CreateNewItem(_ui -> _table -> rowCount() - 1, INPUT_INDEX, QString());
                    CreateNewItem(_ui -> _table -> rowCount() - 1, INPUT_DESCRIPTION_INDEX, QString());
                }
            }
        }
        _ui -> _table -> scrollToBottom();
        _ui -> _table -> item(0, DATE_INDEX) -> setSelected(false);
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
    int element_index = 0;
    while(true) {
        QTableWidgetItem* current_item = _ui -> _table -> item(element_index, DATE_INDEX);
        int item_count = _ui -> _table -> findItems(current_item -> text(), Qt::MatchCaseSensitive).count();
        writer.writeStartElement("note");
        writer.writeAttribute("date", current_item -> text());
        for (int i = element_index; i < element_index + item_count; i++) {
            if (false == _ui -> _table -> item(i, OUTPUT_INDEX) -> text().isEmpty()) {
                writer.writeStartElement("out");
                writer.writeAttribute("value", _ui -> _table -> item(i, OUTPUT_INDEX) -> text());
                writer.writeAttribute("description", _ui -> _table -> item(i, OUTPUT_DESCRIPTION_INDEX) -> text());
                writer.writeEndElement();
            }
            if (false == _ui -> _table -> item(i, INPUT_INDEX) -> text().isEmpty()) {
                writer.writeStartElement("in");
                writer.writeAttribute("value", _ui -> _table -> item(i, INPUT_INDEX) -> text());
                writer.writeAttribute("description", _ui -> _table -> item(i, INPUT_DESCRIPTION_INDEX) -> text());
                writer.writeEndElement();
            }
        }
        writer.writeEndElement();
        element_index += item_count;
        if (element_index >= _ui -> _table -> rowCount())
            break;
    }
    writer.writeEndElement();
    writer.writeEndDocument();
    file.close();
}


void MyWallet::on__action_add_triggered() {
    AddDialog dialog(this);
    if (QDialog::Accepted == dialog.exec()) {
       bool is_output_fields_active = dialog.IsOutputFieldsActive();
       bool is_input_fields_active = dialog.IsInputFieldsActive();
       QDate date = dialog.get_date();
       if (true == is_output_fields_active) {
           int output = dialog.get_input();
           QString output_description = dialog.get_output_description();
           CreateTableRow(date, output, output_description, true);
       }
       if (true == is_input_fields_active) {
            int input = dialog.get_input();
            QString input_description = dialog.get_input_description();
            CreateTableRow(date, input, input_description, false);
       }
    }
}


void MyWallet::on__action_exit_triggered() {
    WriteXML();
    exit(0);
}


void MyWallet::on__action_remove_triggered() {
    if (false == _ui -> _table -> selectedItems().isEmpty()) {
        int current_row = _ui -> _table -> currentRow();
        _ui -> _table -> removeRow(current_row);
    }
}


