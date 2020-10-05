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
    accept_signal = pyqtSignal()
    browse_attachments_signal = pyqtSignal()
    clear_attachments_signal = pyqtSignal()
    change_attachments_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.ui = DataWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_browsPathXlsx.clicked.connect(self.browse_xlsx_signal)
        self.ui.lineEdit_pathXlsx.textChanged.connect(self.change_path_xlsx_signal)
        self.ui.comboBox_sheets.currentTextChanged.connect(self.change_sheet_signal)
        self.ui.comboBox_emailColumn.currentTextChanged.connect(self.change_email_header_signal)
        self.ui.lineEdit_title.textChanged.connect(self.change_title_signal)
        self.ui.pushButton_accept.clicked.connect(self.accept_signal)
        self.ui.plainText_message.textChanged.connect(
            lambda: self.change_message_signal.emit(self.ui.plainText_message.toPlainText()))

        self.ui.pushButton_browsAttachments.clicked.connect(self.browse_attachments_signal)
        self.ui.pushButton_clearAttachments.clicked.connect(self.clear_attachments_signal)

    def browse_attachments(self):
        paths = QFileDialog.getOpenFileNames(self, 'Open file', os.getcwd())[0]
        self.change_attachments_signal.emit(paths)

    def show_attachments(self, paths):
        self.ui.listWidget_attachments.clear()
        self.ui.listWidget_attachments.addItems(paths)

    def clear_attachments(self):
        self.ui.listWidget_attachments.clear()

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

    def show_xlsx(self, titles, fields):
        self.ui.comboBox_emailColumn.addItems(titles)
        self.ui.tableWidget_data.setRowCount(len(fields))
        self.ui.tableWidget_data.setColumnCount(len(titles))
        self.ui.tableWidget_data.setHorizontalHeaderLabels(titles)
        for x, row in enumerate(fields):
            for y, item in enumerate(row):
                self.ui.tableWidget_data.setItem(x, y, QTableWidgetItem(item))
        self.ui.tableWidget_data.resizeColumnsToContents()

    def enable_accept(self, is_enable):
        self.ui.pushButton_accept.setEnabled(is_enable)
