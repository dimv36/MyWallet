#ifndef ADDDIALOG_H
#define ADDDIALOG_H

#include <QDialog>
#include <QDate>
#include <QPushButton>

#include "editingtabledelegate.h"

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
    QList<QPair<QString, QString> > get_outputs() const;
    QList<QPair<QString, QString> > get_inputs() const;

    bool IsOutputFieldsActive() const;
    bool IsInputFieldsActive() const;

private slots:
    void SlotUpdateForm();

};

#endif // ADDDIALOG_H
