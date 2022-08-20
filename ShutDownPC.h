#pragma once

#include <QtWidgets/QMainWindow>
#include "ui_ShutDownPC.h"

class ShutDownPC : public QMainWindow
{
    Q_OBJECT



public:
    ShutDownPC(QWidget *parent = nullptr);
    ~ShutDownPC();

private slots:
    void on_startBtn_clicked();
    void on_comboBox_change();

private:
    void on_startBtn();
    void on_cancelBtn();

    Ui::ShutDownPCClass ui;

};
