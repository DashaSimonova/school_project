from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from base_form import BaseForm
from child_item_widget import ChildItemWidget
from globals import Globals
from time_widget import TimeWidget


class TeacherForm(QMainWindow, BaseForm):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.load_ui('parent_form.ui')
        self.setWindowTitle(Globals.user.get_name())
        self.child_list.setAlignment(Qt.AlignTop)
        for time, childlist in sorted(Globals.teacher().get_children().items()):
            self.child_list.addWidget(TimeWidget(time))
            for childitem in childlist:
                self.child_list.addWidget(ChildItemWidget(childitem))
        self.show()
