import os
import pathlib
import sys
import threading
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QDialog, QMessageBox

import wmi

from View.MainView.Scan import Ui_MainWindow
from scaner_files.scaner_file import scaner_file

from search_bad_word import seach_word
from View.Info.win_inf import Ui_Form
from View.Setting.win_setting import Ui_Dialog


class window(QtWidgets.QMainWindow):
    list_bad_word = ['снилс', 'карта', 'паспорт', 'дата рождения', 'доверенность', 'пароль']
    path_search = []

    def __init__(self, parament=None):

        def open_file():
            '''Открываем файл'''
            file = self.ui.listWidget.currentItem().text()
            os.system('"' + file + '"')

        super(window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start_scan)

        self.ui.listWidget.itemDoubleClicked.connect(open_file)

        self.ui.listWidget.installEventFilter(self)

        self.menuInfo = MenuInfo(self)
        self.ui.action_3.triggered.connect(self.menuInfo.show)

        self.menuSetting = Menu_setting(self)
        self.ui.action_4.triggered.connect(self.open_settting)

        self.menuSetting.ui.btn_save.clicked.connect(self.save_list_bad_word)

        self.get_local_disk()

    def save_list_bad_word(self):
        self.list_bad_word = (self.menuSetting.ui.plainTextEdit.toPlainText()).split(',')
        self.path_search = (self.menuSetting.ui.lineEdit_path.text().split(','))
        # print(self.menuSetting.ui.chB_fileName.isChecked())
        self.menuSetting.close()

    def open_settting(self):
        self.menuSetting.ui.plainTextEdit.setPlainText(','.join(self.list_bad_word))
        self.menuSetting.ui.lineEdit_path.setText(','.join(self.path_search))
        self.menuSetting.exec_()

    def eventFilter(self, source, event):
        '''Событие контекстное меню'''

        def showDialog():
            '''Подтверждение удаления'''
            ret = QMessageBox.question(self, 'Предупреждение', "Вы действительно хотите удалить выбранный файл?",
                                       QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if ret == QMessageBox.Ok:
                if os.path.isfile(self.ui.listWidget.currentItem().text()):
                    os.remove(self.ui.listWidget.currentItem().text())
                    self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())
                    QMessageBox.information(self, 'Уведомление', "Файл удален!", QMessageBox.Ok)

        if (event.type() == QtCore.QEvent.ContextMenu and
                source is self.ui.listWidget):
            menu = QtWidgets.QMenu()
            menu.addAction('Удалить')
            if menu.exec_(event.globalPos()):
                showDialog()
            return True
        return super(window, self).eventFilter(source, event)

    def add_item(self, rezylt, path_file):
        if rezylt == 'regulyar':
            self.ui.listWidget.addItem(QListWidgetItem(QIcon("Image/red.png"), path_file))
        elif rezylt == 'word':
            self.ui.listWidget.addItem(QListWidgetItem(QIcon("Image/yellow.png"), path_file))
        elif rezylt == 'green':
            self.ui.listWidget.addItem(QListWidgetItem(QIcon("Image/green.png"), path_file))

    def start_scan(self):
        """Запус сканирования"""

        self.thread = Scan_fale_thread(self.list_bad_word, self.menuSetting.ui.chB_scanReg.isChecked(),
                                       self.path_search, self.menuSetting.ui.chB_fileName.isChecked())

        # Подключаем сигнал потока к методу add_bad_file
        self.thread.add_bad_file.connect(self.add_item)
        # Подключаем сигнал потока к методу enable_start_btn
        self.thread.enable_start_btn.connect(self.ui.pushButton.setEnabled)
        # Подключаем сигнал потока к методу current_file
        self.thread.current_file.connect(self.ui.statusbar.showMessage)

        self.ui.listWidget.clear()
        self.thread.start()
        self.ui.pushButton.setEnabled(False)

    def get_local_disk(self):
        '''Список локалбных дисков'''
        import pythoncom
        pythoncom.CoInitialize()
        c = wmi.WMI()
        disk_list = []
        for i in c.Win32_LogicalDisk(DriveType=3):
            disk_list.append(i.Caption + '\\')
        print(disk_list)
        self.path_search = disk_list
        return disk_list
        # return ["C:\Temp"]


class Scan_fale_thread(QtCore.QThread):

    def __init__(self, list_bad_word, check_regul, search_path, chek_filename):
        super().__init__()
        self.list_bad_word = list_bad_word
        self.check_regul = check_regul
        self.search_path = search_path
        self.chek_filename = chek_filename

    add_bad_file = QtCore.pyqtSignal(str, str)  # сигнал обновить интерфейс ListWidget
    enable_start_btn = QtCore.pyqtSignal(bool)  # сигнал обновить интерфейс button Start
    current_file = QtCore.pyqtSignal(str)  # сигнал обновить интерфейс statusBar
    total_files = QtCore.pyqtSignal(str)  # сигнал обновить интерфейс statusBar

    def run(self):
        list_rezult = []

        def print_rezult(rezylt, path_file):
            '''Вывод результатов'''
            self.add_bad_file.emit(rezylt[0], path_file)
            tmp = rezylt, path_file
            list_rezult.append(tmp)

        def enumerate_fale(dir, list_bad_word=None, check_regul=None, chek_filename=None):
            exclude = set(['Windows', 'Program Files', 'Program Files (x86)'])
            for adress, dirs, files in os.walk(dir, topdown=True):
                dirs[:] = [d for d in dirs if d not in exclude]
                for file in files:
                    path_curent_file = os.path.join(adress, file).replace('\\', os.path.sep)
                    self.current_file.emit(os.path.join(adress, path_curent_file))

                    suffix_file = pathlib.Path(path_curent_file).suffix

                    list_suffix_file = ['.docx', '.xlsx', '.xls', '.txt']
                    if suffix_file in list_suffix_file:

                        rezylt = scaner_file(path_curent_file, list_bad_word, check_regul)
                        if rezylt != None:
                            print_rezult(rezylt, path_curent_file)
                        else:
                            if chek_filename:
                                if seach_word(path_curent_file, list_bad_word):
                                    print_rezult(['green'], path_curent_file)

        for i in self.search_path:
            enumerate_fale(i, self.list_bad_word, self.check_regul, self.chek_filename)

        self.enable_start_btn.emit(True)


class MenuInfo(QtWidgets.QDialog):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.win = QDialog(self)
        self.ui = Ui_Form()
        self.ui.setupUi(self)


class Menu_setting(QtWidgets.QDialog):
    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.win = QDialog(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.btn_cancel.clicked.connect(self.close)


app = QtWidgets.QApplication([])
app.setWindowIcon((QtGui.QIcon('Image/all.ico')))
main = window()
main.show()
sys.exit(app.exec_())
