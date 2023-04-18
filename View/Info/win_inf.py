# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'win_info.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_3 = QtWidgets.QSplitter(Form)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.lable_yellow_2 = QtWidgets.QLabel(self.splitter_3)
        self.lable_yellow_2.setStyleSheet("")
        self.lable_yellow_2.setText("")
        self.lable_yellow_2.setPixmap(QtGui.QPixmap("./Image/green.png"))
        self.lable_yellow_2.setObjectName("lable_yellow_2")
        self.lable_yellow_info_2 = QtWidgets.QLabel(self.splitter_3)
        self.lable_yellow_info_2.setWordWrap(True)
        self.lable_yellow_info_2.setObjectName("lable_yellow_info_2")
        self.verticalLayout.addWidget(self.splitter_3)
        self.splitter_2 = QtWidgets.QSplitter(Form)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.lable_yellow = QtWidgets.QLabel(self.splitter_2)
        self.lable_yellow.setStyleSheet("")
        self.lable_yellow.setText("")
        self.lable_yellow.setPixmap(QtGui.QPixmap("./Image/yellow.png"))
        self.lable_yellow.setObjectName("lable_yellow")
        self.lable_yellow_info = QtWidgets.QLabel(self.splitter_2)
        self.lable_yellow_info.setWordWrap(True)
        self.lable_yellow_info.setObjectName("lable_yellow_info")
        self.verticalLayout.addWidget(self.splitter_2)
        self.splitter = QtWidgets.QSplitter(Form)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.lable_red = QtWidgets.QLabel(self.splitter)
        self.lable_red.setStyleSheet("")
        self.lable_red.setText("")
        self.lable_red.setPixmap(QtGui.QPixmap("./Image/red.png"))
        self.lable_red.setObjectName("lable_red")
        self.label_red_info = QtWidgets.QLabel(self.splitter)
        self.label_red_info.setWordWrap(True)
        self.label_red_info.setObjectName("label_red_info")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Справка"))
        self.lable_yellow_info_2.setText(_translate("Form", "В имени файла содержится слово, включенное в список слов к поиску запрещенной информации (паспорт, снилс, карта, дата рождения)."))
        self.lable_yellow_info.setText(_translate("Form", "В документе содержится слово, включенное в список слов к поиску запрещенной информации (паспорт, снилс, карта, дата рождения)."))
        self.label_red_info.setText(_translate("Form", "В документе содержится информация, совпадающая с номером паспорта или номером СНИЛС (XXXX XXXXXX, XXX-XXX-XXX XX)"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
