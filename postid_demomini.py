import requests

postid = {"id":114514}
print postid
try:
        #headers = {'Content-Type' : 'utf-8'}
 r = requests.post("http://rums.rd.dendai.ac.jp/home",data = postid)
 print r.text
except:
 print "ERROR"
