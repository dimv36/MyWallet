#ifndef ADDDIALOG_H
#define ADDDIALOG_H

#include <QDialog>
#include <QPushButton>

namespace Ui {
class AddDialog;
}

class AddDialog : public QDialog {
    Q_OBJECT

public:
    explicit AddDialog(QWidget* parent = 0);
    ~AddDialog();

private:
    Ui::AddDialog* _ui;

private:
    void UpdateForm();
};

#endif // ADDDIALOG_H
