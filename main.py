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

    def add_child(self, child):
        child_ui = QWidget()
        uic.loadUi('uis\\child_card.ui', child_ui)
        child_ui.child_label.setText(child['label']['rus'])
        return child_ui


    def initUI(self, args):
        uic.loadUi('uis\\parent_form.ui', self)
        for _ in user.get_children():
            self.child_list.addWidget(self.add_child(_))
        self.setWindowTitle(user.get_name())
        self.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = AuthorizationForm()
    sys.exit(app.exec())
