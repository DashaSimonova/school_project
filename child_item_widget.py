from PyQt5.QtWidgets import QWidget

from base_form import BaseForm


class ChildItemWidget(QWidget, BaseForm):
    def __init__(self, item):
        super().__init__()
        self.load_ui('child_item.ui')
        self.child_name.setText(item['label']['eng'])