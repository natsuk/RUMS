
import nfc
import binascii

#sys.path.append('/usr/local/src/nfcpy')
import nfc
import requests


def connected(tag):
    print tag
    postid =  str(tag.idm).encode("hex")  
    r = requests.host("rums.rd.dendai.ac.jp/oyakata/getid.py",data = postid)
    

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
clf.close()

