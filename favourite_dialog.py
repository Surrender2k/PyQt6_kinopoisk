# Form implementation generated from reading ui file 'favourite_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_FavouriteDialog(object):
    def setupUi(self, FavouriteDialog):
        FavouriteDialog.setObjectName("FavouriteDialog")
        FavouriteDialog.resize(332, 160)
        FavouriteDialog.setMinimumSize(QtCore.QSize(332, 160))
        FavouriteDialog.setMaximumSize(QtCore.QSize(332, 160))
        FavouriteDialog.setStyleSheet("")
        self.widget = QtWidgets.QWidget(FavouriteDialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 332, 160))
        self.widget.setMinimumSize(QtCore.QSize(332, 160))
        self.widget.setMaximumSize(QtCore.QSize(332, 160))
        self.widget.setStyleSheet("QWidget#widget{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 72, 72, 255), stop:1 rgba(136, 129, 255, 255));\n"
"}\n"
"\n"
"QPushButton{\n"
"    \n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 140, 0, 255), stop:1 rgba(0, 212, 255, 255));\n"
"    border: 2px solid #85efff;\n"
"    border-radius: 15px;    \n"
"    color: rgb(255, 255, 255);\n"
"    font-family: roboto;\n"
"    font-size: 16px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(0, 255, 115, 255), stop:1 rgba(184, 255, 73, 255));\n"
"    border: 2px solid #90ff94;\n"
"}\n"
"\n"
"QLabel{\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QLineEdit{\n"
"    border-radius: 15px;\n"
"    font-family: roboto;\n"
"    font-size: 20px;\n"
"}\n"
"")
        self.widget.setObjectName("widget")
        self.favouriteEdit = QtWidgets.QLineEdit(self.widget)
        self.favouriteEdit.setGeometry(QtCore.QRect(10, 30, 311, 41))
        font = QtGui.QFont()
        font.setFamily("roboto")
        font.setPointSize(-1)
        self.favouriteEdit.setFont(font)
        self.favouriteEdit.setCursorPosition(0)
        self.favouriteEdit.setDragEnabled(False)
        self.favouriteEdit.setObjectName("favouriteEdit")
        self.addButton = QtWidgets.QPushButton(self.widget)
        self.addButton.setGeometry(QtCore.QRect(10, 100, 141, 41))
        self.addButton.setObjectName("addButton")
        self.showButton = QtWidgets.QPushButton(self.widget)
        self.showButton.setGeometry(QtCore.QRect(180, 100, 141, 41))
        self.showButton.setObjectName("showButton")

        self.retranslateUi(FavouriteDialog)
        QtCore.QMetaObject.connectSlotsByName(FavouriteDialog)

    def retranslateUi(self, FavouriteDialog):
        _translate = QtCore.QCoreApplication.translate
        FavouriteDialog.setWindowTitle(_translate("FavouriteDialog", "Dialog"))
        self.favouriteEdit.setPlaceholderText(_translate("FavouriteDialog", "ID"))
        self.addButton.setText(_translate("FavouriteDialog", "Добавить"))
        self.showButton.setText(_translate("FavouriteDialog", "Показать"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FavouriteDialog = QtWidgets.QDialog()
    ui = Ui_FavouriteDialog()
    ui.setupUi(FavouriteDialog)
    FavouriteDialog.show()
    sys.exit(app.exec())