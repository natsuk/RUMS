import sqlite3

DATABASE = 'DB/usr.db'
TABLE = 'usr_table'

class DB_init():
    def connect_db(self):
        self.connect = sqlite3.connect(DATABASE)
        self.cur = self.connect.cursor()

    def close_db(self):
        self.cur.close()


class DB_operation(DB_init):
    # print用のリストを渡す
    def print_db(self):
        self.connect_db()
        self.array=[]
        self.rows = 0
        for row in self.cur.execute('select * from '+TABLE+' order by Student_id'):
            self.array.append(row)
            self.rows += 1
        print(self.array)
        self.close_db()
   
    # レコードの追加 
    def db_add(self,Student_id,passwd):
        self.connect_db()
        self.cur.execute('insert into '+ TABLE + ' values(\''+Student_id+'\',\''+passwd+'\',0)')
        self.connect.commit()
        self.close_db()

    # レコードの更新(パスワード)
    def db_update(self,Student_id,passwd):
        self.connect_db()
        self.cur.execute('update '+TABLE+' set passwd = \'' +passwd+ '\' where Student_id = \''+Student_id+'\'')
        self.connect.commit()
        self.close_db()
    
    # レコードの削除
    def db_drop(self,Student_id):
        self.connect_db()
        self.cur.execute('delete from '+TABLE+' where Student_id = \'' +Student_id+ '\'')
        self.connect.commit()
        self.close_db()

    # ユーザーのログイン状態を取得、変更
    def user_state(self,Student_id,task):
        self.connect_db()
        if task == 2:
            self.cur.execute('select inout from '+TABLE+' where Student_id = \'' +Student_id+ '\'')
            temp=self.cur.fetchone()
            self.usr_state=temp[0]
        elif task == 0:
            self.cur.execute('update '+TABLE+' set inout = 0 where Student_id = \''+Student_id+'\'')
            self.connect.commit()
        elif task == 1:
            self.cur.execute('update '+TABLE+' set inout = 1 where Student_id = \''+Student_id+'\'')
            self.connect.commit()
        self.close_db()

    # IDの有無よみとり
    def ID_check(self,Student_id):
        self.connect_db()
        self.cur.execute('select Student_id from '+TABLE+' where Student_id = \'' +Student_id+ '\'')
        S_id=self.cur.fetchone()
        if S_id == None:
            self.ID_exist = False
        elif S_id[0] == Student_id:
            self.Student_id = S_id[0]
            self.ID_exist = True
        else:
            self.ID_exist = False  
        self.close_db()
    
    # ログイン用
    def login(self,Student_id,passwd):
        self.connect_db()
        print(Student_id)
        self.cur.execute('select Student_id,passwd from '+TABLE+' where Student_id = \'' +Student_id+ '\'')
        usrinfo = self.cur.fetchone()
        if usrinfo == None:
            self.passwd = False
        elif usrinfo[1] == passwd:
            self.passwd = True
            self.user_state(Student_id,1)
        else:
            self.passwd = False
        self.close_db()
    # ログアウト用
    def logout(self,Student_id):
        self.connect_db()
        self.user_state(Student_id,0)
        self.close_db()

