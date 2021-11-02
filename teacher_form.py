from PyQt5.QtWidgets import QMainWindow, QLabel

from base_form import BaseForm
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
                lblc = QLabel()
                lblc.setText(childitem['label']['eng'])
                lblc.setStyleSheet('QLabel { font-size: 14pt; margin-left: 20px }')
                self.child_list.addWidget(lblc)
                #     self.child_list.addWidget(ChildItemWidget(childitem))

        # verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.child_list.addItem(verticalSpacer)
        self.show()
