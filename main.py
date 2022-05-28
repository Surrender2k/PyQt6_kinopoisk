from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QMainWindow
from main_window import Ui_MainWindow
from login_dialog import Ui_LoginDialog
from find_dialog import  Ui_Dialog

# pyuic6 -x find_dialog.ui -o find_dialog.py

class FindDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)



# pyuic6 -x login_dialog.ui -o login_dialog.py

class LoginDialog(QDialog, Ui_LoginDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


# pyuic6 -x main_window.ui -o main_window.py

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0, 300) # name
        self.tableWidget.setColumnWidth(1, 50)  # year
        self.tableWidget.setColumnWidth(2, 133) # country
        self.tableWidget.setColumnWidth(3, 133) # genre
        self.tableWidget.setColumnWidth(4, 133) # director
        self.tableWidget.setColumnWidth(5, 49) # rating
        self.addButton.hide()
        self.delButton.hide()


        self.loadButton.clicked.connect(self.loadDB)
        self.loginButton.clicked.connect(self.loginButtonClicked)
        self.findButton.clicked.connect(self.findButtonClicked)

    def loginButtonClicked(self):
        log_d = LoginDialog(self)
        log_d.exec()


    def loadDB(self):
        # TODO
        pass


    def findButtonClicked(self):
        find_d = FindDialog(self)
        find_d.exec()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
