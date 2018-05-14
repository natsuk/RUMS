
import nfc
import binascii

#sys.path.append('/usr/local/src/nfcpy')
import nfc

service_code = 0x0109

def connected(tag):
    print tag
  
    if isinstance(tag, nfc.tag.tt3.Type3Tag):
        try:
            sc = nfc.tag.tt3.ServiceCode(service_code >> 6, service_code & 0x3f)
            bc = nfc.tag.tt3.BlockCode(2, service=0)
            print "block: %s" % binascii.hexlify(tag.read_without_encryption([sc], [bc]))
            print binascii.b2a_uu(tag.read_without_encryption([sc], [bc]))
        except Exception as e:                                                                                                                                                                                                                                              
            print "error: %s" % e
    else:   
        print "error: tag isn't Type3Tag"
        
clf = nfc.ContactlessFrontend('usb')
clf.connect(rdwr={'on-connect': connected})
clf.close()
