#include "mywallet.h"
#include "ui_mywallet.h"

#include <QDebug>
#define DEFAULT_FILE_NAME "wallet.xml"
#define MAIN_SETTINGS "MyWallet"
#define DATE_INDEX 0
#define OUTPUT_INDEX 1
#define OUTPUT_DESCRIPTION_INDEX 2
#define INPUT_INDEX 3
#define INPUT_DESCRIPTION_INDEX 4
#define DATE_FORMAT "d MMMM yyyy"


MyWallet::MyWallet(QWidget *parent) :
    QMainWindow(parent),
    _ui(new Ui::MyWallet) {
    _ui -> setupUi(this);
    connect(this, SIGNAL(SignalUpdate()), this, SLOT(SlotUpdateTotalFields()));
    connect(this, SIGNAL(SignalWalletWasOpen()), this, SLOT(SlotUpdateWindowHeader()));
    _current_path = QDir().home().path() + "/.MyWallet";
    _wallet_name = DEFAULT_FILE_NAME;
    ReadSettings();
    ReadXML();
    _ui -> _table -> setCurrentItem(0);

    _ui -> _table -> setItemDelegateForColumn(OUTPUT_INDEX, new EditingTableDelegate);
    _ui -> _table -> setItemDelegateForColumn(INPUT_INDEX, new EditingTableDelegate);

    if (_ui -> _label_rest_value -> text().toInt() == 0)
        ChangeMonthRest();
}


MyWallet::~MyWallet() {
    WriteSettings();
    WriteXML();
    delete _ui;
}


