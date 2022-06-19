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
from favourite_dialog import Ui_FavouriteDialog


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


# pyuic6 -x favourite_dialog.ui -o favourite_dialog.py

class FavouriteDialog(QDialog, Ui_FavouriteDialog):
    def __init__(self, parent=None, login=''):
        super().__init__(parent)
        self.setupUi(self)
        self.login = login
        self.addButton.clicked.connect(self.addButtonClicked)
        self.showButton.clicked.connect(self.showButtonClicked)

    def addButtonClicked(self):
        try:
            if self.favouriteEdit.text() != '':
                if database.findFilm(int(self.favouriteEdit.text())):
                    database.addFavourites(self.login, int(self.favouriteEdit.text()))
                    QMessageBox.information(self, 'Информация', 'Фильм успешно добавлен в избранное')
                else:
                    QMessageBox.information(self, 'Ошибка', 'Id не найден!')                
                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Заполните корректно поля')

        except Exception as ex:
            QMessageBox.warning(self, 'Ошибка', 'Заполните корректно поля')

    def showButtonClicked(self):
        # TODO сделать запрос показать избранные фильмы
        self.close()


# pyuic6 -x reg_dialog.ui -o reg_dialog.py

class RegDialog(QDialog, Ui_RegDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.regButton.clicked.connect(self.regButtonClicked)

    def regButtonClicked(self):
        login = self.loginEdit.text()
        password = self.passEdit.text()
        isUserAdded = database.addUser(login, password)
        if not isUserAdded:
            QMessageBox.warning(self, 'Ошибка', 'Этот логин занят!')
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

        self.login = ''
        self.password = ''

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
            self.login = self.loginEdit.text()
            self.password = self.passEdit.text()
            if self.login == 'admin' and self.password == 'admin':
                self.is_admin = True
                self.is_found = True
            elif database.findUser(self.login, self.password):
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
        if self.check_fields():
            try:
                title = self.nameEdit.text()
                year = int(self.yearEdit.text())
                countries = self.countryEdit.text().split(', ')
                categories = self.genreEdit.text().split(', ')
                directors = self.directorEdit.text().split(', ')
                rate = float(self.ratingEdit.text())
                database.addFilm(title, year, rate, countries, categories, directors)
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
                filmId = self.deleteEdit.text()
                self.is_deleted = database.deleteFilm(filmId)
                # TODO: добавить форму "Фильм удалён" (сделал)
                QMessageBox.information(self, 'Информация', 'Фильм удален')
            except Exception as ex:
                QMessageBox.warning(self, 'Ошибка', 'Запись не найдена')
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
        # TODO дать подпиську
        QMessageBox.information(self, 'Подписка', 'Поздравляем! Вы ТИПО приобрели подписку :)')
        self.close()


# pyuic6 -x main_window.ui -o main_window.py

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.addButton.hide()
        self.delButton.hide()
        self.tableWidget.setColumnWidth(0, 5)  # rate
        self.tableWidget.setColumnWidth(1, 128)  # name
        self.tableWidget.setColumnWidth(2, 120)  # year
        self.tableWidget.setColumnWidth(3, 133)  # country
        self.tableWidget.setColumnWidth(4, 133)  # genre
        self.tableWidget.setColumnWidth(5, 133)  # director
        self.tableWidget.setColumnWidth(6, 112)  # rate
        self.tableWidget.verticalHeader().setVisible(False)

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

        if log_d.is_found:

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
        target = find_d.findEdit.text()

        if target != '':
            try:
                films = database.findAny(target)

                if (len(films) == 0):
                    QMessageBox.information(self, 'Поиск', 'По вашему запросу ничего не найдено')
                    return

                self.tableWidget.setRowCount(len(films))
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

                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))  # id
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(row[1]))  # title
                    self.tableWidget.setItem(i, 2, QTableWidgetItem(str(row[2])))  # year
                    self.tableWidget.setItem(i, 3, QTableWidgetItem(counries[:-2]))  # countries
                    self.tableWidget.setItem(i, 4, QTableWidgetItem(genres[:-2]))  # genres
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(directors[:-2]))  # directors
                    self.tableWidget.setItem(i, 6, QTableWidgetItem(str(row[3])))  # rate
                    i += 1

                    self.tableWidget.setColumnWidth(0, 5)  # id
                    self.tableWidget.setColumnWidth(1, 250)  # title
                    self.tableWidget.setColumnWidth(2, 5)  # year
                    self.tableWidget.setColumnWidth(3, 130)  # countries
                    self.tableWidget.setColumnWidth(4, 154)  # genres
                    self.tableWidget.setColumnWidth(5, 130)  # directors
                    self.tableWidget.setColumnWidth(6, 5)  # rate

            except Exception as ex:
                QMessageBox.information(self, 'Ошибка', 'Всё сломалось!')
                print(ex)

    def addButtonClicked(self):
        add_d = AddDialog(self)
        add_d.exec()
        if add_d.is_added:
            self.loadDB()

    def delButtonClicked(self):
        del_d = DeleteDialog(self)
        del_d.exec()
        if del_d.is_deleted:
            self.loadDB()

    def subButtonClicked(self):
        # TODO сколько осталось до истечения
        isSubscriber = database.isSubscriber(self.login)
        sub_d = SubDialog(login=self.login, password=self.password, parent=self)
        if isSubscriber:
            sub_d.status_label.setText('Статус: активна')
        else:
            sub_d.status_label.setText('Статус: не активна')
        sub_d.exec()

    def likeButtonClicked(self):        
        favourite_d = FavouriteDialog(parent=self, login=self.login)
        favourite_d.exec()

    def loadDB(self):
        try:
            films = database.getAllFilms()
            self.tableWidget.setRowCount(len(films))
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

                self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[0])))  # id
                self.tableWidget.setItem(i, 1, QTableWidgetItem(row[1]))  # title
                self.tableWidget.setItem(i, 2, QTableWidgetItem(str(row[2])))  # year
                self.tableWidget.setItem(i, 3, QTableWidgetItem(counries[:-2]))  # countries
                self.tableWidget.setItem(i, 4, QTableWidgetItem(genres[:-2]))  # genres
                self.tableWidget.setItem(i, 5, QTableWidgetItem(directors[:-2]))  # directors
                self.tableWidget.setItem(i, 6, QTableWidgetItem(str(row[3])))  # rate
                i += 1

            self.tableWidget.setColumnWidth(0, 5)  # id
            self.tableWidget.setColumnWidth(1, 250)  # title
            self.tableWidget.setColumnWidth(2, 5)  # year
            self.tableWidget.setColumnWidth(3, 130)  # countries
            self.tableWidget.setColumnWidth(4, 154)  # genres
            self.tableWidget.setColumnWidth(5, 130)  # directors
            self.tableWidget.setColumnWidth(6, 5)  # rate

        except Exception as ex:
            QMessageBox.information(self, 'Ошибка', 'Всё сломалось!')
            print(ex)

    def closeEvent(self, event):
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

    database = Database()
    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
