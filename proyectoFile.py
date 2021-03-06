# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pro.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Proyecto Final")
        MainWindow.resize(473, 487)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Source Sans Pro Light")
        font.setPointSize(34)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.hum = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.press_it(0))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.hum.setFont(font)
        self.hum.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"selection-background-color: rgb(255, 170, 0);")
        self.hum.setObjectName("hum")
        self.verticalLayout.addWidget(self.hum)
        self.temp = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.press_it(1))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.temp.setFont(font)
        self.temp.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"selection-background-color: rgb(255, 170, 0);")
        self.temp.setObjectName("temp")
        self.verticalLayout.addWidget(self.temp)
        self.acc = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.press_it(2))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.acc.setFont(font)
        self.acc.setAutoFillBackground(False)
        self.acc.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"selection-background-color: rgb(255, 170, 0);")
        self.acc.setInputMethodHints(QtCore.Qt.ImhNone)
        self.acc.setShortcut("")
        self.acc.setAutoDefault(False)
        self.acc.setFlat(False)
        self.acc.setObjectName("acc")
        self.verticalLayout.addWidget(self.acc)
        self.giro = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.press_it(3))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.giro.setFont(font)
        self.giro.setAutoFillBackground(False)
        self.giro.setStyleSheet("background-color: rgb(170, 170, 255);\n"
"selection-background-color: rgb(255, 170, 0);")
        self.giro.setInputMethodHints(QtCore.Qt.ImhNone)
        self.giro.setShortcut("")
        self.giro.setAutoDefault(False)
        self.giro.setFlat(False)
        self.giro.setObjectName("giro")
        self.verticalLayout.addWidget(self.giro)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Proyecto Final", "Proyecto Final"))
        self.label.setText(_translate("Proyecto Final", "TextLabel"))
        self.hum.setText(_translate("Proyecto Final", "TEMPERATURA Y HUMEDAD"))
        self.temp.setText(_translate("Proyecto Final", "TEMPERATURA OBJETO"))
        self.acc.setText(_translate("Proyecto Final", "ACELEROMETRO"))
        self.giro.setText(_translate("Proyecto Final", "GIROSCOPIO"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
