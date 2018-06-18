
import nfc
import binascii

#sys.path.append('/usr/local/src/nfcpy')
import nfc

service_code = 0xfc49

def connected(tag):
    print tag
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
         i = 0
         f = open(str(service_code),"wb")
         while(1):
             sc = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
             bc = nfc.tag.tt3.BlockCode(i, service=0)
             data = tag.read_without_encryption([sc], [bc])
             #print(data)
             
             f.write(data)

             print "block: %s" % binascii.hexlify(tag.read_without_encryption([sc], [bc]))
             print binascii.b2a_uu(tag.read_without_encryption([sc], [bc]))
             i += 1
        except Exception as e:  
         print "error: %s" % e
         f.close
    else:   
        print "error: tag isn't Type3Tag"
        
clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
clf.close()