void MyWallet::CreateTableRow(QDate &date, int total, QString &description, bool is_rest) {
    _ui -> _table -> setRowCount(_ui -> _table -> rowCount() + 1);
    int row_count = _ui -> _table -> rowCount() - 1;
    CreateNewItem(row_count, DATE_INDEX, date.toString(DATE_FORMAT));
    QTableWidgetItem *total_item = new QTableWidgetItem(QString::number(total));
    QTableWidgetItem *description_item = new QTableWidgetItem(description);
    total_item -> setTextAlignment(Qt::AlignCenter);
    description_item -> setTextAlignment(Qt::AlignCenter);
    if (true == is_rest) {
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
    _ui -> _table -> sortByColumn(DATE_INDEX, Qt::AscendingOrder);
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
    _ui -> _table -> setRowCount(0);
    QString file_name = _current_path + "/" + _wallet_name;
    if (true == QFileInfo(file_name).exists()) {
        QFile wallet_file(file_name);
        if (false == wallet_file.open(QFile::ReadOnly)) {
            QMessageBox::warning(this,
                                 tr("MyWallet"),
                                 tr("Невозможно открыть файл %1 \n%2").arg(file_name).arg(wallet_file.errorString()),
                                 QMessageBox::Ok);
            return;
        }
        QXmlStreamReader reader(&wallet_file);
        int year = 0;
        int month = 0;
        int day = 0;
        QDate date;
        QDate current_date = QDate::currentDate();
        while(false == reader.atEnd()) {
            if (true == reader.readNextStartElement()) {
                if ("year" == reader.name())
                    year = reader.attributes().value("value").toInt();
                if ("month" == reader.name()) {
                    month = reader.attributes().value("value").toInt();
                    QString rest = reader.attributes().value("rest").toString();
                    _ui -> _label_rest_value -> setText(rest);
                }
                if (year == current_date.year() && month == current_date.month()) {
                    if ("day" == reader.name())
                        day = reader.attributes().value("value").toInt();
                    if ("in" == reader.name()) {
                        QString input = reader.attributes().value("value").toString();
                        QString description = reader.attributes().value("description").toString();
                        AddNewRowInTable();
                        date = QDate(year, month, day);
                        CreateNewItem(_ui -> _table -> rowCount() - 1, DATE_INDEX, date.toString(DATE_FORMAT));
                        CreateNewItem(_ui -> _table -> rowCount() - 1, OUTPUT_INDEX, QString());
                        CreateNewItem(_ui -> _table -> rowCount() - 1, OUTPUT_DESCRIPTION_INDEX, QString());
                        CreateNewItem(_ui -> _table -> rowCount() - 1, INPUT_INDEX, input);
                        CreateNewItem(_ui -> _table -> rowCount() - 1, INPUT_DESCRIPTION_INDEX, description);
                    }
                    if ("out" == reader.name()) {
                        QString output = reader.attributes().value("value").toString();
                        QString description = reader.attributes().value("description").toString();
                        AddNewRowInTable();
                        date = QDate(year, month, day);
                        CreateNewItem(_ui -> _table -> rowCount() - 1, DATE_INDEX, date.toString(DATE_FORMAT));
                        CreateNewItem(_ui -> _table -> rowCount() - 1, OUTPUT_INDEX, output);
                        CreateNewItem(_ui -> _table -> rowCount() - 1, OUTPUT_DESCRIPTION_INDEX, description);
                        CreateNewItem(_ui -> _table -> rowCount() - 1, INPUT_INDEX, QString());
                        CreateNewItem(_ui -> _table -> rowCount() - 1, INPUT_DESCRIPTION_INDEX, QString());
                    }
                }
            }
        }
        _ui -> _table -> scrollToBottom();
        emit SignalUpdate();
        emit SignalWalletWasOpen();
    } else
        return;
}


QTableWidgetItem* MyWallet::GetNextItem(QTableWidgetItem *item) const {
    int column = item -> column();
    int row = item -> row();
    if (_ui -> _table -> rowCount() == row + 1)
        return 0;
    else
        return _ui -> _table -> item(row + 1, column);
}


QTableWidgetItem* MyWallet::GetPreviousItem(QTableWidgetItem *item) const {
    int column = item -> column();
    int row = item -> row();
    if (row - 1 >= 0)
        return _ui -> _table -> item(row - 1, column);
    else
        return 0;
}


QDomElement MyWallet::GetChildItemByAttribute(QDomElement &element, int value) const {
        QDomElement result;
        if (true == element.hasChildNodes()) {
            QDomNodeList node_list = element.childNodes();
            for (int index = 0; index < node_list.count(); index++) {
                QDomElement item = node_list.at(index).toElement();
                if (value == item.attribute("value").toInt())
                    result = item;
            }
        }
        return result;
}


QDomElement MyWallet::GetChildItemByAttribute(QDomElement &element, int value, QString &description) const {
    QDomElement result;
    if (true == element.hasChildNodes()) {
        QDomNodeList node_list = element.childNodes();
        for (int index = 0; index < node_list.count(); index++) {
            QDomElement item = node_list.at(index).toElement();
            if (value == item.attribute("value").toInt() && description == item.attribute("description"))
                result = item;
        }
    }
    return result;
}


void MyWallet::WriteXML() const {
    if (0 == _ui -> _table -> rowCount())
        return;
    if (false == QDir(_current_path).exists())
        QDir().mkdir(_current_path);
    QDir().setCurrent(_current_path);
    QFile file(_wallet_name);
    if (false == file.open(QFile::ReadOnly)) {
       QMessageBox::warning(0,
                            tr("MyWallet"),
                            tr("Невозможно открыть файл %1 \n%2 на чтение").arg(_wallet_name).arg(file.errorString()),
                            QMessageBox::Ok);
        return;
    }
    QDomDocument document;
    document.setContent(&file);
    file.close();
    if (false == file.open(QFile::WriteOnly)) {
        QMessageBox::warning(0,
                             tr("MyWallet"),
                             tr("Невозможно открыть файл %1 \n%2 на запись").arg(_wallet_name).arg(file.errorString()),
                             QMessageBox::Ok);
         return;
    }
    QTextStream stream(&file);
    QDomElement root = document.documentElement();
    if (true == root.isNull()) {
        root = document.createElement("mywallet");
        document.appendChild(root);
    }
    for (int row = 0; row < _ui -> _table -> rowCount(); row++) {
        QDate date = QDate::fromString(_ui -> _table -> item(row, DATE_INDEX) -> text(), DATE_FORMAT);
        QDomElement year_item = GetChildItemByAttribute(root, date.year());
        if (true == year_item.isNull()) {
            year_item = document.createElement("year");
            year_item.setAttribute("value", date.year());
            root.appendChild(year_item);
        }
        QDomElement month_item = GetChildItemByAttribute(year_item, date.month());
        if (true == month_item.isNull()) {
            month_item = document.createElement("month");
            month_item.setAttribute("value", date.month());
            month_item.setAttribute("rest", _ui -> _label_rest_value -> text());
            year_item.appendChild(month_item);
        }
        QDomElement day_item = GetChildItemByAttribute(month_item, date.day());
        if (true == day_item.isNull()) {
            day_item = document.createElement("day");
            day_item.setAttribute("value", date.day());
            month_item.appendChild(day_item);
        }
        if (false == _ui -> _table -> item(row, INPUT_DESCRIPTION_INDEX) -> text().isEmpty()) {
            int in = _ui -> _table -> item(row, INPUT_INDEX) -> text().toInt();
            QString description = _ui -> _table -> item(row, INPUT_DESCRIPTION_INDEX) -> text();
            QDomElement input = GetChildItemByAttribute(day_item, in, description);
            if (true == input.isNull()) {
                input = document.createElement("in");
                input.setAttribute("value", _ui -> _table -> item(row, INPUT_INDEX) -> text());
                input.setAttribute("description", _ui -> _table -> item(row, INPUT_DESCRIPTION_INDEX) -> text());
                day_item.appendChild(input);
            }
        }
        if (false == _ui -> _table -> item(row, OUTPUT_DESCRIPTION_INDEX) -> text().isEmpty()) {
            int out = _ui -> _table -> item(row, OUTPUT_INDEX) -> text().toInt();
            QString description = _ui -> _table -> item(row, OUTPUT_DESCRIPTION_INDEX) -> text();
            QDomElement output = GetChildItemByAttribute(day_item, out, description);
            if (true == output.isNull()) {
                output = document.createElement("out");
                output.setAttribute("value", _ui -> _table -> item(row, OUTPUT_INDEX) -> text());
                output.setAttribute("description", _ui -> _table -> item(row, OUTPUT_DESCRIPTION_INDEX) -> text());
                day_item.appendChild(output);
            }
        }
    }
    document.save(stream, 4);
    file.close();
}


void MyWallet::WriteSettings()  {
    _settings.beginGroup(MAIN_SETTINGS);
    _settings.setValue("position", pos());
    _settings.setValue("size", size());
    _settings.setValue("path", _current_path);
    _settings.setValue("wallet_name", _wallet_name);
    _settings.endGroup();
}


void MyWallet::ReadSettings() {
    _settings.beginGroup(MAIN_SETTINGS);
    resize(_settings.value("size").toSize());
    move(_settings.value("position").toPoint());
    if ((false ==_settings.value("path").toString().isEmpty()) && (false == _settings.value("wallet_name").toString().isEmpty())) {
        _current_path = _settings.value("path").toString();
        _wallet_name = _settings.value("wallet_name").toString();
    }
    _settings.endGroup();
}


void MyWallet::ChangeMonthRest() {
    RestMonthDialog dialog;
    dialog.set_rest_month(_ui -> _label_rest_value -> text().toInt());
    if (QDialog::Accepted == dialog.exec()) {
        int rest = dialog.get_rest_month();
        _ui -> _label_rest_value -> setText(QString::number(rest));
    }
    emit SignalUpdate();
}


void MyWallet::DeleteItemFromXML(QDate &date, int value, QString &description, bool is_rest) {
    QDir().setCurrent(_current_path);
    QFile file(_wallet_name);
    if (false == file.open(QFile::ReadOnly)) {
       QMessageBox::warning(0,
                            tr("MyWallet"),
                            tr("Невозможно открыть файл %1 \n%2 на чтение").arg(_wallet_name).arg(file.errorString()),
                            QMessageBox::Ok);
        return;
    }
    QDomDocument document;
    document.setContent(&file);
    file.close();
    if (false == file.open(QFile::WriteOnly)) {
        QMessageBox::warning(0,
                             tr("MyWallet"),
                             tr("Невозможно открыть файл %1 \n%2 на запись").arg(_wallet_name).arg(file.errorString()),
                             QMessageBox::Ok);
         return;
    }
    QTextStream stream(&file);
    QDomElement root = document.documentElement();
    QDomElement year_element = GetChildItemByAttribute(root, date.year());
    QDomElement month_element = GetChildItemByAttribute(year_element, date.month());
    QDomElement day_element = GetChildItemByAttribute(month_element, date.day());
    QString tag_name;
    if (true == is_rest)
        tag_name = "out";
    else
        tag_name = "in";
    QDomElement delete_element = GetChildItemByAttribute(day_element, value, description);
    day_element.removeChild(delete_element);
    if (false == day_element.hasChildNodes())
        month_element.removeChild(day_element);
    if (false == month_element.hasChildNodes())
        year_element.removeChild(month_element);
    if (false == year_element.hasChildNodes())
        root.removeChild(year_element);
    document.save(stream, 4);
    file.close();
}


void MyWallet::on__action_add_triggered() {
    AddDialog dialog(this);
    if (QDialog::Accepted == dialog.exec()) {
       bool is_output_fields_active = dialog.IsOutputFieldsActive();
       bool is_input_fields_active = dialog.IsInputFieldsActive();
       QDate date = dialog.get_date();
       if (true == is_output_fields_active) {
           QList<QPair<QString, QString> > outputs = dialog.get_outputs();
           for (int i = 0; i < outputs.size(); i++) {
               QPair<QString, QString> row = outputs.at(i);
               CreateTableRow(date, row.first.toInt(), row.second, true);
           }
       }
       if (true == is_input_fields_active) {
            QList<QPair<QString, QString> > inputs = dialog.get_inputs();
            for (int i = 0; i < inputs.size(); i++) {
                QPair<QString, QString> row = inputs.at(i);
                CreateTableRow(date, row.first.toInt(), row.second, false);
            }
       }
       emit SignalUpdate();
    }
}


void MyWallet::on__action_exit_triggered() {
    WriteSettings();
    WriteXML();
    exit(0);
}


void MyWallet::on__action_remove_triggered() {
    if (false == _ui -> _table -> selectedItems().isEmpty()) {
        int current_row = _ui -> _table -> currentRow();
        QDate date = QDate::fromString(_ui -> _table -> item(current_row, DATE_INDEX) -> text(), DATE_FORMAT);
        int value = 0;
        QString description;
        if (true == _ui -> _table -> item(current_row, OUTPUT_DESCRIPTION_INDEX) -> text().isEmpty()) {
            value = _ui -> _table -> item(current_row, INPUT_INDEX) -> text().toInt();
            description = _ui -> _table -> item(current_row, INPUT_DESCRIPTION_INDEX) -> text();
        } else {
            value = _ui -> _table -> item(current_row, OUTPUT_INDEX) -> text().toInt();
            description = _ui -> _table -> item(current_row, OUTPUT_DESCRIPTION_INDEX) -> text();
        }
        DeleteItemFromXML(date, value, description);
        _ui -> _table -> removeRow(current_row);
        emit SignalUpdate();
    }
}


void MyWallet::SlotUpdateTotalFields() {
    int input = 0;
    int output = 0;
    int month_output = _ui -> _label_rest_value -> text().toInt();
    for (int i = 0; i < _ui -> _table -> rowCount(); i++) {
        input += _ui -> _table -> item(i, INPUT_INDEX) -> text().toInt();
        output += _ui -> _table -> item(i, OUTPUT_INDEX) -> text().toInt();
    }
    int total = month_output + input - output;
    _ui -> _label_output_value -> setText(QString::number(output));
    _ui -> _label_input_value -> setText(QString::number(input));
    _ui -> _label_total_value -> setText(QString::number(total));
    if (total >= 0)
       _ui -> _label_total_value -> setStyleSheet("QLabel { color: green }");
    else
       _ui -> _label_total_value -> setStyleSheet("QLabel { color: red }");
}


void MyWallet::on__action_open_triggered() {
    QString file_name = QFileDialog::getOpenFileName(this,
                                                     tr("Выбрать файл"),
                                                     QDir::current().path(),
                                                     tr("XML-файлы (*.xml)"));
    WriteXML();
    _current_path = QFileInfo(file_name).dir().path();
    _wallet_name = QFileInfo(file_name).fileName();
    ReadXML();
}


void MyWallet::on__action_settings_triggered() {
    SettingsDialog dialog(this);
    dialog.set_directory(_current_path);
    dialog.set_wallet_name(_wallet_name);
    if (QDialog::Accepted == dialog.exec()) {
        if (true == dialog.IsWalletBoxIsActive()) {
            _current_path = dialog.get_directory() + "/";
            _wallet_name = dialog.get_wallet_name();
        }
    }
}


void MyWallet::SlotUpdateWindowHeader() {
    setWindowTitle(_current_path + _wallet_name + " - [MyWallet]");
}

