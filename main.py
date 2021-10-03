import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit

# API_URL = 'http://127.0.0.1:12345'
from PyQt5 import uic

API_URL = 'http://192.168.88.15:12345'
user = None


class User:
    @staticmethod
    def create(json):
        #print(json)
        if json['type'] == 'parent':
            return Parent(json['name'], json['children'])
        else:
            raise ValueError('Неизвестный тип пользователя')

    def is_parent(self):
        return isinstance(self, Parent)

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name


class Parent(User):
    def __init__(self, name, children):
        super().__init__(name)
        self.children = children

    def get_children(self):
        return self.children


class AuthorizationForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('uis\\login.ui', self)
        self.auth_error.hide()
        self.pushButton.clicked.connect(self.authorise)
        self.show()
        self.username_input.setText('user1')
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
        else:
            raise ValueError()


class ParentForm(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        uic.loadUi('uis\\parent_form.ui', self)
        for _ in user.get_children():
            self.child_list.addWidget(ChildWidget(_))
        self.setWindowTitle(user.get_name())
        self.show()


class ChildWidget(QWidget):
    def __init__(self, child):
        super().__init__()
        uic.loadUi('uis\\child_card.ui', self)
        self.child_label.setText(child['label']['rus'])
        self.pushButton.clicked.connect(self.choose_time)
        self.child_obj = child
        self.time_list.hide()
        self.choose_timebutton.hide()
        self.choose_timebutton.clicked.connect(self.save_time)

    def choose_time(self):
        self.time_list.show()
        self.pushButton.hide()
        self.choose_timebutton.show()
        for _ in self.child_obj['times']:
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
