import sys
from datetime import datetime
from configparser import ConfigParser
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from PyQt5.QtWidgets import QMessageBox


class Ui_MainWindow(object):
    def __init__(self, MainWindow, config_file_path):
        self.MainWindow = MainWindow
        self.width = 874
        self.height = 520
        self.tableRow = 50
        self.tableColumn = 4
        self.file = config_file_path
        self.config = ConfigParser()
        self.csvPath = r'C:\Users\battlefrog\Desktop\test.csv'
        self.iconPath = r"Resources\sicon.png"

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.MainWindow.setWindowIcon(QtGui.QIcon(self.iconPath))
        MainWindow.resize(self.width, self.height)
        MainWindow.setMaximumWidth(self.width)
        MainWindow.setMaximumHeight(self.height)
        MainWindow.setMinimumSize(self.width, self.height)
        MainWindow.setStyleSheet("\n"
                                 "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(235, 148, 61, 100), stop:0.98 rgba(0, 0, 0, 255), stop:1 rgba(0, 0, 0, 0));\n"
                                 "\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 480, 61, 16))
        self.label_2.setStyleSheet("background-color: transparent;\n"
                                   "color: rgb(255, 255, 255);")
        self.label_2.setObjectName("label_2")
        self.groupBox_plc_config = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_plc_config.setGeometry(QtCore.QRect(40, 23, 301, 211))
        font = QtGui.QFont()
        font.setFamily("Tarif Arabic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_plc_config.setFont(font)
        self.groupBox_plc_config.setStyleSheet("color: rgb(255, 255, 255);\n"
                                               "background-color: rgba(194, 194, 194, 100);\n"
                                               "border-radius:15px")
        self.groupBox_plc_config.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_plc_config.setObjectName("groupBox_plc_config")
        self.lineEdit_test_intervals = QtWidgets.QLineEdit(self.groupBox_plc_config)
        self.lineEdit_test_intervals.setGeometry(QtCore.QRect(140, 140, 150, 20))
        self.lineEdit_test_intervals.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_test_intervals.setStyleSheet("color: rgb(0, 0, 0);")
        self.lineEdit_test_intervals.setObjectName("lineEdit_test_intervals")
        self.lineEdit_ip = QtWidgets.QLineEdit(self.groupBox_plc_config)
        self.lineEdit_ip.setGeometry(QtCore.QRect(140, 41, 150, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(50)
        self.lineEdit_ip.setFont(font)
        self.lineEdit_ip.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                       "border-radius:15px;\n"
                                       "color: rgb(0, 0, 0);")
        self.lineEdit_ip.setStyleSheet("color: rgb(0, 0, 0);")
        self.lineEdit_ip.setObjectName("lineEdit_ip")
        self.lineEdit_Port = QtWidgets.QLineEdit(self.groupBox_plc_config)
        self.lineEdit_Port.setGeometry(QtCore.QRect(140, 77, 150, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(50)
        self.lineEdit_Port.setFont(font)
        self.lineEdit_Port.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_Port.setStyleSheet("color: rgb(0, 0, 0);")
        self.lineEdit_Port.setMaxLength(32766)
        self.lineEdit_Port.setFrame(True)
        self.lineEdit_Port.setObjectName("lineEdit_Port")
        self.lineEdit_number_of_samples = QtWidgets.QLineEdit(self.groupBox_plc_config)
        self.lineEdit_number_of_samples.setGeometry(QtCore.QRect(140, 109, 150, 20))
        self.lineEdit_number_of_samples.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_number_of_samples.setStyleSheet("color: rgb(0, 0, 0);")
        self.lineEdit_number_of_samples.setObjectName("lineEdit_number_of_samples")
        self.label_ip = QtWidgets.QLabel(self.groupBox_plc_config)
        self.label_ip.setGeometry(QtCore.QRect(15, 41, 127, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ip.setFont(font)
        self.label_ip.setStyleSheet("background-color: transparent;\n"
                                    "")
        self.label_ip.setObjectName("label_ip")
        self.label_port = QtWidgets.QLabel(self.groupBox_plc_config)
        self.label_port.setGeometry(QtCore.QRect(14, 72, 127, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_port.setFont(font)
        self.label_port.setStyleSheet("background-color: transparent;\n"
                                      "")
        self.label_port.setObjectName("label_port")
        self.label_number_of_samples = QtWidgets.QLabel(self.groupBox_plc_config)
        self.label_number_of_samples.setGeometry(QtCore.QRect(14, 94, 127, 56))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_number_of_samples.setFont(font)
        self.label_number_of_samples.setStyleSheet("background-color: transparent;\n"
                                                   "")
        self.label_number_of_samples.setObjectName("label_number_of_samples")
        self.label_test_intervals = QtWidgets.QLabel(self.groupBox_plc_config)
        self.label_test_intervals.setGeometry(QtCore.QRect(10, 93, 127, 117))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_test_intervals.setFont(font)
        self.label_test_intervals.setStyleSheet("background-color: transparent;\n"
                                                "")
        self.label_test_intervals.setObjectName("label_test_intervals")
        self.pushButton_saveConfig = QtWidgets.QPushButton(self.groupBox_plc_config)
        self.pushButton_saveConfig.setGeometry(QtCore.QRect(90, 170, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_saveConfig.setFont(font)
        self.pushButton_saveConfig.setStyleSheet("background-color: rgb(41, 144, 255,200);\n"
                                                 "border-radius:10px;\n"
                                                 "border-color: rgb(255, 5, 5);\n"
                                                 "color: rgb(255, 255, 255);\n"
                                                 "")
        self.pushButton_saveConfig.setObjectName("pushButton_saveConfig")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(70, 270, 241, 171))
        font = QtGui.QFont()
        font.setFamily("Tarif Arabic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "background-color: rgba(194, 194, 194, 100);\n"
                                    "border-radius:15px")
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName("groupBox")
        self.pushButton_save_training_data = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_save_training_data.setGeometry(QtCore.QRect(60, 126, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_save_training_data.setFont(font)
        self.pushButton_save_training_data.setStyleSheet("background-color: rgb(41, 144, 255,200);\n"
                                                         "border-radius:10px;\n"
                                                         "border-color: rgb(255, 5, 5);\n"
                                                         "color: rgb(255, 255, 255);\n"
                                                         "")
        self.pushButton_save_training_data.setObjectName("pushButton_save_training_data")
        self.pushButton_load_Training_data = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_load_Training_data.setGeometry(QtCore.QRect(60, 86, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.pushButton_load_Training_data.setFont(font)
        self.pushButton_load_Training_data.setStyleSheet("background-color: rgb(41, 144, 255,200);\n"
                                                         "border-radius:10px;\n"
                                                         "border-color: rgb(255, 5, 5);\n"
                                                         "color: rgb(255, 255, 255);\n"
                                                         "")
        self.pushButton_load_Training_data.setObjectName("pushButton_load_Training_data")
        self.label_Csv_Path = QtWidgets.QLabel(self.groupBox)
        self.label_Csv_Path.setGeometry(QtCore.QRect(10, 50, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_Csv_Path.setFont(font)
        self.label_Csv_Path.setStyleSheet("background-color: transparent;\n"
                                          "")
        self.label_Csv_Path.setObjectName("label_Csv_Path")
        self.lineEdit_Csv_Path = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_Csv_Path.setGeometry(QtCore.QRect(81, 49, 151, 20))
        self.lineEdit_Csv_Path.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_Csv_Path.setStyleSheet("color: rgb(0, 0, 0);")
        self.lineEdit_Csv_Path.setText("")
        self.lineEdit_Csv_Path.setObjectName("lineEdit_Csv_Path")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(370, 20, 471, 471))
        font = QtGui.QFont()
        font.setFamily("Tarif Arabic")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                      "background-color: rgba(194, 194, 194, 100);\n"
                                      "border-radius:15px")
        self.groupBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.tableWidget = QtWidgets.QTableWidget(self.groupBox_2)
        self.tableWidget.setGeometry(QtCore.QRect(20, 30, 429, 391))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.tableWidget.setFont(font)
        self.tableWidget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                       "color: rgb(11, 11, 11);\n"
                                       "")
        self.tableWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidget.setLineWidth(2)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setRowCount(self.tableRow)
        self.tableWidget.setColumnCount(self.tableColumn)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)

        # load item structure
        for i in range(self.tableRow):
            for j in range(self.tableColumn):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, j, item)

        self.pushButton_Save_Table_Data = QtWidgets.QPushButton(self.groupBox_2)
        self.pushButton_Save_Table_Data.setGeometry(QtCore.QRect(170, 430, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.pushButton_Save_Table_Data.setFont(font)
        self.pushButton_Save_Table_Data.setStyleSheet("background-color: rgb(41, 144, 255,200);\n"
                                                      "border-radius:10px;\n"
                                                      "border-color: rgb(255, 5, 5);\n"
                                                      "color: rgb(255, 255, 255);\n"
                                                      "")
        self.pushButton_Save_Table_Data.setObjectName("pushButton_Save_Table_Data")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 884, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SalumaIU"))
        self.label_2.setText(_translate("MainWindow", "Version 1.0"))
        self.groupBox_plc_config.setTitle(_translate("MainWindow", "PLC Configuration"))
        self.label_ip.setText(_translate("MainWindow", "IP"))
        self.label_port.setText(_translate("MainWindow", "PORT"))
        self.label_number_of_samples.setText(_translate("MainWindow", "No./Of Samples"))
        self.label_test_intervals.setText(_translate("MainWindow", "Test Intervals"))
        self.pushButton_saveConfig.setText(_translate("MainWindow", "Save Config"))
        self.groupBox.setTitle(_translate("MainWindow", "Traning Data"))
        self.pushButton_save_training_data.setText(_translate("MainWindow", "Save Training Data"))
        self.pushButton_load_Training_data.setText(_translate("MainWindow", "Load Training Data"))
        self.label_Csv_Path.setText(_translate("MainWindow", "Csv Path"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Registers Values"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Tag Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Offset"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Inner/Outer"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Decription"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton_Save_Table_Data.setText(_translate("MainWindow", "Save Table Data"))

        self.pushButton_saveConfig.clicked.connect(self.button_clicked)
        self.pushButton_load_Training_data.clicked.connect(self.button_clicked)
        self.pushButton_save_training_data.clicked.connect(self.button_clicked)
        self.pushButton_Save_Table_Data.clicked.connect(self.button_clicked)
        self.load_config()
        self.load_Csv()

    def button_clicked(self):
        sender = self.MainWindow.sender().text()
        if sender == 'Save Config':
            self.save_config(self.lineEdit_ip.text(), self.lineEdit_Port.text(), self.lineEdit_number_of_samples.text(),
                             self.lineEdit_test_intervals.text())
        if sender == 'Load Training Data':
            self.load_training_data()
        if sender == 'Save Training Data':
            self.save_training_data()
        if sender == 'Save Table Data':
            self.get_table_input()

    def get_table_input(self):
        table_data = []
        for i in range(self.tableRow):
            table_data.clear()
            for j in range(self.tableColumn):
                if self.tableWidget.item(i, j).text() != "":
                    table_data.append(self.tableWidget.item(i, j).text())
            if table_data:
                print(table_data)
                self.save_table(table_data)
        sent_from = 'Save Table Data'
        self.show_popup(sent_from)

    def save_table(self, lst):
        self.config.read(self.file)
        temp_elements = ""
        temp_section = lst[0]
        for i in range(1, len(lst)):
            temp_elements += lst[i]
            if i != 3:
                temp_elements += ","
        self.config.set('REGISTERS', temp_section, temp_elements)
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)

    def save_config(self, ip, port, number_of_samples, test_intervals):
        self.config.read(self.file)
        self.config['PLC_CONFIG'] = {}
        self.config.set('PLC_CONFIG', 'ip', ip)
        self.config.set('PLC_CONFIG', 'port', port)
        self.config.set('PLC_CONFIG', 'train_data_no_samples', number_of_samples)
        self.config.set('PLC_CONFIG', 'test_intervals', test_intervals)
        with open(self.file, 'w') as configfile:
            self.config.write(configfile)
            sent_from = 'Save Config'
        self.show_popup(sent_from)

    def load_config(self):
        self.config.read(self.file)
        try:
            self.lineEdit_ip.setText(self.config['PLC_CONFIG']['ip'])
            self.lineEdit_Port.setText(self.config['PLC_CONFIG']['port'])
            self.lineEdit_number_of_samples.setText(self.config['PLC_CONFIG']['train_data_no_samples'])
            self.lineEdit_test_intervals.setText(self.config['PLC_CONFIG']['test_intervals'])
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.lineEdit_ip.setText('N/A')
            self.lineEdit_Port.setText('N/A')
            self.lineEdit_number_of_samples.setText('N/A')
            self.lineEdit_test_intervals.setText('N/A')


    def load_Csv(self):
        self.lineEdit_Csv_Path.setText(self.csvPath)

    def load_training_data(self):
        self.csvPath = self.lineEdit_Csv_Path.text()
        my_file = Path(self.csvPath)
        if my_file.is_file():
            self.df = pd.read_csv(self.csvPath)
            sent_from = 'Load Training Data'
            self.show_popup(sent_from)
        else:
            sent_from = 'File Not Found'
            self.show_popup(sent_from)

    def save_training_data(self):
        self.csvPath = self.lineEdit_Csv_Path.text()
        raws = []
        for i in range(10):
            timestamp = datetime.now()
            dataframe_raw = ["key" + str(i), timestamp, i ** 2]
            raws.append(dataframe_raw)
        data_frame = pd.DataFrame(raws, columns=['VarName', 'TimeString', 'VarValue'])
        data_frame.to_csv(self.csvPath)
        sent_from = 'Save Training Data'
        self.show_popup(sent_from)

    def show_popup(self, sender):
        msg = QMessageBox()
        msg.setWindowIcon(QtGui.QIcon(self.iconPath))
        if sender == 'Save Config':
            msg.setWindowTitle("Config Saved")
            msg.setText("Config Saved successfully")
            msg.setWindowIcon(QtGui.QIcon(r"Resources\sicon.png"))
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

        if sender == 'Load Training Data':
            msg.setWindowTitle("Training Data Loaded - First 5 Rows")
            msg.setText(str(self.df.head()))
            msg.setWindowIcon(QtGui.QIcon(r"Resources\sicon.png"))
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

        if sender == 'File Not Found':
            msg.setWindowTitle("Training Data")
            msg.setText("File Not Found")
            msg.setWindowIcon(QtGui.QIcon(r"Resources\sicon.png"))
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

        if sender == 'Save Training Data':
            msg.setWindowTitle("Training Data")
            msg.setText("Training Data Saved successfully")
            msg.setWindowIcon(QtGui.QIcon(r"Resources\sicon.png"))
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

        if sender == 'Save Table Data':
            msg.setWindowTitle("Table")
            msg.setText("Table Saved successfully")
            msg.setWindowIcon(QtGui.QIcon(r"Resources\sicon.png"))
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

        if sender == 'Table Empty':
            msg.setWindowTitle("Table")
            msg.setText("Table Empty")
            msg.setWindowIcon(QtGui.QIcon(r"Resources\sicon.png"))
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()



# Main entry.
def load_ui(config_file_path):

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setStyle('Fusion')
    ui = Ui_MainWindow(MainWindow, config_file_path)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    load_ui('config.ini') # used for local run