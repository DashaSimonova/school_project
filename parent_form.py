from PyQt5.QtWidgets import QMainWindow
from base_form import BaseForm
from child_widget import ChildWidget
from globals import Globals


class ParentForm(QMainWindow, BaseForm):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.load_ui('parent_form.ui')
        for _ in Globals.parent().get_children():
            self.child_list.addWidget(ChildWidget(_, Globals.parent().get_times()))
        self.setWindowTitle(Globals.parent().get_name())
        self.show()


