from flask import Flask, render_template,request,g,redirect,url_for
import json
import sys
from db import DB_operation

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('index_card_read'))

# ホーム画面
@app.route('/card_read')
@app.route('/card_read/<status>')
def index_card_read(status=None):
    if status != 'miss':
        return render_template('index.html')
    else:
        return render_template('index.html',status='miss')

# DB操作メニュー画面
@app.route('/db_operation', methods=['GET','POST'] )
def db_ope_menu():
    return render_template('db_operation.html');


# DBの表示
@app.route('/db_operation/print' ,methods=['GET','POST'])
def p_db(): 
    db.print_db() 
    return render_template('print_db.html',array=db.array,count=db.rows)


# DBにレコードを追加
@app.route('/db_operation/add',methods=['GET','POST'])
def add_operation():
    method = request.method
    if method == "GET":
        return render_template('add.html')
    else:
        db.db_add(request.form['Student_id'],request.form['passwd'])
        return redirect(url_for('db_ope_menu'))


# DBのレコード(パスワード)の更新
@app.route('/db_operation/update',methods=['GET','POST'])
def update_operation():
    method = request.method
    if method == "GET":
        return render_template('update.html')
    else:
        db.db_update(request.form['Student_id'],request.form['passwd'])
        return redirect(url_for('db_ope_menu'))


# DBのレコード削除
@app.route('/db_operation/drop',methods=['GET','POST'])
def drop_oprarion():
    method = request.method
    if method == "GET":
        return render_template('drop.html')
    else:
        db.db_drop(request.form['Student_id'])
        return redirect(url_for('db_ope_menu'))

# ログイン処理等
@app.route('/login', methods=['GET','POST'] )
@app.route('/login/<status>', methods=['GET','POST'])
def login(status=None):
    if request.method == 'GET':
        return redirect(url_for('index_card_read'))
    else:
        db.user_state(request.form['Student_id'],2)
        if db.usr_state == 1:
            db.logout(request.form['Student_id'])
            return render_template('logout.html')
        db.ID_check(request.form['Student_id'])
        if db.ID_exist == False: #IDミス
            return redirect(url_for('index_card_read',status = "miss"))
        else:
            return render_template('login.html', Student_id=request.form['Student_id'] )

# ログイン処理の結果
@app.route('/login/result', methods=['GET','POST'] )
@app.route('/login/lesult/<status>', methods=['GET','POST'])
def logined():
    if request.method == 'GET':
        return redirect(url_for('index_card_read'))
    else:
        db.login(db.Student_id,request.form['passwd'])
        if db.passwd == False:
            return render_template('login.html', Student_id=db.Student_id,status='miss')
        else:
            return render_template('logined.html', Student_id=db.Student_id )

# エラったとき用らしいけど現状使えない
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        print('closed DB')

if __name__ == '__main__':
    db = DB_operation()
   #  app.debug = True
    app.run(host='0.0.0.0', port=5000,debug=True)
