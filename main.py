from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QDialog, QMainWindow, QTableWidgetItem
from main_window import Ui_MainWindow
from login_dialog import Ui_LoginDialog
from find_dialog import Ui_Dialog

import pymysql


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

# TODO
# Написать функции подключения к бд, очищения таблицы, функции перехвата сигнала

# pyuic6 -x main_window.ui -o main_window.py

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.tableWidget.setColumnWidth(0, 300)  # name
        self.tableWidget.setColumnWidth(1, 50)  # year
        self.tableWidget.setColumnWidth(2, 133)  # country
        self.tableWidget.setColumnWidth(3, 133)  # genre
        self.tableWidget.setColumnWidth(4, 133)  # director
        self.tableWidget.setColumnWidth(5, 49)  # rating
        self.addButton.hide()
        self.delButton.hide()


        self.loadButton.clicked.connect(self.loadDB)  # Загрузить
        self.loginButton.clicked.connect(self.loginButtonClicked) # Войти
        self.findButton.clicked.connect(self.findButtonClicked) # Найти

    def loginButtonClicked(self):
        log_d = LoginDialog(self)
        log_d.exec()
        # if admin -> to reveal add and delete buttons
        # TODO

    def loadDB(self):
        # TODO
        try:
            connection = pymysql.connect(
                host='localhost',
                port='3306',
                user='user',
                database='db_name',
                cursorclass=pymysql.cursors.DictCursor
            )
            print('success\n# * 20')

            try:
                with connection.cursor() as cur:
                    get_data_query = 'SELECT * FROM'
                    i = 0
                    for row in cur.execute(get_data_query):
                        self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # name
                        self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # year
                        self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # country
                        self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # genre
                        self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # director
                        self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # rating
                        i += 1
            finally:
                connection.close()
        except Exception as ex:
            print('Connection failed')
            print(ex)

    def findButtonClicked(self):
        find_d = FindDialog(self)
        find_d.exec()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
