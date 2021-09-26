import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit

# API_URL = 'http://127.0.0.1:12345'
API_URL = 'http://192.168.88.15:12345'
user = None


class User(object):
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

    def num_children(self):
        return len(self.children)


class AuthorizationForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)

        self.username_input = QLineEdit()
        layout.addWidget(QLabel('Логин:'))
        layout.addWidget(self.username_input)

        layout.addSpacerItem(QSpacerItem(0, 20, vPolicy=QSizePolicy.Minimum))

        self.password_input = QLineEdit()
        layout.addWidget(QLabel('Пароль:'))
        layout.addWidget(self.password_input)

        self.auth_error = QLabel()
        self.auth_error.setStyleSheet('QLabel { color: "red" }')
        self.auth_error.hide()
        layout.addWidget(self.auth_error)

        layout.addSpacerItem(QSpacerItem(1, 1, vPolicy=QSizePolicy.Expanding))

        button = QPushButton('Вход')
        button.clicked.connect(self.authorise)
        layout.addWidget(button)

        wid = QWidget(self)
        wid.setLayout(layout)
        self.setCentralWidget(wid)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Авторизация')
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
        except (ValueError, requests.exceptions.RequestException):
            self.show_error()

    def create_main_form(self):
        if user.is_parent():
            return ParentForm()
        else:
            raise ValueError()


class ParentForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(user.get_name() + ":" + str(user.num_children()) + " children"))
        self.setLayout(layout)
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Форма родителя')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    frm = AuthorizationForm()
    sys.exit(app.exec())
