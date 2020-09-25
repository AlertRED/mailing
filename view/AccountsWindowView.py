import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from view.qt import AccountsWindow
import re


class AccountsWindowView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.ui = AccountsWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.radioButton_single.toggled.connect(self.onSelectRadioButton_single)
        self.ui.radioButton_multiple.toggled.connect(self.onSelectRadioButton_multiple)
        self.ui.radioButton_single.setChecked(True)
        self.ui.pushButton_test.clicked.connect(self.onClickTest)
        self.ui.pushButton_browseTxt.clicked.connect(self.onClickBrowse)
        self.ui.pushButton_accept.clicked.connect(self.accept)
        self.ui.pushButton_accept.setEnabled(False)
        self.ui.lineEdit_password.textChanged.connect(self.changedEmailAndPassword)
        self.ui.lineEdit_login.textChanged.connect(self.changedEmailAndPassword)
        self.ui.pushButton_test.setEnabled(False)


    def changedEmailAndPassword(self):
        not_empty = self.ui.lineEdit_password.text() != '' and self.ui.lineEdit_login.text() != ''
        self.ui.pushButton_accept.setEnabled(not_empty)
        self.ui.pushButton_test.setEnabled(not_empty)


    def onSelectRadioButton_single(self, is_select):
        self.ui.label_login.setEnabled(is_select)
        self.ui.lineEdit_login.setEnabled(is_select)
        self.ui.label_password.setEnabled(is_select)
        self.ui.lineEdit_password.setEnabled(is_select)
        self.ui.pushButton_test.setEnabled(is_select)

    def onSelectRadioButton_multiple(self, is_select):
        self.ui.lineEdit_pathTxt.setEnabled(is_select)
        self.ui.pushButton_browseTxt.setEnabled(is_select)
        self.ui.label_infoTxt.setEnabled(is_select)

    def onClickTest(self):
        email = self.ui.lineEdit_login.text()
        password = self.ui.lineEdit_password.text()
        self.controller.onClickTestAccount(email, password)

    def onClickBrowse(self):
        pathOpen = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())[0]
        if pathOpen != '':
            self.ui.lineEdit_pathTxt.setText(pathOpen)

    def showEmailIsNotValidate(self):
        self.showStatus('Email is not validate', True)

    def showAccountIsConnected(self, is_connected):
        if is_connected:
            self.showStatus('Account is connected', False)
        else:
            self.showStatus('Account is not connected', True)

    def showEmailNotValidate(self):
        self.showStatus('Email is not validate')

    def showStatus(self, message, is_error: bool = True):
        style = "QLabel { color : %s; }" % ("red" if is_error else "green")
        self.ui.label_error.setStyleSheet(style)
        self.ui.label_error.setText(("Error: %s" if is_error else "Info: %s") % message)

    def accept(self):
        self.close()
