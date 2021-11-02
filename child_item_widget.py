from PyQt5.QtWidgets import QWidget, QCheckBox

from server.school.application_status import ApplicationStatus
from base_form import BaseForm
from globals import Globals


class ChildItemWidget(QCheckBox, BaseForm):
    def __init__(self, item):
        super().__init__()
        # self.load_ui('child_item.ui')
        # self.child_name.setText(item['label']['eng'])
        self.item = item
        self.setText(item['label']['eng'])
        self.setStyleSheet('QCheckBox { font-size: 14pt; margin-left: 20px }')
        if item['application'] == '':
            self.setEnabled(False)
        elif item['application']['status'] != ApplicationStatus.CREATED:
            self.setChecked(True)
            self.setEnabled(False)
        else:
            self.clicked.connect(self.set_status)

    def set_status(self):
        Globals.api.set_application_status(self.item['id'], ApplicationStatus.RELEASED)
        self.setEnabled(False)
