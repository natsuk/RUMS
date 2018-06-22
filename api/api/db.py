import sqlite3

DATABASE = 'usr.db'
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
        self.close_db()

    def count_inout(self):
        self.connect_db()
        self.cur.execute('select sum(inout) from usr_table')
        ret=self.cur.fetchone()
        self.close_db()
        return ret[0]   
