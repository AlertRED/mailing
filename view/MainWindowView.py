from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QSize

from view.qt import MainWindow
from time import strftime
import time


class MainWindowView(QtWidgets.QMainWindow):
    open_data_signal = pyqtSignal()
    open_accounts_signal = pyqtSignal()
    start_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    test_only_signal = pyqtSignal(bool)
    print_log_signal = pyqtSignal(str, time.struct_time)
    print_progress_signal = pyqtSignal(int, int)
    print_email_stat_signal = pyqtSignal(str, int, int)
    start_without_test_message = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionData.triggered.connect(self.open_data_signal)
        self.ui.actionAccounts.triggered.connect(self.open_accounts_signal)
        self.ui.pushButton_play.clicked.connect(self.start_signal)
        self.ui.pushButton_pause.clicked.connect(self.pause_signal)
        self.ui.pushButton_stop.clicked.connect(self.stop_signal)
        self.ui.checkBox_testOnly.toggled.connect(self.test_only_signal)
        self.print_log_signal.connect(self.print_log)
        self.print_progress_signal.connect(self.print_progress)
        self.print_email_stat_signal.connect(self.print_email_stat)

    def print_log(self, text, time=None):
        if time:
            text = '[ {0} ] {1}'.format(strftime("%H:%M:%S", time), text)
        else:
            text = '{0}'.format(text)
        self.ui.plainText_log.appendPlainText(text)

    def print_progress(self, count: int, total: int):
        self.ui.progressBar_mailing.setValue(count)
        self.ui.progressBar_mailing.setMaximum(total if total else 1)
        self.ui.label_sendedMails.setText(f'Sent: {count} / {total:<6}')

    def print_email_stat(self, email: str, count: int, total: int):
        self.ui.label_curentEmail.setText(f'Current: {email}')
        self.ui.label_countEmails.setText(f'Accounts: {count} / {total:<6}')

    def test_checked(self, is_checked):
        self.ui.checkBox_testOnly.setChecked(is_checked)

    def start_mailing(self):
        self.__state_player(False, True, True)
        self.ui.checkBox_testOnly.setEnabled(True)
        self.ui.checkBox_testOnly.setEnabled(False)

    def pause_mailing(self):
        self.__state_player(True, False, True)

    def stop_mailing(self):
        self.__state_player(True, False, False)
        self.ui.checkBox_testOnly.setEnabled(True)

    def show_no_test_message(self):
        qm = QtWidgets.QMessageBox()
        result = qm.question(self, '', "Are you sure to start WITHOUT TEST?", qm.Yes | qm.No)
        self.start_without_test_message.emit(result == qm.Yes)


    def __state_player(self, is_start, is_pause, is_stop):
        self.ui.pushButton_play.setEnabled(is_start)
        self.ui.pushButton_pause.setEnabled(is_pause)
        self.ui.pushButton_stop.setEnabled(is_stop)

    def show_error(self, text: str):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(text)
        msg.setWindowTitle("Error")
        msg.exec()
