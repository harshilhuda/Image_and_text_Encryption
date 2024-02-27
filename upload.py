import hashlib
import base64
import hashlib
from random import randint
import smtplib
from email.message import EmailMessage
import imghdr
import string
from text_encryption import Encryption
from text_encryption import Decryption
from tkinter import *
import tkinter as tk
from Crypto.Cipher import AES
from PIL import Image ,ImageTk
from tkinter.ttk import *
from pymsgbox import *
from tkinter import messagebox as ms
from tkinter.filedialog import askopenfilename
import sqlite3
from otp import generate_and_send_otp  # Import the function from otp.py

root = tk.Tk()

root.title("IMAGE AND TEXT ENCRYPTION USING AES ALGORITHM")
bg = Image.open(r"dd2.jpg")
bg.resize((1000, 850), Image.NEAREST)
bg_img = ImageTk.PhotoImage(bg)
bg_lbl = tk.Label(root, image=bg_img)
bg_lbl.place(x=30, y=100)

w = tk.Label(root, text="IMAGE AND TEXT ENCRYPTION ", width=40, background="skyblue", height=2,
             font=("Times new roman", 19, "bold"))
w.place(x=150, y=15)

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.configure(background="skyblue")

s_file = ""
new_key = tk.IntVar()
new_key1 = tk.StringVar()


def upload_Image():
    global fn
    fileName = askopenfilename(initialdir='D:/', title='Select image for Encryption ',
                               filetypes=[("png", "*.*")])
    IMAGE_SIZE = 200
    imgpath = fileName
    fn = fileName
    im1 = Image.open(imgpath)

    md5_hash = hashlib.md5()
    with open(fn, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
        print(md5_hash.hexdigest())
        a = md5_hash.hexdigest()
        print(str(a))

    db = sqlite3.connect('evaluation.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS img_database"
                   "(name TEXT, key TEXT)")
    db.commit()
    print("hello1")
    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()
        bad_chars = [',', '(', ')', "'"]
        c.execute('SELECT key FROM img_database WHERE key = ?', (a,))
        print("hello2")
        records = c.fetchall()
        print(records)
        print(type(records))
        listToStr = ' '.join([str(elem) for elem in records])

        print(listToStr)
        delete_dict = {sp_character: '' for sp_character in string.punctuation}
        delete_dict[' '] = ''
        table = str.maketrans(delete_dict)
        test_string = listToStr.translate(table)

        # printing resultant string
        print(str(test_string))
        print(1)
        print(str(a))
        # print(concatstr)

        if test_string == str(a):
            ms.showinfo('Error!', 'Image Already Exist !')

        else:
            conn = sqlite3.connect('evaluation.db')
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO img_database(name, key) VALUES(?,?)',
                    (fileName, a))
                conn.commit()
                ms.showinfo('Success!', 'Stored Successfully !')
                im1 = im1.save("fn.png")
                from subprocess import call
                call(["python", "main.py"])

                # frame = tk.LabelFrame(root, text="", width=600, height=300, bd=5, font=('times', 14, ' bold
                # '),bg="antiquewhite2") frame.grid(row=0, column=0, sticky='nw') frame.place(x=370, y=120)
                #
                # l2 = tk.Label(frame, text="Enter Key :", width=12, font=("Times new roman", 15, "bold"),
                # bg="antiquewhite2",bd=5) # l2.place(x=30, y=30) # t1 = tk.Entry(frame, textvar=new_key, width=20,
                # font=('', 15),bd=5) # t1.place(x=230, y=30)
                #
                # btn = tk.Button(frame, text="Encrypt", bg="red",font=("",20),fg="white", width=9, height=1,
                # command=onClickEncrypt) # btn.place(x=230, y=180)


