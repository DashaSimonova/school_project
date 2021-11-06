from PyQt5.QtWidgets import QDialog

from base_form import BaseForm
from globals import Globals


class ApplicationDialog(QDialog, BaseForm):
    def __init__(self, child):
        super().__init__()
        self.load_ui('create_application_dialog.ui')
        self.add_times()
        self.setModal(True)
        self.show()

    def add_times(self):
        for time in Globals.administrator().get_future_times():
            self.timeList.addItem(time)
