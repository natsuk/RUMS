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

import res


url =  "https://0.0.0.0:8443"

def connected(tag):
 global resp
 resp = res.res(url)
 print tag
 id =  str(tag.idm).encode("hex")
 stat = resp.post_id(id)

 if stat == 1:
  app =  input_pw()
 elif stat == 2:

    #root = Tk()
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
 elif stat == 3 or stat == 0:

     #root = Tk()
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
def input_pw():
 
 
 
  def final(event):
     print "final"
     #global root
     root.quit()

 



  #root = Tk()
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
  
  print entry1.get()

  stat = resp.post_pw(password)


  if stat == 1:

   #root = Tk()
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
  elif stat == 0:

     #root = Tk()
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

    #root = Tk()
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



