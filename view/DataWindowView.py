import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem

from view.qt import DataWindow


class DataWindowView(QtWidgets.QMainWindow):

    def __init__(self, dao):
        super().__init__()
        self.dao = dao
        self.ui = DataWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_browsPathXlsx.clicked.connect(self.onClickBrowsPathXlsx)
        self.ui.comboBox_sheets.currentIndexChanged.connect(self.select_sheet)
        self.ui.pushButton_accept.clicked.connect(self.accept)
        self.ui.lineEdit_pathXlsx.textChanged.connect(self.change_path_xlsx)
        self.ui.plainText_message.textChanged.connect(self.change_message)

    def change_path_xlsx(self):
        path = self.ui.lineEdit_pathXlsx.text()
        self.dao.set_xlsx(path)
        self.enable_accept()

    def change_message(self):
        self.enable_accept()

    def enable_accept(self):
        if self.ui.lineEdit_pathXlsx.text() and self.ui.plainText_message.toPlainText() and self.ui.comboBox_sheets.currentIndex() != -1:
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

    def select_sheet(self, index):
        if index != -1:
            text = self.ui.comboBox_sheets.currentText()
            self.dao.load_data_from_sheet(text)
        self.enable_accept()

    def show_xlsx(self, data):
        data = data
        headers = data.keys()
        self.ui.tableWidget_data.setRowCount(data.shape[0])
        self.ui.tableWidget_data.setColumnCount(data.shape[1])
        self.ui.tableWidget_data.setHorizontalHeaderLabels(headers)
        for x, header in enumerate(headers):
            for y, column_item in enumerate(data[header]):
                self.ui.tableWidget_data.setItem(y, x, QTableWidgetItem(column_item))
        self.ui.tableWidget_data.resizeColumnsToContents()

    def load_settings(self, path, message):
        if path is not None:
            self.ui.lineEdit_pathXlsx.setText(path)
        if message is not None:
            self.ui.plainText_message.setPlainText(message)

    def accept(self):
        path_xlsx = self.ui.lineEdit_pathXlsx.text()
        message = self.ui.plainText_message.toPlainText()
        index = self.ui.comboBox_sheets.currentText()
        self.dao.save_settings(path_xlsx, message)
        self.close()
