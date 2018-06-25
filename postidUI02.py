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
#接続先ＵＲＬの指定（今は自身に対して行ってる）
url =  "https://0.0.0.0:8443"

def connected(tag):
#タッチされたらタグとか出力
 print tag
 #カードＩＤを１６進数の変換して辞書型で渡す
 id =  str(tag.idm).encode("hex")  
 postid = {"card_id": id}
 print postid
 r = requests.post(url+"/id_check",postid,verify=False)
 
 #帰ってきたものの確認
 global token
 token = r
 print token.text

 #ステータスコードで動作を変える
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
#パスワード入力
 #printf"input password"
#帰ってきたデータを解いてデータを引き抜く
 solt = json.loads(token.text)
 #solt = token
 print "solt"
 print solt["token"]

 id_pass = StringVar()
 id_pass.set("")

 while(1):
#パスワード入力求める

  root = Tk()
  root.title('Login Form')
  frame1 = ttk.Frame(root)
  label1 = ttk.Label(frame1, text = 'Input password')
  entry1 = ttk.Entry(frame1,textvariable = id_pass, width = 15, show = '*')
  button1 = ttk.Button(frame1,text = 'OK',command=root.destroy)
  frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
  label1.grid(row = 3, column = 2, sticky = E)
  button1.grid(row = 4, column = 2)
  entry1.grid(row = 2,column = 2)
  for child in frame1.winfo_children():
    child.grid_configure(padx = 5,pady = 5)
  root.mainloop()


  id_pass =id_pass.get()
  print id_pass
  print type(id_pass)

  password = id_pass
  #password = getpass()
#送信用にデータ変換
  password += solt["token"]
  s_hash = hashlib.sha256(password.encode()).hexdigest()
  
  post_h = {'card_id':id,'passwd':s_hash}
  post_h = json.dumps(post_h)
  
  #print post_h
  #データ渡す
  headers = {'content-type': 'application/json'}
  r = requests.post(url+"/pw_check",post_h,headers = headers,verify=False) 

 #帰ってきたデータを読む
  print "pass_request"
  print r.text
  #r = json.loads(r.text)
  stat = r.status_code


#返信で動作を変える
  if stat == 201:

   root = Tk()
   root.title('Login Form')
   frame1 = ttk.Frame(root)
   label1 = ttk.Label(frame1,text = 'Login')
   button1 = ttk.Button(frame1, text = 'OK', command = sys.exit)
   frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
   label1.grid(row = 2, column = 2, sticky = E)
   button1.grid(row = 3, column = 2)
   for child in frame1.winfo_children():
     child.grid_configure(padx = 5, pady = 5)
   root.mainloop()

   print "log in"
   return 1
  elif stat == 403:

     root = Tk()
     root.title('Login Form')
     frame1 = ttk.Frame(root)
     label1 = ttk.Label(frame1,text = 'miss password')
     button1 = ttk.Button(frame1, text = 'OK', command = root.destroy)
     frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
     label1.grid(row = 2, column = 2, sticky = E)
     button1.grid(row = 3, column = 2)
     for child in frame1.winfo_children():
        child.grid_configure(padx = 5, pady = 5)
     root.mainloop()

     print "miss password"
     return 3
  else:

    root = Tk()
    root.title('Login Form')
    frame1 = ttk.Frame(root)
    label1 = ttk.Label(frame1,text = 'False pass')
    button1 = ttk.Button(frame1, text = 'OK', command = sys.exit)
    frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
    label1.grid(row = 2, column = 2, sticky = E)
    button1.grid(row = 3, column = 2)
    for child in frame1.winfo_children():
       child.grid_configure(padx = 5, pady = 5)
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
     child.grid_configure(padx = 5, pady = 5)
  root.update()


  clf = nfc.ContactlessFrontend('usb')
  #カードタッチで以下の関数が呼び出される
  card = clf.connect(rdwr={'on-connect': connected})
  sleep(3)
  clf.close()



