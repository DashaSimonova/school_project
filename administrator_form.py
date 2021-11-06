from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QPushButton

from application_dialog import ApplicationDialog
from application_utils import ApplicationUtils
from base_form import BaseForm
from globals import Globals
from server.school.application_status import ApplicationStatus


class AdministratorForm(QMainWindow, BaseForm):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        self.load_ui('administrator_form.ui')
        self.setWindowTitle(Globals.administrator().get_name())
        self.render_class_selector()
        self.render_children()

    def render_class_selector(self):
        for grade in Globals.administrator().get_grades():
            self.class_selector.addItem(grade)
        self.class_selector.currentTextChanged.connect(self.render_children)

    def get_table_item(self, label):
        item = QTableWidgetItem(label)
        item.setFlags(Qt.ItemIsSelectable)
        return item

    def create_action_button(self, child):
        if child['application'] == '':
            btn = QPushButton('Создать заявку')
            btn.clicked.connect(lambda: self.show_application_dialog(child))
            return btn

        if child['application']['status'] == ApplicationStatus.RELEASED:
            btn = QPushButton('Выдать')
            btn.clicked.connect(lambda: self.set_gathered(child['id']))
            return btn

        return None

    def show_application_dialog(self, child):
        dlg = ApplicationDialog(child)
        dlg.exec_()
        if dlg.result() == 1:
            self.update_children(
                Globals.api.create_application(child['id'], dlg.timeList.currentText()))

    def set_gathered(self, child_id):
        self.update_children(
            Globals.api.set_application_status(child_id, ApplicationStatus.GATHERED))

    def update_children(self, json):
        if not json:
            return
        Globals.administrator().children = json['children']
        self.render_children()

    def render_children(self):
        children = self.get_filtered_children()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setRowCount(len(children))
        for i, c in enumerate(children):
            self.tableWidget.setItem(i, 0, self.get_table_item(c['label']['rus']))
            self.tableWidget.setItem(i, 1, self.get_table_item(
                ApplicationUtils.get_date(c['application'])))
            self.tableWidget.setItem(i, 2, self.get_table_item(
                ApplicationUtils.get_text(c['application'])))

            btn = self.create_action_button(c)
            if btn is not None:
                self.tableWidget.setCellWidget(i, 3, btn)

    def get_filtered_children(self):
        return list(filter(
            lambda c: c['grade'] == self.class_selector.currentText(),
            Globals.administrator().get_children()
        ))
