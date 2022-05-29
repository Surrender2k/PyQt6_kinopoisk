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
        self.is_found = False
        self.is_admin = False

    def logButtonClicked(self):
        if self.check_fields():
            self.find()
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните корректно поля')

    def check_fields(self):
        return not (self.loginEdit.text() == '' or self.passEdit.text() == '')

    def find(self):
        # TODO SQL найти пользователя по логину и паролю и определить админ это или пользователь
        try:
            if True:  # Проверка, что пользователь есть в базе
                self.is_found = True
                if True:  # Проверка, что пользователь это админ
                    self.is_admin = True
        except Exception as ex:
            QMessageBox.warning(self, 'Ошибка', 'Пользователь не найден')


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
        self.subButton.hide()
        self.outButton.hide()
        self.in_Account = True
        self.sub_enabled = False

        self.loadButton.clicked.connect(self.loadDB)  # Загрузить
        self.loginButton.clicked.connect(self.loginButtonClicked)  # Войти
        self.findButton.clicked.connect(self.findButtonClicked)  # Найти
        self.addButton.clicked.connect(self.addButtonClicked)  # Добавить
        self.delButton.clicked.connect(self.delButtonClicked)  # Удалить

        self.subButton.clicked.connect(self.subButtonClicked)  # Подписка
        self.outButton.clicked.connect(self.outButtonClicked)  # Выйти

    def loginButtonClicked(self):
        log_d = LoginDialog(self)
        log_d.exec()
        login = log_d.loginEdit.text()
        password = log_d.passEdit.text()
        admin = True
        if log_d.is_found:
            if log_d.is_admin:
                self.addButton.show()
                self.delButton.show()
            else:
                # TODO
                self.subButton.show()
            self.loginButton.hide()
            self.outButton.show()

    def findButtonClicked(self):
        find_d = FindDialog(self)
        find_d.exec()

    def addButtonClicked(self):
        add_d = AddDialog(self)
        add_d.exec()
        if add_d.is_added:
            self.loadDB()

    def delButtonClicked(self):
        del_d = DeleteDialog(self)
        del_d.exec()
        if del_d.is_deleted:
            # TODO
            self.loadDB()

    def subButtonClicked(self):
        pass

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

    def closeEvent(self, event):
        if self.connection is not None:
            self.connection.close()
        sys.exit()

    def outButtonClicked(self):
        self.addButton.hide()
        self.delButton.hide()
        self.outButton.hide()
        self.subButton.hide()
        self.loginButton.show()

    # def toggle_add_sub_button(self):
    #     if not self.sub_enabled:
    #         self.addButton.hide()
    #         self.subButton.show()
    #         self.sub_enabled = True
    #     else:
    #         self.subButton.hide()
    #         self.addButton.show()
    #         self.sub_enabled = False


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
