from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QCheckBox

from view.qt import MainWindow
from time import strftime


class MainWindowView(QtWidgets.QMainWindow):
    open_data_signal = pyqtSignal()
    open_accounts_signal = pyqtSignal()
    start_signal = pyqtSignal()
    pause_signal = pyqtSignal()
    stop_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionData.triggered.connect(self.open_data_signal)
        self.ui.actionAccounts.triggered.connect(self.open_accounts_signal)
        self.ui.pushButton_play.clicked.connect(self.start_signal)
        self.ui.pushButton_pause.clicked.connect(self.pause_signal)
        self.ui.pushButton_stop.clicked.connect(self.stop_signal)
        # self.ui.pushButton_play.clicked.connect(self.play)
        # self.ui.pushButton_pause.clicked.connect(self.pause)
        # self.ui.pushButton_stop.clicked.connect(self.stop)
        # self.print_progress(0, 0)
        # self.ui.pushButton_stop.setEnabled(False)
        # self.ui.pushButton_pause.setEnabled(False)

    # def show_filters_checkboxes(self, texts, connects):
    #     for text, connect in zip(reversed(texts), reversed(connects)):
    #         item = QCheckBox(text)
    #         item.clicked.connect(connect)
    #         self.ui.verticalLayout_Views.insertWidget(0, item)
    #
    # def open_accounts(self):
    #     self.controller.open_accounts_window()
    #
    # def play(self):
    #     self.controller.start_mailing()
    #
    # def pause(self):
    #     self.controller.pause_mailing()
    #
    # def stop(self):
    #     self.controller.stop_mailing()
    #
    # def change_player_state(self, is_play, is_pause, is_stop):
    #     self.ui.pushButton_play.setEnabled(is_play)
    #     self.ui.pushButton_pause.setEnabled(is_pause)
    #     self.ui.pushButton_stop.setEnabled(is_stop)
    #
    # @pyqtSlot(str, bool)
    # def print_log(self, text, time=None):
    #     if time:
    #         text = '[ {0} ] {1}'.format(strftime("%H:%M:%S", time), text)
    #     else:
    #         text = '{0}'.format(text)
    #     self.ui.plainText_log.appendPlainText(text)
    #
    # @pyqtSlot(int, int)
    # def print_progress(self, count: int, total: int):
    #     self.ui.progressBar_mailing.setValue(count)
    #     self.ui.progressBar_mailing.setMaximum(total if total else 1)
    #     self.ui.label_sendedMails.setText(f'Sended : {count:>6} / {total:<6}')
