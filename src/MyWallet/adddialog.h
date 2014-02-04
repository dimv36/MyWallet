#ifndef ADDDIALOG_H
#define ADDDIALOG_H

#include <QDialog>
#include <QDate>
#include <QPushButton>
#include <QTextEdit>

namespace Ui {
class AddDialog;
}

class AddDialog : public QDialog {
    Q_OBJECT

private:
    Ui::AddDialog* _ui;
public:
    explicit AddDialog(QWidget* parent = 0);
    ~AddDialog();

    QDate get_date() const;
    int get_rest() const;
    QString get_rest_description() const;
    int get_income() const;
    QString get_income_description() const;

    bool IsRestFieldsActive() const;
    bool IsIncomeFieldsActive() const;

private slots:
    void SlotUpdateForm();

private:
    bool IsDataEntered() const;

};

#endif // ADDDIALOG_H
