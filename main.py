import datetime
import os
import sys
import datetime as dt

import requests
from PyQt5.QtWidgets import QApplication, QWidget, QSpacerItem, QSizePolicy, QLabel
from PyQt5.QtWidgets import QMainWindow

from user import User

API_URL = 'http://127.0.0.1:12345/'
from PyQt5 import uic

# API_URL = 'http://192.168.88.15:12345'
user = None
DELTA_MIN = 15


def load_ui(ui, obj):
    uic.loadUi(os.path.join('uis', ui), obj)


class AuthorizationForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        load_ui('login.ui', self)
        self.auth_error.hide()
        self.pushButton.clicked.connect(self.authorise)
        self.show()
        # self.username_input.setText('teacher')
        # self.password_input.setText('1234')

    def show_error(self, message='Ошибка авторизации'):
        self.auth_error.setText(message)
        self.auth_error.show()

    def authorise(self):
        global user
        self.auth_error.hide()
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            r = requests.get(API_URL + username + '.json', auth=(username, password), timeout=2)
            if r.status_code != 200:
                raise ValueError()
            user = User.create(r.json())
            self.form = self.create_main_form()
            self.hide()
        except (ValueError, requests.exceptions.RequestException):
            self.show_error()

    def create_main_form(self):
        if user.is_parent():
            return ParentForm()
        elif user.is_teacher():
            return TeacherForm()
        else:
            raise ValueError()


class ParentForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        load_ui('parent_form.ui', self)
        for _ in user.get_children():
            self.child_list.addWidget(ChildWidget(_, user.get_times()))
        self.setWindowTitle(user.get_name())
        self.show()


class TeacherForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        load_ui('parent_form.ui', self)
        self.setWindowTitle(user.get_name())
        for time, childlist in user.get_children().items():
            lbl = QLabel()
            lbl.setText(time)
            lbl.setStyleSheet('QLabel { font-size: 18pt; font-weight: bold; margin-top: 10px }')
            self.child_list.addWidget(lbl)
         # self.child_list.addWidget(TimeWidget(time, childlist))
            for childitem in childlist:
                lblc = QLabel()
                lblc.setText(childitem['label']['eng'])
                lblc.setStyleSheet('QLabel { font-size: 14pt; margin-left: 20px }')
                self.child_list.addWidget(lblc)
                #     self.child_list.addWidget(ChildItemWidget(childitem))

        # verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.child_list.addItem(verticalSpacer)
        self.show()


class ChildWidget(QWidget):
    def __init__(self, child, times):
        super().__init__()
        load_ui('child_card.ui', self)
        self.child_label.setText(child['label']['rus'])
        self.pushButton.clicked.connect(self.choose_time)
        self.child_obj = child
        self.times = times
        self.time_list.hide()
        self.choose_timebutton.hide()
        self.choose_timebutton.clicked.connect(self.save_time)

    def filter_time(self, tim):
        h, m = tim.split(':')
        time_real = dt.time(int(h), int(m))
        return time_real > (dt.datetime.now() + dt.timedelta(minutes=DELTA_MIN)).time()

    def choose_time(self):
        self.time_list.show()
        self.pushButton.hide()
        self.choose_timebutton.show()
        for _ in list(filter(self.filter_time, self.times)):
            self.time_list.addItem(_)

    def save_time(self):
        print(self.time_list.currentText())
        self.pushButton.show()
        self.time_list.hide()
        self.choose_timebutton.hide()


class TimeWidget(QWidget):
    def __init__(self, time, childlist):
        super().__init__()
        load_ui('teacher_time.ui', self)
        self.time_title.setText(time)
        # for childitem in childlist:
        #     self.child_container.addWidget(ChildItemWidget(childitem))





class ChildItemWidget(QWidget):
    def __init__(self, item):
        super().__init__()
        load_ui('child_item.ui', self)
        self.child_name.setText(item['label']['eng'])


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = AuthorizationForm()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
