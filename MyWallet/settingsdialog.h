#ifndef SETTINGSDIALOG_H
#define SETTINGSDIALOG_H

#include <QDialog>
#include <QFileDialog>

namespace Ui {
class SettingsDialog;
}

class SettingsDialog : public QDialog {
    Q_OBJECT


private:
    Ui::SettingsDialog *_ui;

public:
    explicit SettingsDialog(QWidget *parent = 0);
    ~SettingsDialog();

    void set_directory(const QString directory);
    void set_wallet_name(const QString wallet_name);
    QString get_directory() const;
    QString get_wallet_name() const;

    bool IsWalletBoxIsActive() const;
private slots:
    void on__directory_button_clicked();
};

#endif // SETTINGSDIALOG_H
