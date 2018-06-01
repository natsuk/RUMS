import hashlib 
import nfc
import binascii
import requests
import json
from getpass import getpass


token = "null"

def connected(tag):
 print tag
 id =  str(tag.idm).encode("hex")  
 postid = {"card_id":id}
 print postid
 try:
  r = requests.post("http://133.14.14.69:8080/id_serch",postid)
  global token
  token = r
 except:
  print "ERROR"

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
  s_hash = hashlib.sha256(password).hexdigest()
  #print s_hash
  post_h = {'pass':s_hash,'card_id':id}
  post_h = json.dumps(post_h)
  #print post_h
  headers = {'content-type': 'application/json'}
  r = requests.post("http://133.14.14.69:8080/pw_serch",post_h,headers = headers) 

  print "pass_request"
  print r.text
  r = json.loads(r.text)
  if r["stat"] == 'OK':
   return 1
  else:
   print "false pass" 



if __name__ == '__main__':

 while(1):
  clf = nfc.ContactlessFrontend('usb')
  card = clf.connect(rdwr={'on-connect': connected})
  clf.close()

  id =  str(card.idm).encode("hex") 

  app = 0
  print token.text
  stat = token.status_code
  if stat == 200:
   app =  input_pw(id)
  elif stat == 403:
   print "this card is no use"
 
  if app == 1:
   print "sacses"
  else: 
   print "OH,ERROR"

