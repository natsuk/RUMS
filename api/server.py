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
    Student_id = request.form['card_id']
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    id = cur.execute('select Student_id from usr_table where Student_id = \'' +Student_id+ '\'')
    response = Response()
    if len(cur.fetchall()) == 0:
        response.status_code = 403
    else:
        response.status_code = 201
        response.data = script.get_token_json(Student_id)
        cur.execute('update usr_table set token = \''+script.get_token(Student_id)+'\'where Student_id = \''+Student_id+'\'')
    
    conn.commit()
    cur.close()
    response.content_type = 'application/json'    
    return response

@app.route('/pw_check',methods=['POST'])
def pw_check():
    pw = request.form['passwd']
    print(pw)
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    id = cur.execute('select Student_id from usr_table where Student_id = \'' +session.get('id') + '\' and passwd = \''+ pw + '\'')
    response = Response()
    if len(cur.fetchall()) == 0 or len(cur.fetchall()) > 1:
        response.status_code = 403
    else:
        response.status_code = 201
        session['check'] = True
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
