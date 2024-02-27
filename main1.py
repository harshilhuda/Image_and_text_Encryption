from PyQt5 import QtCore,QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog,QLabel,QAction,QMainWindow,QApplication, QMessageBox
import sqlite3
from PyQt5.uic import loadUiType
from Encrypter import Encrypter
from Decrypter import Decrypter
from pymsgbox import *
from PIL import Image as Img
from PIL import ImageTk as ImgTk
#from tkinter import *
import Crypto
import base64
from tkinter import messagebox as ms
from Crypto.Cipher import AES
import os
import sys
Qt = QtCore.Qt
ui, _ = loadUiType('ui.ui')
def start():
    global m
    m = Main_Window()
    m.show()
    
class encrypt_page():
    def __init__(self):
        self.file={}
        self.stri=""
        self.Handel_Buttons()
        self.pushButton_3.clicked.connect(self.chooseFile)
        self.pushButton_4.clicked.connect(self.onClickEncrypt)
    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
    def chooseFile(self):
        #from tkinter.filedialog import askopenfilename
        '''self.file = QFileDialog.getOpenFileName(self, 'Open file')
        print(self.file)
        print(type(self.file))'''
        
       # Tuple<int, string> tuple = new Tuple<int, string>(50, "Tom");

        self.file = ('D:/100% Image_and_text_Encryption(updated txt decrp)/fn.png', 'All Files (*)')
       
        pixmap = QtGui.QPixmap(self.file[0])
        
        self.lbl.setPixmap(pixmap.scaledToHeight(201))
        if self.file != None:
            ba = QtCore.QByteArray()
            buff = QtCore.QBuffer(ba)
            buff.open(QtCore.QIODevice.WriteOnly) 
            ok = pixmap.save(buff, "PNG")
            #assert ok
            pixmap_bytes = ba.data()
            #print(type(pixmap_bytes))
            #data = self.file[0]
            self.stri = base64.b64encode(pixmap_bytes)
        
    def onClickEncrypt(self):
        f1=open("id.txt","r")
        id=f1.read()
        f1.close()
        
        myKey=self.lineEdit.text()
        # print(type(myKey))
        print(myKey)
        
        sqliteConnection = sqlite3.connect('evaluation.db')
            #cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
            
        r_set = sqliteConnection.execute("select id from registration where id =" + str(id) +"");
           #cursor.execute(sql_fetch_blob_query, (id))
        print(r_set)
        i=0
        for row in r_set:
               print("id=",row[0],)
               b=row[0]
               print(b)
               r_set1 = sqliteConnection.execute("select * from registration where id =" + str(b) +"");
               with open(r"number.txt", 'w') as f:
                   for row in r_set1:
                       line = str(row[5])
                       f.write(line)
                       print("Number: ",row[5])
        num = row[5]
        print(num)
        import requests
        url="https://www.fast2sms.com/dev/bulk"
        params={

             "authorization":"RDM931xscvkd2Q7WA4uXah5qyiYJnmH6ITwtjEPS0grG8FKpObcyZnfzSN1krjCKuJOhmFwYRbad2BPs",
             "sender_id":"SMSINI",
             "message":myKey,
             "language":"english",
             "route":"p",
             "numbers":num
        }
        requests.get(url,params=params)
        x = Encrypter(self.stri, myKey)
        cipher = x.encrypt_image()
        # print(type(cipher))
        # name = QFileDialog.getSaveFileName(self, 'Save File')
        # file = open(name,'w')
        # text = cipher
        # file.write(text)
        # file.close()
        #fh.write(base64_decoded.decode('base64'))
        fh = open("cipher.txt", "wb")
        fh.write(cipher)
        fh.close()
        QMessageBox.information(self, "QMessageBox.information()",
                                        "Encryption Successful !")
       
       
                    
        # cipherd = base64.b64decode(cipher.decode('utf-8'))
        # ba = QtCore.QByteArray(cipherd)
        # pixmap = QtGui.QPixmap()
        # ok = pixmap.loadFromData(ba, "PNG")
        #assert ok
        #self.lbl.setPixmap(pixmap.scaledToHeight(201))
        #x = Decrypter(cipher)
        #x.decrypt_image(myKey)
        
class decrypt_page():
    def __init__(self):
        self.cipher={}
        self.Handel_Buttons()
        self.pushButton_5.clicked.connect(self.chooseFile1)
        self.pushButton_6.clicked.connect(self.onClickDecrypt)
    def Handel_Buttons(self):
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
    def chooseFile1(self):
        file = QFileDialog.getOpenFileName(self, 'Upload File')
        text=open(file[0]).read()
        #print(text.encode('utf-8'))
        self.cipher= text.encode('utf-8')
    def onClickDecrypt(self):
        myKey=self.lineEdit_2.text()
        x = Decrypter(self.cipher)
        image=x.decrypt_image(myKey)
        
        ba = QtCore.QByteArray(image)
        pixmap = QtGui.QPixmap()
        ok = pixmap.loadFromData(ba, "PNG")
        assert ok        
        self.lbl_2.setPixmap(pixmap.scaledToHeight(201))
        QMessageBox.information(self, "QMessageBox.information()",
                                        "Decryption Successful !")
        # if image!=None:
        #     ba = QtCore.QByteArray()
        #     buff = QtCore.QBuffer(ba)
        #     buff.open(QtCore.QIODevice.WriteOnly) 
        #     ok = pixmap.save(buff, "PNG")
        #     assert ok
        #     pixmap_bytes = ba.data()
        #     #print(type(pixmap_bytes))
        #     #data = self.file[0]
        #     self.stri = base64.b64encode(pixmap_bytes)            
        
class Main_Window(QMainWindow, QWidget, ui,encrypt_page,decrypt_page):
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
    #connect()
    window = start()
    app.exec_()