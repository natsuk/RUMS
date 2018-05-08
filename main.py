import sqlite3
from flask import Flask, render_template,request,g,redirect

app = Flask(__name__)

DATABASE = 'DB/db_sample.db'

# データベースを取得
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# レコードの追加

# レコードの削除

# レコードの変更

# テーブルの表示


@app.route('/')
def index():
    # return 'Hello'
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'] )
def login():
    # request.method
    Student_id=request.form['Student_id']
    print(Student_id)
    return render_template('login.html', Student_id=Student_id)

@app.route('/login/auth', methods=['POST'])
def auth():
    print("/login/auth")
    db=get_db()
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
