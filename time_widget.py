from PyQt5.QtWidgets import QWidget, QLabel

from base_form import BaseForm
from child_item_widget import ChildItemWidget


class TimeWidget(QWidget, BaseForm):
    def __init__(self, time, childlist):
        super().__init__()
        self.load_ui('teacher_time.ui')
        self.time_title.setText(time)
        for childitem in childlist:
            self.child_container.addWidget(QLabel().setText(childitem['label']['eng']), 1)
            # self.child_container.addWidget(ChildItemWidget(childitem))