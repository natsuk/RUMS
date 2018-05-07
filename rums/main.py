from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
def index():
    # return 'Hello'
    return render_template('index.html')

@app.route('/login', methods=['POST'] )
def login():
    # request.method
    return render_template('login.html')

@app.route('/login/auth', methods=['GET'])
def auth():
    print("/login/auth")

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
