import hashlib 
import json
from datetime import datetime

def get_token_json(key):
    salt = str(datetime.now().strftime("%Y/%m/%d %H")+key)
    ret_token = hashlib.sha256(salt.encode()).hexdigest()
    
    token = {"token" : ret_token}
    return json.dumps(token)

def get_token(key):
    salt = str(datetime.now().strftime("%Y/%m/%d %H")+key)
    ret_token = hashlib.sha256(salt.encode()).hexdigest()
    return ret_token

def make_hash_of_synthesized_str(*str_array):
    synthesis_str = "" 
    for i in range(len(str_array)):
        synthesis_str += str_array[i]
    #return hashlib.sha256(synthesis_str.encode()).hexdigest()
    ret = hashlib.sha256(synthesis_str.encode()).hexdigest()
    print(ret)
    return ret
