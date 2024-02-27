
def Encryption(s,k):
    print(s)
    file1 = open(s, "r+")
    n=file1.read()
    print(n)
    n= bytes(n, 'utf-8')
    print(n)
    global encstr
    encstr=""
    from cryptography.fernet import Fernet
    global f
    key = Fernet.generate_key()
    print("Key : ", str(key))
    import requests
    url="https://www.fast2sms.com/dev/bulk"
    params={

         "authorization":"RDM931xscvkd2Q7WA4uXah5qyiYJnmH6ITwtjEPS0grG8FKpObcyZnfzSN1krjCKuJOhmFwYRbad2BPs",
         "sender_id":"SMSINI",
         "message":key,
         "language":"english",
         "route":"p",
         "numbers":"8788640168"
    }
    requests.get(url,params=params)
    f = Fernet(key)
    encstr = f.encrypt(n)
    print("After encryption : ", encstr)
    print("------------------------------------------IN ENCRYPTION")
   
    return encstr
def Decryption(s,k):
    global f
    global encstr
    #p=Encryption(s,k)
    decstr=""
    decstr = f.decrypt(encstr)
    print("After decryption : ", decstr.decode())
    print("------------------------------------------IN DECRYTPION")
   
    return decstr



# root=tk.Tk()

# root.title("IMAGE AND TEXT ENCRYPTION USING AES ALGORITHM")
# file1 = open("myfile.txt","r+") 
# s=file1.read()
# frame = tk.LabelFrame(root, text="", width=600, height=300, bd=5, font=('times', 14, ' bold '),bg="antiquewhite2")
# frame.grid(row=0, column=0, sticky='nw')
# frame.place(x=370, y=120)
# l2 = tk.Label(frame, text="Enter Key :", width=12, font=("Times new roman", 15, "bold"), bg="antiquewhite2",bd=5)
# l2.place(x=30, y=30)
# t1 = tk.Entry(frame, textvar=new_key, width=20, font=('', 15),bd=5)
# t1.place(x=230, y=30)
                    
# btn = tk.Button(frame, text="Encrypt", bg="red",font=("",20),fg="white", width=9, height=1, command=onClickEncrypt)
# btn.place(x=230, y=180)

# btn = tk.Button(frame, text="Decrypt", bg="red",font=("",20),fg="white", width=9, height=1, command=onClickEncrypt)
# btn.place(x=330, y=180)
