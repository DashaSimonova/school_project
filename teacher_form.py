from PyQt5.QtWidgets import QMainWindow, QLabel, QCheckBox

from base_form import BaseForm
from child_item_widget import ChildItemWidget
from globals import Globals
from time_widget import TimeWidget


class TeacherForm(QMainWindow, BaseForm):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.load_ui('parent_form.ui')
        self.setWindowTitle(Globals.user.get_name())
        for time, childlist in Globals.teacher().get_children().items():
            # self.child_list.addWidget(TimeWidget(time, childlist), 1)
            lbl = QLabel()
            lbl.setText(time)
            lbl.setStyleSheet('QLabel { font-size: 18pt; font-weight: bold; margin-top: 10px }')
            self.child_list.addWidget(lbl)
            for childitem in childlist:
                self.child_list.addWidget(ChildItemWidget(childitem))
        self.show()
