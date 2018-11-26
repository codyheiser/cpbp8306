# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Heiser_9.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
"""
Heiser_9.py
@author: Cody Heiser


usage: Heiser_9.py 

"""

from PyQt5 import QtCore, QtGui, QtWidgets
from Heiser_7 import dna_sequence # import DNA sequence class and associated functions for analysis

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(623, 499)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEdit_input = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_input.setGeometry(QtCore.QRect(20, 40, 581, 71))
        self.plainTextEdit_input.setObjectName("plainTextEdit_input")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(230, 120, 161, 46))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 10, 111, 25))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 170, 181, 25))
        self.label_2.setObjectName("label_2")
        self.plainTextEdit_input_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_input_2.setGeometry(QtCore.QRect(20, 200, 581, 71))
        self.plainTextEdit_input_2.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.plainTextEdit_input_2.setObjectName("plainTextEdit_input_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 270, 181, 25))
        self.label_3.setObjectName("label_3")
        self.plainTextEdit_input_3 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_input_3.setGeometry(QtCore.QRect(20, 300, 581, 71))
        self.plainTextEdit_input_3.setReadOnly(True)
        self.plainTextEdit_input_3.setObjectName("plainTextEdit_input_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 410, 113, 21))
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 410, 113, 21))
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(330, 410, 113, 21))
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(480, 410, 113, 21))
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 380, 111, 25))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(180, 380, 111, 25))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(330, 380, 111, 25))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(480, 380, 111, 25))
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 623, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # define connections between widgets when button is pressed
        self.pushButton.clicked.connect(self.get_sequence)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Analyze Sequence"))
        self.label.setText(_translate("MainWindow", "Input Sequence"))
        self.label_2.setText(_translate("MainWindow", "Reverse Complement (DNA)"))
        self.label_3.setText(_translate("MainWindow", "Reverse Complement (RNA)"))
        self.label_4.setText(_translate("MainWindow", "Length (bp)"))
        self.label_5.setText(_translate("MainWindow", "GC Content (%)"))
        self.label_6.setText(_translate("MainWindow", "Mol Wt (g/mol)"))
        self.label_7.setText(_translate("MainWindow", "Tm (C)"))

    def get_sequence(self):
    	'''
    	define function to get DNA sequence, convert to dna_sequence class, 
    	and return values to their respective output spots
    	'''
    	try:
    		# retrieve DNA sequence as dna_sequence class object
    		dna = dna_sequence(self.plainTextEdit_input.toPlainText())

    	except ValueError as err:
    		# if letters other than A, T, C, and G are given, print error to status bar and exit function
    		self.statusbar.showMessage(str(err))
    		return

    	# print reverse complements
    	self.plainTextEdit_input_2.setPlainText(dna.rev_comp('DNA'))
    	self.plainTextEdit_input_3.setPlainText(dna.rev_comp('RNA'))

    	# print sequence length in bp
    	self.lineEdit.setText(str(dna.seq_length))

    	# print GC content
    	self.lineEdit_2.setText(str(dna.gc_content()))

    	# print molecular weight
    	self.lineEdit_3.setText(str(dna.mass_calc()))

    	# print Tm
    	self.lineEdit_4.setText(str(dna.tm_calc()))

    	# reset status bar for successful updating of UI
    	self.statusbar.showMessage('Success!')


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
