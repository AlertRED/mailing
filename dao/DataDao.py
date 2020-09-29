from model.ValidateModel import ValidateModel
from model.XlsxModel import XlsxModel
from settings import Settings


class DataDao:

    def __init__(self, validate_model: ValidateModel, settings: Settings, xlsx_model: XlsxModel):
        self.validate_model = validate_model
        self.settings = settings
        self.xlsx_model = xlsx_model

    def get_sheets(self):
        return self.xlsx_model.get_sheets()

    def load_sheet(self, sheet):
        self.xlsx_model.load_data_from_sheet(sheet)
        data = self.xlsx_model.get_data()
        return data

    def load_xlsx(self, path):
        if self.validate_model.is_validate_xlsx(path):
            self.xlsx_model.load_xlsx(path)

    def save_settings(self, path_xlsx, sheet, email_column, message):
        self.settings.add_settings({'path_xlsx': path_xlsx, 'sheet': sheet, 'email_column': email_column,
                                  'message': message})

    def load_settings(self):
        return self.settings.get_settings('path_xlsx'), self.settings.get_settings('sheet'), self.settings.get_settings('email_column'), self.settings.get_settings('message')
