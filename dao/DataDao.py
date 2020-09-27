from model.Model import Model


class DataDao:

    def __init__(self, model: Model):
        self.model = model

    def set_xlsx(self, path):
        self.model.load_xlsx(path)

    def get_sheets(self):
        return self.model.get_sheets()

    def load_sheet(self, sheet):
        return self.model.get_data_from_sheet(sheet)

    def set_email_column(self, email_column):
        return self.model.set_email_column(email_column)

    def save_settings(self, path_xlsx, sheet, email_column, message):
        self.model.save_settings("Data",
                                 {'path_xlsx': path_xlsx, 'sheet': sheet, 'email_column': email_column,
                                  'message': message})

    def load_settings(self):
        settings = self.model.get_settings("Data")
        return settings.get('path_xlsx'), settings.get('sheet'), settings.get('email_column'), settings.get('message')
