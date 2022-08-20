#include "ShutDownPC.h"
#include <QMessageBox>
#include <sstream>


ShutDownPC::ShutDownPC(QWidget *parent)
    : QMainWindow(parent)
{
    ui.setupUi(this);

    ui.timeEdit->setDateTime(QDateTime::currentDateTime());

    connect(ui.comboBox, &QComboBox::currentIndexChanged, this, &ShutDownPC::on_comboBox_change);
}

ShutDownPC::~ShutDownPC()
{}

void ShutDownPC::on_startBtn_clicked()
{
    if (ui.startBtn->text() == "START")
    {
        on_startBtn();
    }
    else
    {
        on_cancelBtn();
    }
}

void ShutDownPC::on_startBtn()
{
    int shutdownIn;
    if (ui.comboBox->currentIndex() == 0)
    {
        shutdownIn = ui.timeEdit->dateTime().toSecsSinceEpoch() - QDateTime::currentDateTime().toSecsSinceEpoch();
        if (shutdownIn < 0)
        {
            shutdownIn += 86400;
        }
    }
    else if (ui.comboBox->currentIndex() == 1)
    {
        shutdownIn = (ui.timeEdit->time().hour() * 3600) + (ui.timeEdit->time().hour() * 60);
    }
    if (shutdownIn < 300)
    {
        QMessageBox::StandardButton reply;
        reply = QMessageBox::question(this, "Set the timer?", "Are you sure to set the timer less than 5 minutes?",
            QMessageBox::Yes | QMessageBox::No, QMessageBox::No);
        if (reply == QMessageBox::No)
        {
            return;
        }
    }

    std::stringstream fmt;
    fmt << "shutdown -s -t " << shutdownIn;

    system(fmt.str().c_str());

    ui.startBtn->setText(QString("CANCEL"));
}

void ShutDownPC::on_cancelBtn()
{
    system("shutdown -a");

    ui.startBtn->setText(QString("START"));
}

void ShutDownPC::on_comboBox_change()
{
    if (ui.comboBox->currentIndex() == 0)
    {
        ui.timeEdit->setDateTime(QDateTime::currentDateTime());
    }
    else if (ui.comboBox->currentIndex() == 1)
    {
        ui.timeEdit->setTime(QTime(0, 0));
    }
}


