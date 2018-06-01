import cgi
from flask import Flask,request

app = Flask(__name__)

@app.route('/id_serch',methods=['POST'])
def test():
    Student_id = request.form['card_id']
    print (Student_id)
    token = {"token":Student_id}
    return json.dumps(token)

@app.route('/pw_serch',methods=['POST'])
def test2():
    word = request.json['pass']
    #word = json.loads(passworrd)
    print(word)
    print("YAAA")
    res = {"stat":"OK"}
    return json.dumps(res)
if __name__ == '__main__':
    app.debug = True
    app.run(host='00.00.00.00', port=8080)

