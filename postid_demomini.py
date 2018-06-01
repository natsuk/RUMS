import requests
import json

postid = {"card_id":"16rd000"}
print postid
#成功例
try:
 r = requests.post("http://133.14.14.69:8080/test",postid)
 print r.text
except:
 print "ERROR"
