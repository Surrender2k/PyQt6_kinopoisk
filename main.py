from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt6.QtGui import QAction
from main_window import Ui_MainWindow
from login_dialog import Ui_LoginDialog
from find_dialog import Ui_FindDialog
from add_dialog import Ui_AddDialog
from delete_dialog import Ui_DeleteDialog

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
        self.is_correct_fields = False

    def logButtonClicked(self):
        if self.check_fields():
            self.is_correct_fields = True
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
        self.is_added = False

    def addButtonClicked(self):
        # TODO
        if self.check_fields():
            try:
                pass
                self.is_added = True
            except Exception as ex:
                pass
            finally:
                self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните корректно поля')

    def check_fields(self):
        return not (self.nameEdit.text() == '' or self.yearEdit.text() == '' or self.countryEdit.text() == ''
                    or self.genreEdit.text() == '' or self.directorEdit.text() == '' or self.ratingEdit.text() == '')


# pyuic6 -x delete_dialog.ui -o delete_dialog.py
class DeleteDialog(QDialog, Ui_DeleteDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.deleteButton.clicked.connect(self.deleteButtonClicked)
        self.is_deleted = False

    def deleteButtonClicked(self):
        if self.check_fields():
            try:
                # TODO sql
                self.is_deleted = True
                pass
            except Exception as ex:
                QMessageBox.warning(self, 'Ошибка', 'Фильм не найден')
            finally:
                self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните корректно поля')

    def check_fields(self):
        return not (self.deleteEdit.text() == '')

    # TODO sql command
    def find(self):
        name = self.deleteEdit.text()
        pass


# TODO Написать  функции перехвата сигнала

# pyuic6 -x main_window.ui -o main_window.py

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.rowCount = 995
        self.addButton.hide()
        self.delButton.hide()
        self.connection = None
        self.connectDB()
        self.tableWidget.setColumnWidth(0, 133)  # name
        self.tableWidget.setColumnWidth(1, 133)  # year
        self.tableWidget.setColumnWidth(2, 133)  # country
        self.tableWidget.setColumnWidth(3, 133)  # genre
        self.tableWidget.setColumnWidth(4, 133)  # director
        self.tableWidget.setColumnWidth(5, 133)  # rate

        self.loadButton.clicked.connect(self.loadDB)  # Загрузить
        self.loginButton.clicked.connect(self.loginButtonClicked)  # Войти
        self.findButton.clicked.connect(self.findButtonClicked)  # Найти
        self.addButton.clicked.connect(self.addButtonClicked)  # Добавить
        self.delButton.clicked.connect(self.delButtonClicked) # Удалить

    def loginButtonClicked(self):
        log_d = LoginDialog(self)
        res = log_d.exec()
        login = log_d.loginEdit.text()
        password = log_d.passEdit.text()
        admin = True
        if log_d.is_correct_fields:
            # TODO sql query and check if admin
            if admin:
                self.addButton.show()
                self.delButton.show()

    def findButtonClicked(self):
        find_d = FindDialog(self)
        find_d.exec()

    def addButtonClicked(self):
        add_d = AddDialog(self)
        add_d.exec()
        if add_d.is_added:
            self.loadDB()

    def delButtonClicked(self):
        del_d = DeleteDialog()
        del_d.exec()
        if del_d.is_found:
            # TODO
            self.loadDB()

    def loadDB(self):
        # TODO
        self.tableWidget.setColumnWidth(0, 275)  # name
        self.tableWidget.setColumnWidth(1, 5)  # year
        self.tableWidget.setColumnWidth(2, 133)  # country
        self.tableWidget.setColumnWidth(3, 133)  # genre
        self.tableWidget.setColumnWidth(4, 133)  # director
        self.tableWidget.setColumnWidth(5, 10)  # rate

        try:
            with self.connection.cursor() as cur:
                get_data_query = 'SELECT * FROM film'
                i = 0
                cur.execute(get_data_query)
                self.tableWidget.setRowCount(self.rowCount)
                for row in cur.fetchall():
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[3])))  # name
                    i += 1
                # self.connection.commit()
        except Exception as ex:
            QMessageBox.information(self, 'Ошибка', 'Подключение к базе данных не удалось')
            print(ex)

    def connectDB(self):
        try:
            self.connection = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password='****!',
                database='filmoteka'
            )
        except Exception as ex:
            print('Connection failed')
            print(ex)

    def closeDB(self):
        if self.connection is not None:
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
