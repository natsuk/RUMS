import hashlib 
import nfc
import binascii
import requests
import json
from getpass import getpass
from time import sleep

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
  print "log out"
 elif stat == 403:
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

 while(1):
#パスワード入力求める
  password = getpass('input password: ')
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
  if stat == 202:
   print "log in"
   return 1
  elif stat == 404:
   print "miss password"
   return 3
  else:
   print "false pass" 



if __name__ == '__main__':

 while(1):
  clf = nfc.ContactlessFrontend('usb')
  #カードタッチで以下の関数が呼び出される
  card = clf.connect(rdwr={'on-connect': connected})
  sleep(3)
  clf.close()



