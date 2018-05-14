import nfc

def on_startup(targets):
        print("on_startup()")
        return targets

def on_connect(tag):
        print("Tag: {}".format(tag))
        print("Tag type: {}".format(tag.type))
        #print '\n'.join(tag.dump())
        if tag.ndef:
                print tag.ndef.message.pretty()
        #return True

def on_release(tag):
        print("on_release()")
        if tag.ndef:
                print(tag.ndef.message.pretty())

clf = nfc.ContactlessFrontend('usb')
if clf:
        print("Clf: {}".format(clf))
        clf.connect(rdwr={
                'on-startup': on_startup,
                'on-connect': on_connect,
                'on-release': on_release
        })

clf.close()
