import hashlib 
import nfc
import binascii
import requests
import json
from getpass import getpass
from time import sleep
from Tkinter import *
import ttk
import types




token = "null"

url =  "https://0.0.0.0:8443"

def connected(tag):

 print tag
 
 id =  str(tag.idm).encode("hex")  
 postid = {"card_id": id}
 print postid
 r = requests.post(url+"/id_check",postid,verify=False)
 
 
 global token
 token = r
 print token.text


 stat = token.status_code
 if stat == 201:
  app =  input_pw(id)
 elif stat == 203:

    root = Tk()
    root.title('Logout Form')
    frame1 = ttk.Frame(root)
    label1 = ttk.Label(frame1,text = 'Logout')
    button1 = ttk.Button(frame1, text = 'OK', command = sys.exit)
    frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
    label1.grid(row = 2, column = 2, sticky = E)
    button1.grid(row = 3, column = 2)
    for child in frame1.winfo_children():
       child.grid_configure(padx = 5, pady = 5)
    root.mainloop()

    print "log out"
 elif stat == 403:

     root = Tk()
     root.title('Login Form')
     frame1 = ttk.Frame(root)
     label1 = ttk.Label(frame1,text = 'This cards cannot use')
     button1 = ttk.Button(frame1, text = 'OK', command = sys.exit)
     frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
     label1.grid(row = 2, column = 2, sticky = E)
     button1.grid(row = 3, column = 2)
     for child in frame1.winfo_children():
        child.grid_configure(padx = 5, pady = 5)
     root.mainloop()

     print "this card is no use"



"""pass input"""
def input_pw(id):
 solt = json.loads(token.text)

 print "solt"
 print solt["token"]
 
 
 def final(event):
     print "final"
     #global root
     root.quit()

 

 while(1):

  root = Tk()
  root.title('Login Form')
  frame1 = ttk.Frame(root)
  label1 = ttk.Label(frame1, text = 'Input password')
  entry1 = ttk.Entry(frame1, width = 15, show = '*')
  button1 = ttk.Button(frame1,text = 'OK')
  frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
  label1.grid(row = 1, column = 2, sticky = N)
  button1.grid(row = 4, column = 2)
  button1.bind("<Button-1>",final)
  button1.bind("<Return>",final)
  entry1.grid(row = 2,column = 2)
  for child in frame1.winfo_children():
    child.grid_configure(padx = 10,pady = 10)
  root.mainloop()

  password=entry1.get()
  #id_pass =id_pass.get()
  #print id_pass
  #print type(id_pass)
  
  print entry1.get()

  #password = id_pass
  #password = getpass()
  password += solt["token"]
  s_hash = hashlib.sha256(password.encode()).hexdigest()
  
  post_h = {'card_id':id,'passwd':s_hash}
  post_h = json.dumps(post_h)
  
  #print post_h

  headers = {'content-type': 'application/json'}
  r = requests.post(url+"/pw_check",post_h,headers = headers,verify=False) 

 
  print "pass_request"
  print r.text
  #r = json.loads(r.text)
  stat = r.status_code



  if stat == 201:

   root = Tk()
   root.title('Login Form')
   frame1 = ttk.Frame(root)
   label1 = ttk.Label(frame1,text = 'Login')
   button1 = ttk.Button(frame1, text = 'OK', command = sys.exit)
   frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
   label1.grid(row = 2, column = 2, sticky = N)
   button1.grid(row = 3, column = 2)
   for child in frame1.winfo_children():
     child.grid_configure(padx = 10, pady = 10)
   root.mainloop()

   print "log in"
   return 1
  elif stat == 403:

     root = Tk()
     root.title('Login Form')
     frame1 = ttk.Frame(root)
     label1 = ttk.Label(frame1,text = 'miss password.Please retry to touch.')
     button1 = ttk.Button(frame1, text = 'OK')
     frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
     label1.grid(row = 2, column = 2, sticky = E)
     button1.grid(row = 3, column = 2)
     button1.bind("<Button-1>",final)
     button1.bind("<Return>",final)
     for child in frame1.winfo_children():
        child.grid_configure(padx = 10, pady = 10)
     root.mainloop()

     print "miss password"
     return 3
  else:

    root = Tk()
    root.title('Login Form')
    frame1 = ttk.Frame(root)
    label1 = ttk.Label(frame1,text = 'False pass')
    button1 = ttk.Button(frame1, text = 'OK')
    button1.bind("<Button-1>",final)
    button1.bind("<Return>",final)
    frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
    label1.grid(row = 2, column = 2, sticky = E)
    button1.grid(row = 3, column = 2)
    for child in frame1.winfo_children():
       child.grid_configure(padx = 10, pady = 10)
    root.mainloop()


    print "false pass" 



if __name__ == '__main__':

 while(1):

  root = Tk()
  root.title('Login Form')
  frame1 = ttk.Frame(root)
  label1 = ttk.Label(frame1,text = 'Touch your cards')
  frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
  label1.grid(row = 2, column = 2, sticky = E)
  for child in frame1.winfo_children():
     child.grid_configure(padx = 10, pady = 10)
  root.update()


  clf = nfc.ContactlessFrontend('usb')

  card = clf.connect(rdwr={'on-connect': connected})
  sleep(3)
  clf.close()



