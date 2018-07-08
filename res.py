# -*- coding: utf-8 -*-
import hashlib
import nfc
import binascii
import requests
import json
from getpass import getpass
from time import sleep




class res():
    
    def __init__(self,url):
        self.url = url


    "idのチェックを行う。必ず最初に行え。 initに入れてもいいかな？　返り値　0 = error１＝login 2=logout 3=nouse "
    def post_id(self,id):
        self.id = id
        #渡されたIDをぶん投げ
        postid = {"card_id": self.id}
        try:
            r = requests.post(self.url+"/id_check",postid,verify=False)
        except:
            return 0 #false
        self.token = r
        stat = self.token.status_code
        if stat == 201:
            #ステータスコードで判断
            #LOGIN
            try:
                self.text = json.loads(self.token.text)
                self.solt = self.text["token"]
                self.id = id
                return 1
            except:
                #LOGOUT
                return 2
            #失敗
        elif stat == 403:
            return 3
        
    "パスワードチェック 1 = 成功　0 ＝ 失敗"
    def post_pw(self,passwd):
        
        passwd = self.id + passwd
        passwd = hashlib.sha256(passwd.encode()).hexdigest()
        #ソルトを混ぜてハッシュ化
        passwd += self.solt
        self.hash_pw = hashlib.sha256(passwd.encode()).hexdigest()
        #データまとめてjsonに
        post_data = {"card_id":self.id,"passwd":self.hash_pw}
        post_data = json.dumps(post_data)
        headers = {'content-type': 'application/json'}
        
        #投げる
        r = requests.post(self.url+"/pw_check",post_data,headers = headers,verify=False)
        stat = r.status_code
        
        #帰ってきたステータスコードで考える
        if stat == 201:
            return 1
        elif stat == 403:
            return 0
        else:
            return 3
            

    """カードの登録　1=成功　0=失敗"""
    def register(self,id,passwd):
        
        #データまとめてjsonに
        pass = id + passwd;
        pass = hashlib.sha256(pass.encode()).hexdigest()
        postid = {"passwd":pass}
        headers = {'content-type': 'application/json'}
        postid = json.dumps(postid)
        
        #ぶん投げ
        r = requests.post(self.url+"/register",data = postid,headers = headers,verify=False)
        stat = r.status_code
        
        #ステータスコードで考える
        if stat == 201:
            return 1
        elif stat == 403:
            return 0

