
import nfc
import binascii
import json
from getpass import getpass

#sys.path.append('/usr/local/src/nfcpy')
import nfc
import requests


def connected(tag):
    print tag

    id =  str(tag.idm).encode("hex")
    password = getpass('input password: ')

    postid = {"card_id":id,"passwd":password}
    headers = {'content-type': 'application/json'}

    #print id
    postid = json.dumps(postid)
    try:
        r = requests.post("https://0.0.0.0:8443/register",data = postid,headers = headers,verify=False)
        print "ok!!"
        print r.text
    except:
        print "ERROR"

clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
clf.close()

