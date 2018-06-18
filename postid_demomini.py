import requests
import json

postid = {"card_id":"111116rd000"}
print postid

try:
 r = requests.post("https://133.14.14.69:8443/id_check",postid,verify=False)
 #r = requests.post("http://:8443/id_chack",postid)
 print "OK!!"
 print r.text
except:
 print "ERROR"
