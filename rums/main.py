import sqlite3
from flask import Flask, render_template,request,g,redirect,url_for
import json

app = Flask(__name__)

DATABASE = 'DB/usr.db'
TABLE = 'usr_table'

# DBdata = {'Student_id':None,'passwd':None,'inout':None}

# データベースを取得するため
def get_db():
    # db = getattr(g, '_database', None)
    conect = sqlite3.connect(DATABASE)
    cur=conect.cursor()
    db={'conect':conect,'cursor':cur}
    # if db is None:
    #   db = g._database = sqlite3.connect(DATABASE)
    return db
#def conect_db():
#    conect = sqlite3.connect(DATABASE)
#    return conect

# レコードの削除
def drop_db( DBdata ):
    print("a")
# レコードの変更
def change_db( DBdata ):
    print("a")


@app.route('/')
def index():
    # return 'Hello'
    return render_template('index.html')

# DB操作メニュー画面
@app.route('/db_operation', methods=['GET','POST'] )
def db_ope_menu():
    print('db_operation menu')
    return render_template('db_operation.html');


# DBの表示
@app.route('/db_operation/print' ,methods=['GET','POST'])#,POST']  )
def p_db(): 
    # print Database
    print('/db_operation/print') 
    ret = print_db()
    print(type(ret['count']))
    print(ret['count'])
    return render_template('print_db.html',array=ret['array'],count=ret['count'])

def print_db():
    db = get_db();
    array = [];
    count = 0;
    for row in db['cursor'].execute('select * from '+TABLE+' order by Student_id'):
        array.append(row)
        count+=1
        print(row)
    db['cursor'].close()
    ret={'array':array,'count':count}
    return ret    


# DBにレコードを追加
@app.route('/db_operation/add',methods=['POST'])
def add_operation():
    print('add_operation')
    return render_template('add.html')
    
@app.route('/db_operation/add/do',methods=['POST'])    
def add_do():
    print('input_db')
    db = get_db()
    Student_id=request.form['Student_id']
    passwd=request.form['passwd']
    print(type(Student_id))
    print(type(passwd))
    db['cursor'].execute('insert into '+ TABLE + ' values(\''+Student_id+'\',\''+passwd+'\',0)')
#   conect=conect_db()
    db['conect'].commit()
    db['cursor'].close()
#   conect.close()
    print('insert_table')
    return redirect(url_for('db_ope_menu'))


# DBのレコード(パスワード)の更新
@app.route('/db_operation/update',methods=['POST'])
def update_operation():
    print('update_operayion')
    return render_template('update.html')

@app.route('/db_operation/update/do',methods=['POST'])
def update_do():
    print('update_do')
    db = get_db()
    Student_id=request.form['Student_id']
    passwd=request.form['passwd']
    db['cursor'].execute('update '+TABLE+' set passwd = \'' +passwd+ '\' where Student_id = \''+Student_id+'\'')
    db['conect'].commit()
    db['cursor'].close()
    print('update_record')
    return redirect(url_for('db_ope_menu'))


# DBのレコード削除
@app.route('/db_operation/drop',methods=['POST'])
def drop_oprarion():
    print('drop_operation')
    return render_template('drop.html')

@app.route('/db_operation/drop/do',methods=['POST'] ) 
def drop_do():
    db = get_db()
    Student_id=request.form['Student_id']
    db['cursor'].execute('delete from '+TABLE+' where Student_id = \'' +Student_id+ '\'')
    db['conect'].commit()
    db['cursor'].close()
    print('drop_record')
    return redirect(url_for('db_ope_menu'))


@app.route('/login', methods=['POST'] )
def login():
    # request.method
    Student_id=request.form['Student_id']
    print(Student_id)
    return render_template('login.html', Student_id=Student_id)

@app.route('/login/auth', methods=['POST'])
def auth():
    print("/login/auth")
    db=get_db()
    db['cursor'].close()
    #print(g)
    # return redirect('/login')
    return render_template('auth_test.html')

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        print('closed DB')
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
