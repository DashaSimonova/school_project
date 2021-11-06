from PyQt5.QtWidgets import QWidget, QLabel

from base_form import BaseForm

class TimeWidget(QLabel, BaseForm):
    def __init__(self, time):
        super().__init__()
        self.setText(time)
        self.setStyleSheet('QLabel { font-size: 18pt; font-weight: bold }')