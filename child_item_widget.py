from PyQt5.QtWidgets import QWidget, QCheckBox

from server.school.application_status import ApplicationStatus
from base_form import BaseForm
from globals import Globals


class ChildItemWidget(QCheckBox, BaseForm):
    def __init__(self, item):
        super().__init__()
        self.clicked.connect(self.set_status)
        self.item = item
        self.render_ui()

    def is_enabled(self):
        return self.item['application'] != '' \
               and self.item['application']['status'] == ApplicationStatus.CREATED

    def is_checked(self):
        return self.item['application'] != '' \
               and self.item['application']['status'] in [
                   ApplicationStatus.RELEASED,
                   ApplicationStatus.GATHERED
               ]

    def render_ui(self):
        self.setText(self.item['label']['eng'])
        self.setStyleSheet('QCheckBox { font-size: 14pt; margin-left: 20px }')
        self.setEnabled(self.is_enabled())
        self.setChecked(self.is_checked())

    def set_status(self):
        if not Globals.api.set_application_status(self.item['id'], ApplicationStatus.RELEASED):
            return
        self.setEnabled(False)
