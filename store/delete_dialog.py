# Form implementation generated from reading ui file 'delete_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DeleteDialog(object):
    def setupUi(self, DeleteDialog):
        DeleteDialog.setObjectName("DeleteDialog")
        DeleteDialog.resize(400, 196)
        DeleteDialog.setMinimumSize(QtCore.QSize(400, 196))
        DeleteDialog.setMaximumSize(QtCore.QSize(400, 196))
        DeleteDialog.setStyleSheet("")
        self.widget = QtWidgets.QWidget(DeleteDialog)
        self.widget.setGeometry(QtCore.QRect(0, 0, 400, 196))
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
"QLineEdit{\n"
"    border-radius: 15px;\n"
"    font-family: roboto;\n"
"    font-size: 20px;\n"
"}\n"
"\n"
"")
        self.widget.setObjectName("widget")
        self.deleteEdit = QtWidgets.QLineEdit(self.widget)
        self.deleteEdit.setGeometry(QtCore.QRect(10, 50, 381, 41))
        font = QtGui.QFont()
        font.setFamily("roboto")
        font.setPointSize(-1)
        self.deleteEdit.setFont(font)
        self.deleteEdit.setObjectName("deleteEdit")
        self.deleteButton = QtWidgets.QPushButton(self.widget)
        self.deleteButton.setGeometry(QtCore.QRect(110, 130, 181, 41))
        self.deleteButton.setObjectName("deleteButton")

        self.retranslateUi(DeleteDialog)
        QtCore.QMetaObject.connectSlotsByName(DeleteDialog)

    def retranslateUi(self, DeleteDialog):
        _translate = QtCore.QCoreApplication.translate
        DeleteDialog.setWindowTitle(_translate("DeleteDialog", "Dialog"))
        self.deleteEdit.setPlaceholderText(_translate("DeleteDialog", "Название"))
        self.deleteButton.setText(_translate("DeleteDialog", "Удалить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DeleteDialog = QtWidgets.QDialog()
    ui = Ui_DeleteDialog()
    ui.setupUi(DeleteDialog)
    DeleteDialog.show()
    sys.exit(app.exec())
