import pandas as pd

class Model:

    def __init__(self):
        self.password = ""
        self.login = ""
        self.path_accounts = ""
        self.is_single = True

        self.path_xlsx = ""
        self.sheet_name = ""
        self.email_header = ""
        self.title = ""
        self.message = ""

        self.is_play = False
        self.is_pause = False

    def test_connection(self, login, password):
        return login != '' and password != ''

    def get_xlsx(self, path, sheet):
        file = pd.ExcelFile(path)
        sheet = sheet
        # self.file = pd.ExcelFile("path")
        data_dict = file.parse(sheet, dtype=str).fillna('').to_dict("list")
        fields = list(zip(*data_dict.values()))
        headers = list(data_dict.keys())
        return headers, fields

    def accept_accounts(self, login, password, is_single, path_accounts):
        self.login = login
        self.password = password
        self.is_single = is_single
        self.path_accounts = path_accounts

    def accept_data(self, title, message, path_xlsx, sheet_name, email_header):
        self.title = title
        self.message = message
        self.path_xlsx = path_xlsx
        self.sheet_name = sheet_name
        self. email_header = email_header
