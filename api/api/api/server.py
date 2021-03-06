from flask import Flask, render_template,request,g,redirect,url_for,Response,session
import sqlite3
import hashlib
import json
import script
from db import DB_operation
import ssl
import logging

app = Flask(__name__)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('ssl/cert.pem', 'ssl/key.pem')
app.secret_key = 'hogehog'

@app.route('/id_check',methods=['POST'])
def id_check():
    # POSTされたIDを取得
    Student_id = request.form['card_id']

    # DB接続(初期化)
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    # POSTされたIDをDBと照合するための処理
    id = cur.execute('select Student_id from usr_table where Student_id = \'' +Student_id+ '\'')
    response = Response()
    #IDがあるかないか
    if len(cur.fetchall()) == 0:
        response.status_code = 403
        conn.commit()
        cur.close()
        logging.info('CARD ERROR: '+Student_id+' is not registerd.')
        return response

    # ログイン状態取得
    cur.execute('select inout from usr_table where Student_id = \'' +Student_id + '\'')
    data = cur.fetchone() # data[0] is inout
    inout = data[0]
    
    if inout == 1: #ログイン状態にあった場合
        cur.execute('update usr_table set inout = 0 where Student_id = \''+Student_id+'\'')
        response.status_code = 201
        logging.info('LOGOUT: '+Student_id+' logged out.')
    else:
        response.status_code = 201
        response.data = script.get_token_json(Student_id)
        # DBに発行したトークンを保存
        cur.execute('update usr_table set token = \''+script.get_token(Student_id)+'\'where Student_id = \''+Student_id+'\'')
        logging.info('CARD LOADED: '+Student_id+' was touched.')
    
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
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    # POSTされたIDによってpasswardを引き出す
    cur.execute('select passwd, token from usr_table where Student_id = \'' +Student_id + '\'')
    response = Response()
    data = cur.fetchone()
    if len(data) == 0:
        response.status_code = 403
        conn.commit()
        cur.close()
        logging.info('UNEXPECTED ERROR: maybe DB error.(/pw_check)')
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
        response.status_code=201
        # DBのinout_stateを1に
        cur.execute('update usr_table set inout = 1 where Student_id = \''+Student_id+'\'')
        logging.info('LOGIN: '+Student_id+' loged in.')
    else:
        response.status_code = 403
        #logging.info('PWERROR: '+Student_id+' made a mistake in PW.')
   
    # DBの更新を保存&DBクローズ
    conn.commit()
    cur.close()
    return response

# DBの操作選択画面
@app.route('/db_operation' )
def db_ope_menu():
    return render_template('db_operation.html')
# DBの参照画面
@app.route('/db_operation/print')
def p_db():
    db.print_db()
    return render_template('print_db.html',array=db.array,count=db.rows)
# 部屋使用状況画面
@app.route('/room')
def room_status():
    inout_sum=db.count_inout()
    room_raito = inout_sum / capacity * 100
    return render_template('capacity.html',raito=int(room_raito))
# 部屋利用者画面


if __name__ == '__main__':
    db = DB_operation()
    logging.basicConfig(filename='login.log',level=logging.INFO,format='%(asctime)s %(message)s')
    with open('config.json','r') as f:
        config = json.load(f)
        database = config['DATABASE']
        capacity = config['capacity'] #ここでの宣言はグローバル変数扱い
    app.run(host='0.0.0.0',ssl_context=context, port=8443,debug=False)
