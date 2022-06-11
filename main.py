from PyQt6.QtWidgets import QApplication, QDialog, QMainWindow, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt6.QtGui import QAction
from main_window import Ui_MainWindow
from login_dialog import Ui_LoginDialog
from find_dialog import Ui_FindDialog
from add_dialog import Ui_AddDialog
from delete_dialog import Ui_DeleteDialog
from sub_dialog import Ui_SubDialog
from reg_dialog import Ui_RegDialog
import mysql.connector

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


# pyuic6 -x reg_dialog.ui -o reg_dialog.py

class RegDialog(QDialog, Ui_RegDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.regButton.clicked.connect(self.regButtonClicked)


    def regButtonClicked(self):
        # TODO зарегистрировать пользователя
        #self.loginEdit.text # логин
        # self.passEdit
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
        # TODO SQL найти пользователя по логину и паролю и определить админ это или пользователь
        try:
            if True:  # Проверка, что пользователь есть в базе
                self.is_found = True
                if False:  # Проверка, что пользователь это админ
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
        # TODO Добавить фильм
        if self.check_fields():
            try:
                pass #ЗАПРОС ТУТ
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
                #Нйти, если нашел то удалить и вернуть флаг true, иначе false
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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.buyButton.clicked.connect(self.buyButtonClicked)
        self.buyButton_2.clicked.connect(self.buyButtonClicked)
        self.buyButton_3.clicked.connect(self.buyButtonClicked)

    def buyButtonClicked(self):
        QMessageBox.information(self, 'Подписка', 'Поздравляем! Вы ТИПО приобрели подписку :)')




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
        self.likeButton.hide()

        self.in_Account = True
        self.sub_enabled = False

        self.loadButton.clicked.connect(self.loadDB)  # Загрузить
        self.loginButton.clicked.connect(self.loginButtonClicked)  # Войти
        self.findButton.clicked.connect(self.findButtonClicked)  # Найти
        self.addButton.clicked.connect(self.addButtonClicked)  # Добавить
        self.delButton.clicked.connect(self.delButtonClicked)  # Удалить

        self.subButton.clicked.connect(self.subButtonClicked)  # Подписка
        self.outButton.clicked.connect(self.outButtonClicked)  # Выйти
        self.likeButton.clicked.connect(self.likeButtonClicked)  # Избранное

    def loginButtonClicked(self):
        log_d = LoginDialog(self)
        log_d.exec()
        login = log_d.loginEdit.text()
        password = log_d.passEdit.text()
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
        #TODO поиск 
        name = find_d.findEdit.text # это то что в строке

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
        #ТУТ ПИСАТЬ ЕСТЬ ЛИ ПОДПИСКА         
        sub_d = SubDialog(self)
        sub_d.exec()        

    def likeButtonClicked(self):
        pass
        #TODO вывести избранное

    def loadDB(self):

        try:
            with self.connection.cursor() as cur:
                # TODO Нужен нормальный запрос на фильмы
                get_data_query = 'SELECT * FROM film'
                i = 0
                cur.execute(get_data_query)
                self.tableWidget.setRowCount(self.rowCount)
                for row in cur.fetchall():
                    # сюда вставлять столбцы
                    self.tableWidget.setItem(i, 0, QTableWidgetItem(str(row[1])))  # title
                    self.tableWidget.setItem(i, 1, QTableWidgetItem(str(row[2])))  # year
                    self.tableWidget.setItem(i, 5, QTableWidgetItem(str(row[3])))  # rating
                    i += 1
                # self.connection.commit()
                self.tableWidget.setColumnWidth(0, 275)  # name
                self.tableWidget.setColumnWidth(1, 5)  # year
                self.tableWidget.setColumnWidth(2, 133)  # country
                self.tableWidget.setColumnWidth(3, 133)  # genre
                self.tableWidget.setColumnWidth(4, 133)  # director
                self.tableWidget.setColumnWidth(5, 10)  # rate


        except Exception as ex:
            QMessageBox.information(self, 'Ошибка', 'Подключение к базе данных не удалось')
            print(ex)

    def connectDB(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="password",
                database="filmoteka"
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
        self.likeButton.hide()
        self.loginButton.show()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
