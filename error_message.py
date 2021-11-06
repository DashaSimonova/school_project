from PyQt5.QtWidgets import QMessageBox


class ErrorMessage:
    @staticmethod
    def show(message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Ошибка")
        return msg.exec_()
