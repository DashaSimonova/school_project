import datetime as dt

from PyQt5.QtWidgets import QWidget

from base_form import BaseForm
from globals import Globals
from server.school.application_status import ApplicationStatus

DELTA_MIN = 15


class ChildWidget(QWidget, BaseForm):
    def __init__(self, child, times):
        super().__init__()
        self.load_ui('child_card.ui')
        self.child_obj = child
        self.times = times

        application = self.child_obj['application']
        if application != '':
            self.appTime = dt.datetime.fromisoformat(self.child_obj['application']['date']).strftime('%H:%M')
        else:
            self.appTime = None

        self.pushButton.clicked.connect(self.choose_time)
        self.choose_timebutton.clicked.connect(self.save_time)
        self.render_ui()

    def filter_time(self, tim):
        h, m = tim.split(':')
        time_real = dt.time(int(h), int(m))
        return time_real > (dt.datetime.now() + dt.timedelta(minutes=DELTA_MIN)).time()

    def choose_time(self):
        self.time_list.show()
        self.pushButton.hide()
        self.appLabel.hide()
        self.choose_timebutton.show()
        for time in list(filter(self.filter_time, self.times)):
            self.time_list.addItem(time)
        if self.appTime is not None:
            index = self.time_list.findText(self.appTime)
            if index >= 0:
                self.time_list.setCurrentIndex(index)

    def save_time(self):
        self.appTime = self.time_list.currentText()
        Globals.api.create_application(self.child_obj['id'], self.appTime)
        self.render_ui()

    def render_ui(self):
        self.child_label.setText(self.child_obj['label']['rus'])
        self.time_list.hide()
        self.choose_timebutton.hide()
        self.label_alert.hide()
        if self.appTime is not None:
            self.appLabel.setText(self.appTime)
            self.appLabel.show()
            if self.child_obj['application']['status'] != ApplicationStatus.CREATED:
                self.pushButton.hide()
                self.label_alert.show()
            else:
                self.pushButton.show()
                self.pushButton.setText('Изменить')
        else:
            self.appLabel.hide()

