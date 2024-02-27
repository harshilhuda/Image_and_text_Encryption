import requests
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog, QLabel, QAction, QMainWindow, QApplication, QMessageBox
import sqlite3
from PyQt5.uic import loadUiType
from Encrypter import Encrypter
from Decrypter import Decrypter
from pymsgbox import *
import os
import sys
import base64
from otp import generate_and_send_otp  # Import the function from otp.py

Qt = QtCore.Qt
ui, _ = loadUiType('ui.ui')

def start():
    global m
    m = Main_Window()
    m.show()

class encrypt_page():
    def __init__(self):
        self.file = {}
        self.stri = ""
        self.Handel_Buttons()
        self.pushButton_3.clicked.connect(self.chooseFile)
        self.pushButton_4.clicked.connect(self.onClickEncrypt)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def chooseFile(self):
        self.file = QFileDialog.getOpenFileName(self, 'Select Image for Encryption', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif)')
        if self.file[0]:
            pixmap = QtGui.QPixmap(self.file[0])
            self.lbl.setPixmap(pixmap.scaledToHeight(250))
            ba = QtCore.QByteArray()
            buff = QtCore.QBuffer(ba)
            buff.open(QtCore.QIODevice.WriteOnly)
            ok = pixmap.save(buff, "PNG")
            pixmap_bytes = ba.data()
            self.stri = base64.b64encode(pixmap_bytes)

    def onClickEncrypt(self):
        myKey = self.lineEdit.text()
        if not self.stri:
            QMessageBox.warning(self, "Error", "Please select an image for encryption.")
            return

        # Read ID and phone number from files
        try:
            with open("id.txt", "r") as f:
                id = f.read().strip()  # Remove leading/trailing whitespace
            with open("number.txt", "r") as f:
                num = f.read().strip()  # Remove leading/trailing whitespace
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "File not found.")
            return

        # Send OTP to the mobile number
        generate_and_send_otp(myKey, num)

        # Perform encryption
        x = Encrypter(self.stri, myKey)
        cipher = x.encrypt_image()
        with open("cipher.txt", "wb") as fh:
            fh.write(cipher)
        QMessageBox.information(self, "Success", "Encryption Successful !")

class decrypt_page():
    def __init__(self):
        self.cipher = {}
        self.Handel_Buttons()
        self.pushButton_5.clicked.connect(self.chooseFile1)
        self.pushButton_6.clicked.connect(self.onClickDecrypt)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))

    def chooseFile1(self):
        file = QFileDialog.getOpenFileName(self, 'Select Encrypted Image for Decryption', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif)')
        if file[0]:
            text = open(file[0]).read()
            self.cipher = text.encode('utf-8')

    def onClickDecrypt(self):
        myKey = self.lineEdit_2.text()
        if not self.cipher:
            QMessageBox.warning(self, "Error", "Please select an encrypted image for decryption.")
            return

        # Read ID from file
        try:
            with open("id.txt", "r") as f:
                id = f.read().strip()  # Remove leading/trailing whitespace
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "File not found.")
            return

        # Connect to the database and retrieve phone number
        sqliteConnection = sqlite3.connect('evaluation.db')
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT Phoneno FROM registration WHERE id = ?", (id,))
        result = cursor.fetchone()
        if result:
            num = result[0]
        else:
            QMessageBox.warning(self, "Error", "ID not found.")
            return

        # Ensure myKey is set
        if not myKey:
            QMessageBox.warning(self, "Error", "Please enter a decryption key.")
            return

        # Send OTP to the mobile number
        generate_and_send_otp(myKey, num)

        # Read encrypted data from file
        with open("cipher.txt", "rb") as fh:
            cipher_data = fh.read()

        # Perform decryption
        x = Decrypter(cipher_data)
        decrypted_image_data = x.decrypt_image(myKey)

        # Display decrypted image
        ba = QtCore.QByteArray(decrypted_image_data)
        pixmap = QtGui.QPixmap()
        ok = pixmap.loadFromData(ba, "PNG")
        assert ok
        self.lbl_2.setPixmap(pixmap.scaledToHeight(201))
        QMessageBox.information(self, "Success", "Decryption Successful !")

class Main_Window(QMainWindow, QWidget, ui, encrypt_page, decrypt_page):
    def __init__(self):
        QMainWindow.__init__(self)
        QWidget.__init__(self)
        self.setupUi(self)
        encrypt_page.__init__(self)
        decrypt_page.__init__(self)

        self.Handel_Buttons()
        self.stackedWidget.setCurrentIndex(0)

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.pushButton_8.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton_7.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = start()
    app.exec_()
