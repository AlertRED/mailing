from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from view.qt import AccountsWindow


class AccountsWindowView(QtWidgets.QMainWindow):
    select_button_single_signal = pyqtSignal()
    select_button_multiple_signal = pyqtSignal()
    test_login_signal = pyqtSignal()
    change_login_signal = pyqtSignal(str)
    change_password_signal = pyqtSignal(str)
    change_path_accounts = pyqtSignal(str)
    accept_signal = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.ui = AccountsWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.radioButton_single.clicked.connect(self.select_button_single_signal)
        self.ui.radioButton_multiple.clicked.connect(self.select_button_multiple_signal)
        self.ui.pushButton_test.clicked.connect(self.test_login_signal)
        self.ui.lineEdit_password.textChanged.connect(self.change_password_signal)
        self.ui.lineEdit_login.textChanged.connect(self.change_login_signal)
        self.ui.lineEdit_pathTxt.textChanged.connect(self.change_path_accounts)
        self.ui.pushButton_accept.clicked.connect(self.accept_signal)
    #     self.ui.radioButton_single.setChecked(True)
    #     self.ui.pushButton_browseTxt.clicked.connect(self.browse_choose_path)
    #     self.ui.pushButton_accept.clicked.connect(self.accept)
    #     self.ui.pushButton_accept.setEnabled(False)
    #     self.ui.lineEdit_password.textChanged.connect(self.changed_email_and_password)
    #     self.ui.lineEdit_login.textChanged.connect(self.changed_email_and_password)
    #     self.ui.lineEdit_pathTxt.textChanged.connect(self.changed_path_txt)
    #     self.ui.pushButton_test.setEnabled(False)
    #
    # def changed_email_and_password(self):
    #     self.enable_accept()
    #
    # def changed_path_txt(self):
    #     self.enable_accept()
    #
    # def enable_accept(self):
    #     if self.ui.radioButton_single.isChecked():
    #         not_empty = self.ui.lineEdit_password.text() != '' and self.ui.lineEdit_login.text() != ''
    #         self.ui.pushButton_test.setEnabled(not_empty)
    #     else:
    #         not_empty = self.ui.lineEdit_pathTxt.text() != ''
    #     self.ui.pushButton_accept.setEnabled(not_empty)
    #

    def show_test(self, is_show):
        self.ui.pushButton_test.setEnabled(is_show)

    def show_single_part(self, is_show):
        self.ui.label_login.setEnabled(is_show)
        self.ui.lineEdit_login.setEnabled(is_show)
        self.ui.label_password.setEnabled(is_show)
        self.ui.lineEdit_password.setEnabled(is_show)
        self.ui.pushButton_test.setEnabled(is_show)

    def show_multiple_part(self, is_show):
        self.ui.lineEdit_pathTxt.setEnabled(is_show)
        self.ui.pushButton_browseTxt.setEnabled(is_show)
        self.ui.label_infoTxt.setEnabled(is_show)

    def select_single_part(self):
        self.ui.radioButton_single.click()

    def select_multiple_part(self):
        self.ui.radioButton_multiple.click()

    def enable_accept(self, is_enable):
        self.ui.pushButton_accept.setEnabled(is_enable)

    def show_error(self, text):
        self._show_status(text)

    def show_info(self, text):
        self._show_status(text, False)

    def _show_status(self, message, is_error: bool = True):
        style = "QLabel { color : %s; }" % ("red" if is_error else "green")
        self.ui.label_error.setStyleSheet(style)
        self.ui.label_error.setText(("Error: %s" if is_error else "Info: %s") % message)


    #
    # def test_login(self):
    #     email = self.ui.lineEdit_login.text()
    #     password = self.ui.lineEdit_password.text()
    #     self.controller.test_account(email, password)
    #
    # def browse_choose_path(self):
    #     pathOpen = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())[0]
    #     if pathOpen != '':
    #         self.ui.lineEdit_pathTxt.setText(pathOpen)
    #
    # # def load_settings(self, is_single, email, password, path_txt):
    # #     if is_single is not None:
    # #         self.ui.radioButton_single.setChecked(is_single)
    # #     if email is not None:
    # #         self.ui.lineEdit_login.setText(email)
    # #     if password is not None:
    # #         self.ui.lineEdit_password.setText(password)
    # #     if path_txt is not None:
    # #         self.ui.lineEdit_pathTxt.setText(path_txt)
    #
    # def accept(self):
    #     is_single = self.ui.radioButton_single.isChecked()
    #     email = self.ui.lineEdit_login.text()
    #     password = self.ui.lineEdit_password.text()
    #     path_txt = self.ui.lineEdit_pathTxt.text()
    #
    #     self.controller.save_account_settings(is_single, email, password, path_txt)
    #     self.close()