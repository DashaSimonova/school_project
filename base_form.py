import os

from PyQt5 import uic


class BaseForm:
    def load_ui(self, ui):
        uic.loadUi(os.path.join('uis', ui), self)