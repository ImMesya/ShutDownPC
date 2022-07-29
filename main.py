# -*- coding: utf-8 -*-

import os
from datetime import timedelta

from PyQt5.QtCore import QDateTime, QTime
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QVBoxLayout, \
    QRadioButton, QTimeEdit, QWidget, QApplication, qApp, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        timer_VBox = QVBoxLayout()

        timer_font = QFont()
        timer_font.setPixelSize(25)

        self.timer = QTimeEdit()
        self.timer.setFont(timer_font)
        self.timer.setDateTime(QDateTime.currentDateTime().toPyDateTime())

        timer_VBox.addWidget(self.timer)

        radial_HBox = QHBoxLayout()

        self.in_radioButton = QRadioButton()
        self.in_radioButton.setText('Выключить в')
        self.in_radioButton.setChecked(True)
        self.in_radioButton.clicked.connect(self.on_radiobutton_state)
        self.at_radioButton = QRadioButton()
        self.at_radioButton.setText('Выключить через')
        self.at_radioButton.clicked.connect(self.on_radiobutton_state)

        radial_HBox.addWidget(self.in_radioButton)
        radial_HBox.addWidget(self.at_radioButton)

        buttons_HBox = QHBoxLayout()

        self.start_button = QPushButton()
        self.start_button.setText('START')
        self.start_button.clicked.connect(self.cancel_start_button)
        exit_button = QPushButton()
        exit_button.setText('EXIT')
        exit_button.clicked.connect(self.on_exit_button)

        buttons_HBox.addWidget(self.start_button)
        buttons_HBox.addWidget(exit_button)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(radial_HBox)
        mainLayout.addLayout(timer_VBox)
        mainLayout.addLayout(buttons_HBox)

        self.setWindowTitle('Shutdown Timer')
        self.setLayout(mainLayout)

    def on_exit_button(self):
        qApp.quit()

    def cancel_start_button(self):
        if self.start_button.text() == 'START':
            self.on_start_button()
        else:
            self.on_cancel_button()

    def on_start_button(self):
        if self.in_radioButton.isChecked():
            shutdown_in = self.timer.dateTime().toSecsSinceEpoch() - QDateTime.currentDateTime().toSecsSinceEpoch()
            if shutdown_in < 0:
                shutdown_in += 86400
        elif self.at_radioButton.isChecked():
            shutdown_in = (self.timer.time().hour() * 3600) + (self.timer.time().minute() * 60)

        if shutdown_in < 300:
            reply = QMessageBox.question(self, 'Установить таймер?',
                                         'Вы указали время меньше 5 минут, установить таймер?',
                                         QMessageBox.Yes | QMessageBox.No,
                                         QMessageBox.No)
            if reply == QMessageBox.No:
                return

        os.system(f'shutdown -s -t {shutdown_in}')
        QMessageBox.information(self, 'Таймер установлен',
                                f'Ваш ПК выключится через {timedelta(seconds=shutdown_in)}!')

        self.start_button.setText('ОТМЕНИТЬ')

    def on_cancel_button(self):
        os.system('shutdown -a')
        QMessageBox.information(self, 'Таймер отменён',
                                'Таймер на выключение ПК отменён, установите новый')
        self.start_button.setText('START')

    def on_radiobutton_state(self):
        if self.in_radioButton.isChecked():
            self.timer.setDateTime(QDateTime.currentDateTime().toPyDateTime())
        elif self.at_radioButton.isChecked():
            self.timer.setTime(QTime(0, 0))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())
