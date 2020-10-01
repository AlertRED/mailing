import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from view.qt import AccountsWindow


class AccountsWindowView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.ui = AccountsWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.radioButton_single.toggled.connect(self.on_select_radio_button_single)
        self.ui.radioButton_multiple.toggled.connect(self.on_select_radio_button_multiple_multiple)
        self.ui.radioButton_single.setChecked(True)
        self.ui.pushButton_test.clicked.connect(self.test_login)
        self.ui.pushButton_browseTxt.clicked.connect(self.browse_choose_path)
        self.ui.pushButton_accept.clicked.connect(self.accept)
        self.ui.pushButton_accept.setEnabled(False)
        self.ui.lineEdit_password.textChanged.connect(self.changed_email_and_password)
        self.ui.lineEdit_login.textChanged.connect(self.changed_email_and_password)
        self.ui.lineEdit_pathTxt.textChanged.connect(self.changed_path_txt)
        self.ui.pushButton_test.setEnabled(False)

    def changed_email_and_password(self):
        self.enable_accept()

    def changed_path_txt(self):
        self.enable_accept()

    def enable_accept(self):
        if self.ui.radioButton_single.isChecked():
            not_empty = self.ui.lineEdit_password.text() != '' and self.ui.lineEdit_login.text() != ''
            self.ui.pushButton_test.setEnabled(not_empty)
        else:
            not_empty = self.ui.lineEdit_pathTxt.text() != ''
        self.ui.pushButton_accept.setEnabled(not_empty)

    def on_select_radio_button_single(self, is_select):
        self.ui.label_login.setEnabled(is_select)
        self.ui.lineEdit_login.setEnabled(is_select)
        self.ui.label_password.setEnabled(is_select)
        self.ui.lineEdit_password.setEnabled(is_select)
        self.ui.pushButton_test.setEnabled(is_select)
        if is_select:
            self.changed_email_and_password()

    def on_select_radio_button_multiple_multiple(self, is_select):
        self.ui.lineEdit_pathTxt.setEnabled(is_select)
        self.ui.pushButton_browseTxt.setEnabled(is_select)
        self.ui.label_infoTxt.setEnabled(is_select)
        if is_select:
            self.changed_path_txt()

    def test_login(self):
        email = self.ui.lineEdit_login.text()
        password = self.ui.lineEdit_password.text()
        self.controller.test_account(email, password)

    def browse_choose_path(self):
        pathOpen = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())[0]
        if pathOpen != '':
            self.ui.lineEdit_pathTxt.setText(pathOpen)

    def show_error(self, text):
        self.showStatus(text)

    def show_info(self, text):
        self.showStatus(text, False)

    def _show_status(self, message, is_error: bool = True):
        style = "QLabel { color : %s; }" % ("red" if is_error else "green")
        self.ui.label_error.setStyleSheet(style)
        self.ui.label_error.setText(("Error: %s" if is_error else "Info: %s") % message)

    # def load_settings(self, is_single, email, password, path_txt):
    #     if is_single is not None:
    #         self.ui.radioButton_single.setChecked(is_single)
    #     if email is not None:
    #         self.ui.lineEdit_login.setText(email)
    #     if password is not None:
    #         self.ui.lineEdit_password.setText(password)
    #     if path_txt is not None:
    #         self.ui.lineEdit_pathTxt.setText(path_txt)

    def accept(self):
        is_single = self.ui.radioButton_single.isChecked()
        email = self.ui.lineEdit_login.text()
        password = self.ui.lineEdit_password.text()
        path_txt = self.ui.lineEdit_pathTxt.text()

        self.controller.save_account_settings(is_single, email, password, path_txt)
        self.close()