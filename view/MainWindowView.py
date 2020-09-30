from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QCheckBox

from view.qt import MainWindow
from time import gmtime, strftime


class MainWindowView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.controller = controller
        self.ui.actionData.triggered.connect(self.onClickActionData)
        self.ui.actionAccounts.triggered.connect(self.onClickActionAccounts)
        self.ui.pushButton_play.clicked.connect(self.play)
        self.ui.pushButton_pause.clicked.connect(self.pause)
        self.ui.pushButton_stop.clicked.connect(self.stop)
        self.printProgress(0, 0)
        self.ui.pushButton_stop.setEnabled(False)
        self.ui.pushButton_pause.setEnabled(False)

    def showViews(self, texts, connects):
        for text, connect in zip(reversed(texts), reversed(connects)):
            item = QCheckBox(text)
            item.clicked.connect(connect)
            self.ui.verticalLayout_Views.insertWidget(0, item)

    def changeViewCheckboxes(self, is_checked):
        print(is_checked)

    def onClickActionData(self):
        self.controller.open_data_window()

    def onClickActionAccounts(self):
        self.controller.open_accounts_window()

    def play(self):
        self.printLog('Рассылка начата', with_time=True)
        self.controller.start_mailing()
        self.ui.pushButton_play.setEnabled(False)
        self.ui.pushButton_pause.setEnabled(True)
        self.ui.pushButton_stop.setEnabled(True)

    def pause(self):
        self.printLog('Рассылка приостановленна', with_time=True)
        self.controller.pause_mailing()
        self.ui.pushButton_play.setEnabled(True)
        self.ui.pushButton_pause.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(True)


    def stop(self):
        self.printLog('Рассылка окончена', with_time=True)
        self.controller.stop_mailing()
        self.ui.pushButton_play.setEnabled(True)
        self.ui.pushButton_pause.setEnabled(False)
        self.ui.pushButton_stop.setEnabled(False)


    @pyqtSlot(str, bool)
    def printLog(self, text, with_time=True):
        if with_time:
            text = '[ {0} ] {1}'.format(strftime("%H:%M:%S", gmtime()), text)
        self.ui.plainText_log.appendPlainText(text)

    @pyqtSlot(int, int)
    def printProgress(self, count: int, total: int):
        self.ui.progressBar_mailing.setValue(count)
        self.ui.progressBar_mailing.setMaximum(total if total else 1)
        self.ui.label_sendedMails.setText(f'Sended : {count:>6} / {total:<6}')
