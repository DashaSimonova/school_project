import requests
from PyQt5.QtWidgets import QMainWindow

from administrator_form import AdministratorForm
from base_form import BaseForm
from error_message import ErrorMessage
from globals import Globals
from parent_form import ParentForm
from teacher_form import TeacherForm


class AuthorizationForm(QMainWindow, BaseForm):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.load_ui('login.ui')
        self.pushButton.clicked.connect(self.authorise)
        self.show()

    def authorise(self):
        username = self.username_input.text()
        password = self.password_input.text()
        Globals.create_api(username, password)
        if not Globals.create_user():
            return
        try:
            self.form = self.create_main_form()
        except (ValueError, TypeError) as e:
            print(e)
            return ErrorMessage.show('Ошибка авторизации')
        self.hide()

    def create_main_form(self):
        if Globals.user.is_administrator():
            return AdministratorForm()
        elif Globals.user.is_parent():
            return ParentForm()
        elif Globals.user.is_teacher():
            return TeacherForm()
        else:
            raise ValueError()

