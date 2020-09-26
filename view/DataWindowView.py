import os

from PyQt5 import QtWidgets
from PyQt5.QtCore import QMimeData
from PyQt5.QtGui import QStandardItemModel
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

    def onClickBrowsPathXlsx(self):
        pathOpen = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'Excel (*.xls *.xlsx)')[0]
        if pathOpen != '':
            self.ui.lineEdit_pathXlsx.setText(pathOpen)
            self.dao.set_xlsx(pathOpen)
            self.show_sheets()

    def show_sheets(self):
        sheets = self.dao.get_sheets()
        self.ui.comboBox_sheets.addItems(sheets)

    def select_sheet(self, index):
        text = self.ui.comboBox_sheets.itemText(index)
        self.dao.load_data_from_sheet(text)

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

    def accept(self):
        self.close()
