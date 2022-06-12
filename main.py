from dataclasses import dataclass
from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt6.QtGui import QAction
from database import Database
from main_window import Ui_MainWindow
from login_dialog import Ui_LoginDialog
from find_dialog import Ui_FindDialog
from add_dialog import Ui_AddDialog
from delete_dialog import Ui_DeleteDialog
from sub_dialog import Ui_SubDialog
from reg_dialog import Ui_RegDialog

# pyuic6 -x find_dialog.ui -o find_dialog.py

database = Database()

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


# pyuic6 -x reg_dialog.ui -o reg_dialog.py

class RegDialog(QDialog, Ui_RegDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.regButton.clicked.connect(self.regButtonClicked)

    def regButtonClicked(self):
        login = self.loginEdit.text()
        password = self.passEdit.text()             
        database.addUser(login, password)        
        self.close()

# pyuic6 -x login_dialog.ui -o login_dialog.py

class LoginDialog(QDialog, Ui_LoginDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.logButton.clicked.connect(self.logButtonClicked)
        self.regButton.clicked.connect(self.regButtonClicked)
        self.is_found = False
        self.is_admin = False        

    def regButtonClicked(self):
        reg_d = RegDialog()
        reg_d.exec()

    def logButtonClicked(self):
        if self.check_fields():
            self.find()
            self.close()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Заполните корректно поля')

    def check_fields(self):
        return not (self.loginEdit.text() == '' or self.passEdit.text() == '')

    def find(self):        
        try:
            login = self.loginEdit.text()
            password = self.passEdit.text()
            if login == 'admin' and password == 'admin':
                self.is_admin = True
            elif database.findUser(login, password):                
                self.is_found = True
            else: 
                QMessageBox.warning(self, 'Ошибка', 'Не верный логин или пароль')

        except Exception as ex:
            QMessageBox.warning(self, 'Ошибка', 'Всё сломалось')


# pyuic6 -x add_dialog.ui -o add_dialog.py

class AddDialog(QDialog, Ui_AddDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.addButton.clicked.connect(self.addButtonClicked)
        self.is_added = False

    def addButtonClicked(self):
        # TODO Добавить фильм
        if self.check_fields():
            try:
                pass  # ЗАПРОС ТУТ
                self.is_added = True
            except Exception as ex:
                QMessageBox.warning(self, 'Ошибка', f'{ex}')
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
                # TODO Удалить фильм
                # Нйти, если нашел то удалить и вернуть флаг true, иначе false
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


# pyuic6 -x sub_dialog.ui -o sub_dialog.py
class SubDialog(QDialog, Ui_SubDialog):
    def __init__(self, login, password, parent=None):
        super().__init__(parent)
        self.login = login
        self.password = password
        self.setupUi(self)
        self.buyButton.clicked.connect(self.buyButtonClicked)
        self.buyButton_2.clicked.connect(self.buyButtonClicked)
        self.buyButton_3.clicked.connect(self.buyButtonClicked)
        self.hasSubscribtion = False

    def buyButtonClicked(self):
        self.hasSubscribtion = True
        QMessageBox.information(self, 'Подписка', 'Поздравляем! Вы ТИПО приобрели подписку :)')


# pyuic6 -x main_window.ui -o main_window.py

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.rowCount = 995  # ???
        self.addButton.hide()
        self.delButton.hide()               
        self.tableWidget.setColumnWidth(0, 133)  # name
        self.tableWidget.setColumnWidth(1, 133)  # year
        self.tableWidget.setColumnWidth(2, 133)  # country
        self.tableWidget.setColumnWidth(3, 133)  # genre
        self.tableWidget.setColumnWidth(4, 133)  # director
        self.tableWidget.setColumnWidth(5, 133)  # rate

        self.subButton.hide()
        self.outButton.hide()
        self.likeButton.hide()

        self.in_Account = True

        self.loadButton.clicked.connect(self.loadDB)  # Загрузить
        self.loginButton.clicked.connect(self.loginButtonClicked)  # Войти
        self.findButton.clicked.connect(self.findButtonClicked)  # Найти
        self.addButton.clicked.connect(self.addButtonClicked)  # Добавить
        self.delButton.clicked.connect(self.delButtonClicked)  # Удалить

        self.subButton.clicked.connect(self.subButtonClicked)  # Подписка
        self.outButton.clicked.connect(self.outButtonClicked)  # Выйти
        self.likeButton.clicked.connect(self.likeButtonClicked)  # Избранное

        self.login = ''
        self.password = ''

    def loginButtonClicked(self):
        log_d = LoginDialog(self)
        log_d.exec()
        self.login = log_d.loginEdit.text()
        self.password = log_d.passEdit.text()
        admin = False
        if log_d.is_found:
            # скип говно # TODO Узнать пользователь или админ
            if log_d.is_admin:
                self.addButton.show()
                self.delButton.show()
            else:
                self.subButton.show()
                self.likeButton.show()
            self.loginButton.hide()
            self.outButton.show()

    def findButtonClicked(self):
        find_d = FindDialog(self)
        find_d.exec()
        # TODO поиск
        name = find_d.findEdit.text  # это то что в строке

    def addButtonClicked(self):
        add_d = AddDialog(self)
        add_d.exec()
        if add_d.is_added:
            self.rowCount += 1
            self.loadDB()

    def delButtonClicked(self):
        del_d = DeleteDialog(self)
        del_d.exec()
        if del_d.is_deleted:
            self.rowCount -= 1
            self.loadDB()

    # TODO Узнать о подписке пользователя
    def subButtonClicked(self):
        # ТУТ ПИСАТЬ ЕСТЬ ЛИ ПОДПИСКА
        sub_d = SubDialog(login=self.login, password=self.password, parent=self)
        sub_d.exec()

    def likeButtonClicked(self):
        pass
        # TODO вывести избранное

    def loadDB(self):
        try:
            films = database.getAllFilms()
            self.tableWidget.setRowCount(self.rowCount)
            i = 0
            for row in films:

                counries = ''
                for cur in database.getFilmCountries(row[0]):
                    counries += cur[0] + ', '

                genres = ''
                for cur in database.getFilmCategories(row[0]):
                    genres += cur[0] + ', '

                directors = ''
                for cur in database.getFilmDirectors(row[0]):
                    directors += cur[0] + ', '

                self.tableWidget.setItem(i, 0, QTableWidgetItem(row[1]))  # title
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(row[2])))  # year
                self.tableWidget.setItem(i, 2, QTableWidgetItem(counries[:-2]))  # countries
                self.tableWidget.setItem(i, 3, QTableWidgetItem(genres[:-2]))  # genres
                self.tableWidget.setItem(i, 4, QTableWidgetItem(directors[:-2]))  # directors
                self.tableWidget.setItem(i, 5, QTableWidgetItem(str(row[3])))  # rate
                i += 1
            
            self.tableWidget.setColumnWidth(0, 275)  # title
            self.tableWidget.setColumnWidth(1, 5)  # year
            self.tableWidget.setColumnWidth(2, 133)  # countries
            self.tableWidget.setColumnWidth(3, 133)  # genres
            self.tableWidget.setColumnWidth(4, 133)  # directors
            self.tableWidget.setColumnWidth(5, 10)  # rate

        except Exception as ex:
            QMessageBox.information(self, 'Ошибка', 'Подключение к базе данных не удалось')
            print(ex)

    # def connectDB(self):
    #     try:
    #         self.connection = mysql.connector.connect(
    #             host="localhost",
    #             user="root",
    #             passwd="password",
    #             database="filmoteka"
    #         )
    #     except Exception as ex:
    #         print('Connection failed')
    #         print(ex)

    # это нельзя комментить!!!
    def closeEvent(self, event):
        if self.database is not None:
            self.database.close()
        sys.exit()

    def outButtonClicked(self):
        self.addButton.hide()
        self.delButton.hide()
        self.outButton.hide()
        self.subButton.hide()
        self.likeButton.hide()
        self.loginButton.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
