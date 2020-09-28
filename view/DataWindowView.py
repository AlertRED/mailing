import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

from view.qt import DataWindow


class DataWindowView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.ui = DataWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_browsPathXlsx.clicked.connect(self.onClickBrowsPathXlsx)
        self.ui.comboBox_sheets.currentIndexChanged.connect(self.select_sheet)
        self.ui.comboBox_emailColumn.currentIndexChanged.connect(self.select_email_column)
        self.ui.pushButton_accept.clicked.connect(self.accept)
        self.ui.lineEdit_pathXlsx.textChanged.connect(self.change_path_xlsx)
        self.ui.plainText_message.textChanged.connect(self.change_message)
        self.ui.comboBox_sheets.setEnabled(False)
        self.ui.comboBox_emailColumn.setEnabled(False)

    def change_path_xlsx(self):
        path = self.ui.lineEdit_pathXlsx.text()
        self.controller.load_xlsx(path)
        self.enable_accept()

    def change_message(self):
        self.enable_accept()

    def enable_accept(self):
        if self.ui.lineEdit_pathXlsx.text() and self.ui.plainText_message.toPlainText() and self.ui.comboBox_sheets.currentIndex() != -1 and self.ui.comboBox_emailColumn.currentIndex() != -1:
            self.ui.pushButton_accept.setEnabled(True)
        else:
            self.ui.pushButton_accept.setEnabled(False)

    def onClickBrowsPathXlsx(self):
        pathOpen = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'Excel (*.xls *.xlsx)')[0]
        if pathOpen != '':
            self.ui.lineEdit_pathXlsx.setText(pathOpen)

    def show_sheets(self, sheets):
        self.ui.comboBox_sheets.clear()
        self.ui.comboBox_sheets.addItems(sheets)
        self.ui.comboBox_sheets.setEnabled(sheets != [])

    def select_sheet(self, index):
        if index != -1:
            text = self.ui.comboBox_sheets.currentText()
            self.controller.select_sheet(text)
            self.ui.comboBox_emailColumn.setEnabled(True)
            self.enable_accept()
        else:
            self.ui.comboBox_sheets.setCurrentText(False)

    def select_email_column(self, index):
        if index != -1:
            text = self.ui.comboBox_sheets.currentText()
            self.controller.select_email(text)

    def show_xlsx(self, data):
        headers = data.keys()
        self.ui.comboBox_emailColumn.addItems(headers)
        self.ui.tableWidget_data.setRowCount(data.shape[0])
        self.ui.tableWidget_data.setColumnCount(data.shape[1])
        self.ui.tableWidget_data.setHorizontalHeaderLabels(headers)
        for x, header in enumerate(headers):
            for y, column_item in enumerate(data[header]):
                self.ui.tableWidget_data.setItem(y, x, QTableWidgetItem(column_item))
        self.ui.tableWidget_data.resizeColumnsToContents()

    def load_settings(self, path_xlsx, sheet, email_column, message):
        if path_xlsx is not None:
            self.ui.lineEdit_pathXlsx.setText(path_xlsx)
        if sheet is not None:
            self.ui.comboBox_sheets.setCurrentText(sheet)
        if email_column is not None:
            self.ui.comboBox_emailColumn.setCurrentText(email_column)
        if message is not None:
            self.ui.plainText_message.setPlainText(message)

    def accept(self):
        path_xlsx = self.ui.lineEdit_pathXlsx.text()
        message = self.ui.plainText_message.toPlainText()
        sheet = self.ui.comboBox_sheets.currentText()
        email_column = self.ui.comboBox_emailColumn.currentText()
        self.controller.save_data_settings(path_xlsx, sheet, email_column, message)
        self.close()
