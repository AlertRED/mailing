from model.ValidateModel import ValidateModel
from model.XlsxModel import XlsxModel
from settings import Settings


class DataDao:

    def __init__(self, validate_model: ValidateModel, settings: Settings, xlsx_model: XlsxModel):
        self.validate_model = validate_model
        self.settings = settings
        self.xlsx_model = xlsx_model
        self.pre_xlsx_model = XlsxModel()

        self.path_xlsx = None
        self.sheet = None
        self.email_column = None
        self.message = None
        self.title = None

    def get_sheets(self):
        return self.pre_xlsx_model.get_sheets()

    def load_sheet(self, sheet):
        self.pre_xlsx_model.load_data_from_sheet(sheet)
        data = self.pre_xlsx_model.get_data()
        return data

    def load_xlsx(self, path):
        if self.validate_model.is_validate_xlsx(path):
            self.pre_xlsx_model.load_xlsx(path)

    def save_settings(self, path_xlsx, sheet, email_column, message, title):
        self.pre_xlsx_model.copy_to(self.xlsx_model)
        self.settings.add_settings({'path_xlsx': path_xlsx, 'sheet': sheet, 'email_column': email_column,
                                    'message': message, 'title': title})

    def load_settings(self):
        self.path_xlsx = self.settings.get_settings('path_xlsx')
        self.sheet = self.settings.get_settings('sheet')
        self.email_column = self.settings.get_settings('email_column')
        self.message = self.settings.get_settings('message')
        self.title = self.settings.get_settings('title')

        self.xlsx_model.load_xlsx(self.path_xlsx)
        self.xlsx_model.load_data_from_sheet(self.sheet)

        self.xlsx_model.copy_to(self.pre_xlsx_model)

    def get_settings(self):
        return self.path_xlsx, self.sheet, self.email_column, self.message, self.title
