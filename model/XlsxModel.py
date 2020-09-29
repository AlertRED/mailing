import os
import pandas as pd


class XlsxModel:

    def __init__(self):
        self.xlsx_data = None
        self.file = None
        self.fields = dict()
        self.titles = list()

    def load_xlsx(self, path):
        self.file = pd.ExcelFile(path)
        # self.xlsx_data = self.xlsx_data.fillna('')

    def get_sheets(self):
        if self.file:
            return self.file.sheet_names
        return []

    def load_data_from_sheet(self, sheet):
        if self.file:
            # self.file = pd.ExcelFile("path")
            data_dict = self.file.parse(sheet, dtype=str).fillna('').to_dict("list")
            self.fields = list(zip(*data_dict.values()))
            self.titles = list(data_dict.keys())

    def get_data(self):
        return self.titles, self.fields
