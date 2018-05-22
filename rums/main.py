import sqlite3
from flask import Flask, render_template,request,g,redirect,url_for
import json
import sys

app = Flask(__name__)

DATABASE = 'DB/usr.db'
TABLE = 'usr_table'


# データベースを取得するため
def get_db():
    conect = sqlite3.connect(DATABASE)
    cur=conect.cursor()
    db={'conect':conect,'cursor':cur}
    return db

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
        return render_template('index.html',status='Miss')

# DB操作メニュー画面
@app.route('/db_operation', methods=['GET','POST'] )
def db_ope_menu():
    return render_template('db_operation.html');


# DBの表示
@app.route('/db_operation/print' ,methods=['GET','POST'])
def p_db(): 
    ret = print_db()
    return render_template('print_db.html',array=ret['array'],count=ret['count'])

def print_db():
    db = get_db();
    array = [];
    count = 0;
    for row in db['cursor'].execute('select * from '+TABLE+' order by Student_id'):
        array.append(row)
        count+=1
    db['cursor'].close()
    ret={'array':array,'count':count}
    return ret    


# DBにレコードを追加
@app.route('/db_operation/add',methods=['GET','POST'])
def add_operation():
    method = request.method
    if method == "GET":
        return render_template('add.html')
    else:
        db = get_db()
        Student_id=request.form['Student_id']
        passwd=request.form['passwd']
        db['cursor'].execute('insert into '+ TABLE + ' values(\''+Student_id+'\',\''+passwd+'\',0)')
        db['conect'].commit()
        db['cursor'].close()
        return redirect(url_for('db_ope_menu'))


# DBのレコード(パスワード)の更新
@app.route('/db_operation/update',methods=['GET','POST'])
def update_operation():
    method = request.method
    if method == "GET":
        return render_template('update.html')
    else:
        db = get_db()
        Student_id=request.form['Student_id']
        passwd=request.form['passwd']
        db['cursor'].execute('update '+TABLE+' set passwd = \'' +passwd+ '\' where Student_id = \''+Student_id+'\'')
        db['conect'].commit()
        db['cursor'].close()
        return redirect(url_for('db_ope_menu'))


# DBのレコード削除
@app.route('/db_operation/drop',methods=['GET','POST'])
def drop_oprarion():
    method = request.method
    if method == "GET":
        return render_template('drop.html')
    else:
        db = get_db()
        Student_id=request.form['Student_id']
        db['cursor'].execute('delete from '+TABLE+' where Student_id = \'' +Student_id+ '\'')
        db['conect'].commit()
        db['cursor'].close()
        return redirect(url_for('db_ope_menu'))


@app.route('/login', methods=['GET','POST'] )
def login():
    method = request.method
    if method == 'GET':
        return redirect(url_for('index_card_read'))
    else:
        # パスワード入力
        try:
            Student_id=request.form['Student_id']
            db = get_db()
            db['cursor'].execute('select Student_id from '+TABLE+' where Student_id = \'' +Student_id+ '\'')
            if db['cursor'].fetchone() == None:
                db['cursor'].close()
                return redirect(url_for('index_card_read',status = "miss"))
            db['cursor'].close()
            return render_template('login.html', Student_id=Student_id)
        except:
        # パスワード認証
            try:
                passwd = request.form['passwd']
                db=get_db()
                db['cursor'].close()
                return render_template('auth_test.html')
            except:
                sys.exit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        print('closed DB')
if __name__ == '__main__':
   #  app.debug = True
    app.run(host='0.0.0.0', port=5000,debug=True)
