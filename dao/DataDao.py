class DataDao:

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller

    def set_xlsx(self, path):
        self.model.load_xlsx(path)
        sheets = self.get_sheets()
        self.controller.dataWindowModel.show_sheets(sheets)

    def get_sheets(self):
        return self.model.get_sheets()

    def load_data_from_sheet(self, sheet):
        data = self.model.get_data_from_sheet(sheet)
        self.controller.dataWindowModel.show_xlsx(data)

    def save_settings(self, path_xlsx, message):
        self.model.save_settings("Data",
                                 {'path_xlsx': path_xlsx, 'message': message})

    def load_settings(self):
        settings = self.model.get_settings("Data")
        self.controller.dataWindowModel.load_settings(settings.get('path_xlsx'), settings.get('message'))