def upload_text():
    global fn
    fileName = askopenfilename(initialdir='D:/', title='Select image for Encryption ',
                               filetypes=[("all files", "*.*")])
    print(type(fileName))
    file1 = open(fileName, "r+")
    fn = file1.read()
    print(fn)

    md5_hash = hashlib.md5()
    with open(fileName, "rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
        print(md5_hash.hexdigest())
        a = md5_hash.hexdigest()

    db = sqlite3.connect('evaluation.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS text_database"
                   "(name TEXT, key TEXT)")
    db.commit()

    with sqlite3.connect('evaluation.db') as db:
        c = db.cursor()
        bad_chars = [',', '(', ')', "'"]
        c.execute('SELECT key FROM text_database WHERE key = ?', (a,))
        records = c.fetchall()
        print(records)
        print(type(records))
        listToStr = ' '.join([str(elem) for elem in records])

        print(listToStr)
        delete_dict = {sp_character: '' for sp_character in string.punctuation}
        delete_dict[' '] = ''
        table = str.maketrans(delete_dict)
        test_string = listToStr.translate(table)

        # printing resultant string
        print(str(test_string))
        print(1)
        print(str(a))
        # print(concatstr)

        if test_string == str(a):
            ms.showinfo('Error!', 'This Text File Already Exist !')

        else:
            conn = sqlite3.connect('evaluation.db')
            with conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO text_database(name, key) VALUES(?,?)',
                               (fileName, a))
                conn.commit()
                ms.showinfo('Success!', 'Stored Successfully !')
                save_text = open("myfile.txt", 'w')
                save_text.write(fn)
                save_text.close()
                frame = tk.LabelFrame(root, text="", width=600, height=300, bd=5,
                                      font=('times', 14, ' bold '), bg="antiquewhite2")
                frame.grid(row=0, column=0, sticky='nw')
                frame.place(x=370, y=120)

                def onClickDecrypt():
                    root = tk.Tk()
                    root.geometry('500x300')
                    root.title("Decryption")
                    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
                    root.geometry("%dx%d+0+0" % (w, h))

                    key = new_key1.get()
                    cipher1 = Decryption(fileName, key)
                    T = Text(root, height=700, width=1200)
                    T.place(x=50, y=50)
                    T.insert(tk.END, cipher1)
                    ms.showinfo('Success!', 'Decryption Successful !')

                def onClickEncrypt():
                    f1 = open("id.txt", "r")
                    id = f1.read()
                    f1.close()

                    key = new_key.get()
                    print(key)

                    sqliteConnection = sqlite3.connect('evaluation.db')
                    print("Connected to SQLite")

                    r_set = sqliteConnection.execute("select id from registration where id =" + str(id) + "");
                    print(r_set)
                    i = 0
                    for row in r_set:
                        print("id=", row[0], )
                        b = row[0]
                        print(b)
                        r_set1 = sqliteConnection.execute("select * from registration where id =" + str(b) + "");
                        with open(r"number.txt", 'w') as f:
                            for row in r_set1:
                                line = str(row[5])
                                f.write(line)
                                print("Number: ", row[5])
                    num = row[5]
                    print(num)
                    import requests
                    url = "https://www.fast2sms.com/dev/bulk"
                    params = {

                        "authorization": "RDM931xscvkd2Q7WA4uXah5qyiYJnmH6ITwtjEPS0grG8FKpObcyZnfzSN1krjCKuJOhmFwYRbad2BPs",
                        "sender_id": "SMSINI",
                        "message": key,
                        "language": "english",
                        "route": "p",
                        "numbers": num
                    }
                    requests.get(url, params=params)
                    cipher = Encryption(fileName, key)
                    ms.showinfo('Success!', 'Encryption Successful !')
                    frame1 = tk.LabelFrame(root, text="", width=600, height=300, bd=5,
                                           font=('times', 14, ' bold '), bg="antiquewhite2")
                    frame1.grid(row=0, column=0, sticky='nw')
                    frame1.place(x=370, y=120)

                    l2 = tk.Label(frame1, text="Enter Key :", width=12, font=("Times new roman", 15, "bold"),
                                  bg="antiquewhite2", bd=5)
                    l2.place(x=30, y=30)
                    t1 = tk.Entry(frame1, textvar=new_key1, width=20, font=('', 15), show='*', bd=5)
                    t1.place(x=230, y=30)

                    btn = tk.Button(frame1, text="Decrypt", bg="red", font=("", 20), fg="white", width=9, height=1,
                                    command=onClickDecrypt)
                    btn.place(x=200, y=180)

                btn = tk.Button(frame, text="Encrypt", bg="red", font=("", 20), fg="white", width=9, height=1,
                                command=onClickEncrypt)
                btn.place(x=200, y=180)


Disease2 = tk.Button(root, text="UPLOAD IMAGE", command=upload_Image, width=20, height=2, bd=0, background="skyblue",
                     foreground="black", font=("times new roman", 14, "bold"))
Disease2.place(x=800, y=18)

Disease3 = tk.Button(root, text="UPLOAD TEXT FILE", command=upload_text, width=20, height=2, bd=0, background="skyblue",
                     foreground="black", font=("times new roman", 14, "bold"))
Disease3.place(x=1000, y=18)

root.mainloop()
