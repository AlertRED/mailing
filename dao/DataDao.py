class DataDao:

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller

    def set_xlsx(self, path):
        self.model.set_xlsx(path)

    def get_sheets(self):
        return self.model.get_sheets()

    def load_data_from_sheet(self, sheet):
        data = self.model.get_data_from_sheet(sheet)
        self.controller.dataWindowModel.show_xlsx(data)
