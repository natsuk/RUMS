from flask import Flask, render_template,request,g,redirect,url_for,Response,session
import sqlite3
import hashlib

import script

DATABASE = 'usr.db'
TABLE = 'usr_table'

app = Flask(__name__)
app.secret_key = 'hogehoge'

@app.route('/id_check',methods=['POST'])
def id_check():
    # POSTされたIDを取得
    Student_id = request.form['card_id']

    # DB接続(初期化)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # POSTされたIDをDBと照合するための処理
    id = cur.execute('select Student_id from usr_table where Student_id = \'' +Student_id+ '\'')
    response = Response()
    #IDがあるかないか
    if len(cur.fetchall()) == 0:
        response.status_code = 403
        conn.commit()
        cur.close()
        return response

    # ログイン状態取得
    cur.execute('select inout from usr_table where Student_id = \'' +Student_id + '\'')
    data = cur.fetchone() # data[0] is inout
    inout = data[0]
    
    if inout == 1: #ログイン状態にあった場合
        cur.execute('update usr_table set inout = 0 where Student_id = \''+Student_id+'\'')
        response.status_code = 203
    else:
        response.status_code = 201
        response.data = script.get_token_json(Student_id)
        # DBに発行したトークンを保存
        cur.execute('update usr_table set token = \''+script.get_token(Student_id)+'\'where Student_id = \''+Student_id+'\'')
    
    # DBの更新を保存&DBクローズ
    conn.commit()
    cur.close()
    
    response.content_type = 'application/json'
    return response

@app.route('/pw_check',methods=['POST'])
def pw_check():
    # POSTされたjsonの取得
    pw_msg = request.json
    # jsonの展開
    Student_id = pw_msg['card_id']
    got_pw = pw_msg = pw_msg['passwd']
    print(Student_id)
    print(got_pw) 
    # DB接続(初期化)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # POSTされたIDによってpasswardを引き出す
    cur.execute('select passwd, token from usr_table where Student_id = \'' +Student_id + '\'')
    response = Response()
    data = cur.fetchone()
    if len(data) == 0:
        response.status_code = 403
        conn.commit()
        cur.close()
        return response
    
    true_pw = data[0]
    token = data[1]
    print (data)
    print(true_pw)
    # DBから引き抜いたPWとtokenを合成、ハッシュ化
    made_hash = script.make_hash_of_synthesized_str(true_pw,token)
    
    # パスワードの判定
    response = Response()
    if got_pw == made_hash:
        response.status_code=202
        # DBのinout_stateを1に
        cur.execute('update usr_table set inout = 1 where Student_id = \''+Student_id+'\'')
    else:
        response.status_code = 405
   
    # DBの更新を保存&DBクローズ
    conn.commit()
    cur.close()
    return response

@app.route('/logout',methods=['POST'])
def logout():
    response = Response()
    response.status_code = 201
    session['check'] = False
    session['id'] = None
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080,debug=False)
