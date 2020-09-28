from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
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

    def onClickActionData(self):
        self.controller.open_data_window()

    def onClickActionAccounts(self):
        self.controller.open_accounts_window()

    def play(self):
        self.printLog('Рассылка начата', with_time=True)
        self.controller.start_mailing()

    def pause(self):
        self.printLog('Рассылка приостановленна', with_time=True)
        self.controller.pause_mailing()

    def stop(self):
        self.printLog('Рассылка окончена', with_time=True)
        self.controller.stop_mailing()

    @pyqtSlot(str, bool)
    def printLog(self, text, with_time=True):
        if with_time:
            text = '[ {0} ] {1}'.format(strftime("%H:%M:%S", gmtime()), text)
        self.ui.plainText_log.appendPlainText(text)
