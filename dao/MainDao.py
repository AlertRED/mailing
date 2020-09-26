
class MainDao:

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller

    def openDataWindow(self):
        self.controller.dataView.show()

    def openAccountsWindow(self):
        self.controller.accountsView.show()



