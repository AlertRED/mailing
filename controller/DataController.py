import threading

from PyQt5.QtCore import pyqtSignal

from view.DataWindowView import DataWindowView


class DataController:

    def __init__(self, model):
        self.data_view = DataWindowView()
        self.model = model
        self.init()

    def init(self):
        self.data_view.browse_xlsx_signal.connect(self.browse_xlsx)
        self.data_view.change_path_xlsx_signal.connect(self.change_xlsx)
        self.data_view.change_sheet_signal.connect(self.change_sheet)
        self.data_view.change_email_header_signal.connect(self.change_email_header)
        self.data_view.change_title_signal.connect(self.change_title)
        self.data_view.change_message_signal.connect(self.change_message)
        self.data_view.accept_signal.connect(self.accept)
        self.title = ""
        self.message = ""
        self.path_xlsx = ""
        self.sheet_name = ""
        self.email_header = ""
        self.headers = list()
        self.fields = list()

    def browse_xlsx(self):
        self.data_view.browse_xlsx()

    def change_xlsx(self, path):
        self.path_xlsx = path
        self.change_enable_sheets()
        self.enable_accept()

    def change_enable_sheets(self):
        if self.path_xlsx != "":
            self.data_view.enable_sheet(True)
            self.data_view.show_sheets(['Sheet1'])
        else:
            self.data_view.enable_sheet(False)
            self.data_view.show_sheets([])

    def change_sheet(self, sheet_name):
        self.sheet_name = sheet_name
        self.change_enable_email_header()
        self.load_table()
        self.enable_accept()

    def load_table(self):
        headers, fields = self.model.get_xlsx(self.path_xlsx, self.sheet_name)
        self.data_view.show_xlsx(headers, fields)

    def change_enable_email_header(self):
        if self.sheet_name != "":
            self.data_view.enable_email_header(True)
            self.data_view.show_email_headers(['header1', 'header2'])
        else:
            self.data_view.enable_email_header(False)
            self.data_view.show_email_headers([])

    def change_email_header(self, header_name):
        self.email_header = header_name
        self.enable_accept()

    def change_title(self, title):
        self.title = title
        self.enable_accept()

    def change_message(self, message):
        self.message = message
        self.enable_accept()

    def enable_accept(self):
        is_enable = self.path_xlsx != "" \
                    and self.sheet_name != "" \
                    and self.email_header != "" \
                    and self.title != "" \
                    and self.message != ""
        self.data_view.enable_accept(is_enable)

    def accept(self):
        self.model.accept_data(self.title, self.message, self.path_xlsx, self.sheet_name, self.email_header)
        self.data_view.close()

    def run(self):
        self.change_enable_sheets()
        self.change_enable_email_header()
        self.enable_accept()
        self.data_view.show()
