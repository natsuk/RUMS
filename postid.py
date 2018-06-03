import hashlib 
import nfc
import binascii
import requests
import json
from getpass import getpass
from time import sleep

token = "null"
url =  "http://0.0.0.0:8080"

def connected(tag):
 print tag
 id =  str(tag.idm).encode("hex")  
 postid = {"card_id": id}
 print postid
 r = requests.post(url+"/id_check",postid)
 global token
 
 token = r
 print token.text

 stat = token.status_code
 if stat == 201:
  app =  input_pw(id)
 elif stat == 203:
  print "log out"
 elif stat == 403:
  print "this card is no use"



"""pass input"""
def input_pw(id):
 #printf"input password"
 solt = json.loads(token.text)
 #solt = token
 print "solt"
 print solt["token"]
 while(1):
  password = getpass('input password: ')
  password += solt["token"]
  s_hash = hashlib.sha256(password.encode()).hexdigest()
  #print s_hash
  post_h = {'card_id':id,'passwd':s_hash}
  post_h = json.dumps(post_h)
  #print post_h
  headers = {'content-type': 'application/json'}
  r = requests.post(url+"/pw_check",post_h,headers = headers) 

  print "pass_request"
  print r.text
  #r = json.loads(r.text)
  stat = r.status_code


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
  card = clf.connect(rdwr={'on-connect': connected})
  sleep(3)
  clf.close()



