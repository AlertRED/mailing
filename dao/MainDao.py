
class MainDao:

    def __init__(self, model, controller):
        self.model = model
        self.controller = controller

    def openDataWindow(self):
        self.controller.dataWindowModel.show()

    def openAccountsWindow(self):
        self.controller.accountsWindowModel.show()



