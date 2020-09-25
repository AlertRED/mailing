import os

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from view.qt import DataWindow


class DataWindowView(QtWidgets.QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.ui = DataWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_browsPathXlsx.clicked.connect(self.onClickBrowsPathXlsx)

    def onClickBrowsPathXlsx(self):
        pathOpen = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(), 'Excel (*.xls *.xlsx)')[0]
        self.ui.lineEdit_pathXlsx.setText(pathOpen)
