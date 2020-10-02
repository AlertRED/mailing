import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

from view.qt import DataWindow


class DataWindowView(QtWidgets.QMainWindow):
    browse_xlsx_signal = pyqtSignal()
    change_path_xlsx_signal = pyqtSignal(str)
    change_sheet_signal = pyqtSignal(str)
    change_email_header_signal = pyqtSignal(str)
    change_title_signal = pyqtSignal(str)
    change_message_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = DataWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_browsPathXlsx.clicked.connect(self.browse_xlsx_signal)
        self.ui.lineEdit_pathXlsx.textChanged.connect(self.change_path_xlsx_signal)
        self.ui.comboBox_sheets.currentTextChanged.connect(self.change_sheet_signal)
        self.ui.comboBox_emailColumn.currentTextChanged.connect(self.change_email_header_signal)
        self.ui.lineEdit_title.textChanged.connect(self.change_title_signal)
        self.ui.plainText_message.textChanged.connect(
            lambda: self.change_message_signal.emit(self.ui.plainText_message.toPlainText()))

        #     self.ui.pushButton_accept.clicked.connect(self.accept)
        #     self.ui.lineEdit_title.textChanged.connect(self.change_title)
        #     self.ui.plainText_message.textChanged.connect(self.change_message)
        #     self.ui.comboBox_sheets.setEnabled(False)
        #     self.ui.comboBox_emailColumn.setEnabled(False)
        #
        # # def change_path_xlsx(self):
        # #     path = self.ui.lineEdit_pathXlsx.text()
        # #     self.controller.load_sheets(path)
        # #
        # # def path_xlsx_is_validate(self):
        # #     self.enable_accept()
        # #
        # # def change_message(self):
        # #     self.enable_accept()
        # #
        # # def change_title(self):
        # #     self.enable_accept()
        # #
        # # def enable_accept(self):
        # #     if self.ui.lineEdit_pathXlsx.text() and \
        # #             self.ui.lineEdit_title.text() and \
        # #             self.ui.plainText_message.toPlainText() and \
        # #             self.ui.comboBox_sheets.currentIndex() != -1 and \
        # #             self.ui.comboBox_emailColumn.currentIndex() != -1:
        # #         self.ui.pushButton_accept.setEnabled(True)
        # #     else:
        # #         self.ui.pushButton_accept.setEnabled(False)
        # #

    def browse_xlsx(self):
        path_open = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'Excel (*.xls *.xlsx)')[0]
        self.ui.lineEdit_pathXlsx.setText(path_open)

    def enable_sheet(self, is_enable):
        self.ui.comboBox_sheets.setEnabled(is_enable)

    def enable_email_header(self, is_enable):
        self.ui.comboBox_emailColumn.setEnabled(is_enable)

    def show_sheets(self, sheets):
        self.ui.comboBox_sheets.clear()
        self.ui.comboBox_sheets.addItems(sheets)

    def show_email_headers(self, headers):
        self.ui.comboBox_emailColumn.clear()
        self.ui.comboBox_emailColumn.addItems(headers)

    def show_xlsx(self):
        pass

    def enable_accept(self, is_enable):
        self.ui.pushButton_accept.setEnabled(is_enable)

        # #
        # # def _select_sheet(self, index):
        # #     if index != -1:
        # #         sheet_name = self.ui.comboBox_sheets.currentText()
        # #         self.controller.select_sheet(sheet_name)
        # #         self.ui.comboBox_emailColumn.setEnabled(True)
        # #         self.enable_accept()
        # #     else:
        # #         self.ui.comboBox_emailColumn.clear()
        # #         self.ui.comboBox_emailColumn.setEnabled(False)
        # #
        # # def show_xlsx(self, titles, fields):
        # #     self.ui.comboBox_emailColumn.addItems(titles)
        # #     self.ui.tableWidget_data.setRowCount(len(fields))
        # #     self.ui.tableWidget_data.setColumnCount(len(titles))
        # #     self.ui.tableWidget_data.setHorizontalHeaderLabels(titles)
        # #     for x, row in enumerate(fields):
        # #         for y, item in enumerate(row):
        # #             self.ui.tableWidget_data.setItem(x, y, QTableWidgetItem(item))
        # #     self.ui.tableWidget_data.resizeColumnsToContents()
        # #
        # # # def load_settings(self, path_xlsx, sheet, email_column, message, title):
        # # #     if path_xlsx is not None:
        # # #         self.ui.lineEdit_pathXlsx.setText(path_xlsx)
        # # #     if sheet is not None:
        # # #         self.ui.comboBox_sheets.setCurrentText(sheet)
        # # #     if email_column is not None:
        # # #         self.ui.comboBox_emailColumn.setCurrentText(email_column)
        # # #     if message is not None:
        # # #         self.ui.plainText_message.setPlainText(message)
        # # #     if title is not None:
        # # #         self.ui.lineEdit_title.setText(title)
        # #
        # # def accept(self):
        # #     path_xlsx = self.ui.lineEdit_pathXlsx.text()
        # #     message = self.ui.plainText_message.toPlainText()
        # #     sheet = self.ui.comboBox_sheets.currentText()
        # #     email_column = self.ui.comboBox_emailColumn.currentText()
        # #     title = self.ui.lineEdit_title.text()
        # #     self.controller.save_data_settings(path_xlsx, sheet, email_column, message, title)
        # #     self.close()
