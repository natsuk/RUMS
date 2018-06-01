import cgi
from flask import Flask,request

app = Flask(__name__)

@app.route('/test',methods=['POST'])
def test():
    Student_id = request.form['card_id']
    print (Student_id)
    return Student_id

if __name__ == '__main__':
    app.debug = True
    app.run(host='00.00.00.00', port=8080)

