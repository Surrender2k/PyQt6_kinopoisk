from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QAction
from main_window import Ui_MainWindow
from login_dialog import Ui_LoginDialog
from find_dialog import Ui_FindDialog
from add_dialog import Ui_AddDialog

import pymysql


# pyuic6 -x find_dialog.ui -o find_dialog.py

class FindDialog(QDialog, Ui_FindDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.findButton.clicked.connect(self.findButtonClicked)

    def findButtonClicked(self):
        if self.findEdit.text() != '':
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните корректно поля')


# pyuic6 -x login_dialog.ui -o login_dialog.py

class LoginDialog(QDialog, Ui_LoginDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.logButton.clicked.connect(self.logButtonClicked)

    def logButtonClicked(self):
        if self.check_fields():
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните корректно поля')

    def check_fields(self):
        return not (self.loginEdit.text() == '' or self.passEdit.text() == '')


# pyuic6 -x add_dialog.ui -o add_dialog.py

class AddDialog(QDialog, Ui_AddDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.addButton.clicked.connect(self.addButtonClicked)

    def addButtonClicked(self):
        if self.check_fields():
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните корректно поля')

    def check_fields(self):
        return not (self.nameEdit.text() == '' or self.yearEdit.text() or self.countryEdit.text() == ''
                    or self.genreEdit.text() or self.directorEdit.text() == '' or self.ratingEdit.text() == '')


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
        self.connection = None
        self.connectDB()

        self.loadButton.clicked.connect(self.loadDB)  # Загрузить
        self.loginButton.clicked.connect(self.loginButtonClicked)  # Войти
        self.findButton.clicked.connect(self.findButtonClicked)  # Найти

    def loginButtonClicked(self):
        log_d = LoginDialog(self)
        res = log_d.exec()
        login = log_d.loginEdit.text()
        password = log_d.passEdit.text()
        admin = False
        if login != '' != password:
            # sql query and check if admin
            # TODO
            if admin:
                self.addButton.show()
                self.delButton.show()

    def loadDB(self):
        # TODO
        try:
            with self.connection.cursor() as cur:
                get_data_query = 'SELECT * FROM pyqt6.films;'
                i = 0
                for row in cur.execute(get_data_query):
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # name
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # year
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # country
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # genre
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # director
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))  # rating
                    i += 1
        except Exception as ex:
            QMessageBox.information(self, 'Ошибка', 'Подключение к базе данных не удалось')
            print(ex)

    def findButtonClicked(self):
        find_d = FindDialog(self)
        find_d.exec()

    def connectDB(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password='****',
                database='pyqt6',
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as ex:
            print('Connection failed')
            print(ex)

    def closeDB(self):
        if self.connection != None:
            self.connection.close()

    def closeEvent(self, event):
        self.closeDB()
        sys.exit()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
