import requests
from PyQt5.QtWidgets import QMainWindow

from base_form import BaseForm
from globals import Globals
from parent_form import ParentForm
from teacher_form import TeacherForm


class AuthorizationForm(QMainWindow, BaseForm):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.load_ui('login.ui')
        self.auth_error.hide()
        self.pushButton.clicked.connect(self.authorise)
        self.show()
        self.username_input.setText('parent')
        self.password_input.setText('1234')

    def show_error(self, message='Ошибка авторизации'):
        self.auth_error.setText(message)
        self.auth_error.show()

    def authorise(self):
        self.auth_error.hide()
        username = self.username_input.text()
        password = self.password_input.text()
        Globals.create_api(username, password)
        try:
            Globals.create_user()
            self.form = self.create_main_form()
            self.hide()
        except (ValueError, requests.exceptions.RequestException):
            self.show_error()

    def create_main_form(self):
        if Globals.user.is_parent():
            return ParentForm()
        elif Globals.user.is_teacher():
            return TeacherForm()
        else:
            raise ValueError()

