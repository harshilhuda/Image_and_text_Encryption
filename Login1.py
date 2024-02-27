
from tkinter import *
from tkinter import messagebox as ms
from PIL import ImageTk 
import sqlite3



class login_system:
    def __init__(self,root):
        self.root = root
        self.root.title("login ")
        w,h = root.winfo_screenwidth(),root.winfo_screenheight()
        root.geometry("%dx%d+0+0"%(w,h))
        
        ##______________________All Images ___________________________##
        
    #=====Variable======#
        
    # Some Usefull variables
    # Create Widgets
        
        # Some Usefull variables
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        
        self.bg1_icon=ImageTk.PhotoImage(file=r"L.jpg")

        self.bg_icon=ImageTk.PhotoImage(file=r"L.jpg")
        self.user_icon=ImageTk.PhotoImage(file=r"u1.png")
        self.pass_icon=ImageTk.PhotoImage(file=r"p1.jpg")
        self.bg=ImageTk.PhotoImage(file=r"reg1.jpg")
        
        bg_lbl=Label(self.root,image=self.bg).pack()
        
        
        bg_lbl=Label(self.root,image=self.bg1_icon).pack()
        
        title=Label(self.root, text="LOGIN", font=("Times new roman", 40, "bold"), bg="skyblue",fg="red",bd=5,relief=RAISED)
        title.place(x=0, y=0,relwidth=1)
        
        Login_frame=Frame(self.root,bg="white")
        Login_frame.place(x=550,y=150)
        
        logolbl=Label(Login_frame,image=self.bg_icon,bd=0).grid(row=0,columnspan=2,pady=20)
        
        lbluser=Label(Login_frame,text="Username",image=self.user_icon,compound=LEFT,font=("Times new roman", 20, "bold"),bg="white").grid(row=1,column=0,padx=20,pady=10)
        txtuser=Entry(Login_frame,bd=5,textvariable=self.username ,relief=GROOVE,font=("",15)).grid(row=1,column=1,padx=20)
        
        lblpass=Label(Login_frame,text="Password",image=self.pass_icon,compound=LEFT,font=("Times new roman", 20, "bold"),bg="white").grid(row=2,column=0,padx=20,pady=10)
        txtpass=Entry(Login_frame,bd=5,textvariable=self.password,relief=GROOVE,font=("",15),show='*').grid(row=2,column=1,padx=20)
        
        btn_log=Button(Login_frame,text="Login",command=self.login,width=15,font=("Times new roman", 14, "bold"),bg="skyblue",fg="red").grid(row=3,column=1,pady=10)
        
        
    
       
        # Login Function
    def login(self):
        # Establish Connection

        with sqlite3.connect('evaluation.db') as db:
            c = db.cursor()

        # Find user If there is any take proper action
        db = sqlite3.connect('evaluation.db')
        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS registration"
                       "(Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT,Gender TEXT,age TEXT , password TEXT)")
        db.commit()
        find_entry = ('SELECT * FROM registration WHERE username = ? and password = ?')
        c.execute(find_entry, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        
        find_entry1 = ('SELECT id FROM registration WHERE username = ?')
        c.execute(find_entry1, [(self.username.get())])
        result1 = c.fetchall()
        print(result1)
         
        for row in result1:
             print("id=",row[0],)
             id=str(row[0])
             print(id)
             with open(r"id.txt", 'w') as f:
                 
             
                f.write(str(id))
             # f1=open("id.txt","w")
             # f1.write(str(id))
        

        if result:
            msg = "LogIn sucessfully"
            # self.logf.pack_forget()
            # self.head['text'] = self.username.get() + '\n Loged In'
            # msg = self.head['text']
            #            self.head['pady'] = 150
            print(msg)
            ms.showinfo("messege", "LogIn sucessfully")
            # ===========================================
            #import main
          #  root.destroy()

            from subprocess import call
            call(['python','upload.py'])

            # ================================================
        else:
            ms.showerror('Oops!', 'Username Or Password Did Not Found/Match.')
        
    
    
        
       
        
        
root = Tk()
obj = login_system(root)
root.mainloop()