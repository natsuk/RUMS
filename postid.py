
import nfc
import binascii

#sys.path.append('/usr/local/src/nfcpy')
import nfc
import requests


def connected(tag):
    print tag
    id =  str(tag.idm).encode("hex")  
    postid = ["id":id]
    print postid
   # try:
    r = requests.post("rums.rd.dendai.ac.jp/oyakata/RUMS/getid.py",data = postid)
    print r.text
 #   except:
  #   print "ERROR"

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
clf.close()

