import os
import sys
import datetime as dt

import requests
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow
from user import User

# API_URL = 'http://127.0.0.1:12345/index.json'
from PyQt5 import uic

API_URL = 'http://192.168.88.15:12345'
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
        self.username_input.setText('mr.gerson')
        self.password_input.setText('1234')

    def show_error(self, message='Ошибка авторизации'):
        self.auth_error.setText(message)
        self.auth_error.show()

    def authorise(self):
        global user
        self.auth_error.hide()
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            r = requests.get(API_URL, auth=(username, password), timeout=2)
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
            self.child_list.addWidget(ChildWidget(_))
        self.setWindowTitle(user.get_name())
        self.show()


class TeacherForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        load_ui('parent_form.ui', self)
        # for _ in user.get_children():
        #     self.child_list.addWidget(ChildWidget(_))
        self.setWindowTitle(user.get_name())
        self.show()


class ChildWidget(QWidget):
    def __init__(self, child):
        super().__init__()
        load_ui('child_card.ui', self)
        self.child_label.setText(child['label']['rus'])
        self.pushButton.clicked.connect(self.choose_time)
        self.child_obj = child
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
        for _ in list(filter(self.filter_time, self.child_obj['times'])):
            self.time_list.addItem(_)

    def save_time(self):
        print(self.time_list.currentText())
        self.pushButton.show()
        self.time_list.hide()
        self.choose_timebutton.hide()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        frm = AuthorizationForm()
        sys.exit(app.exec())
    except Exception as e:
        print(str(e))
