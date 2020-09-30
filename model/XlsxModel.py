import pandas as pd


class XlsxModel:

    def __init__(self):
        self.file = None
        self.fields = dict()
        self.headers = list()
        self.sheet = None

    def load_xlsx(self, path):
        self.file = pd.ExcelFile(path)
        # self.xlsx_data = self.xlsx_data.fillna('')

    def get_sheets(self):
        if self.file:
            return self.file.sheet_names
        return []

    def load_data_from_sheet(self, sheet):
        if self.file and self.sheet != sheet:
            self.sheet = sheet
            # self.file = pd.ExcelFile("path")
            data_dict = self.file.parse(sheet, dtype=str).fillna('').to_dict("list")
            self.fields = list(zip(*data_dict.values()))
            self.headers = list(data_dict.keys())

    def copy_to(self, other):
        other.file = self.file
        other.fields = self.fields
        other.headers = self.headers

    def get_data(self):
        return self.headers, self.fields

    # def get_sheets(self, path):
    #
    # def get_data_from_sheet(self, sheet):
    #     if self.file:
    #         # self.file = pd.ExcelFile("path")
    #         data_dict = self.file.parse(sheet, dtype=str).fillna('').to_dict("list")
    #         file = list(zip(*data_dict.values()))
    #         titles = list(data_dict.keys())
    #         return titles, file
