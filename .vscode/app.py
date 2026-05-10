from flask import Flask, render_template, request

app = Flask(__name__)

users = {
    "admin": "1234"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in users and users[username] == password:
        return "Login Successful"
    else:
        return "Invalid Credentials"

if __name__ == '__main__':
    app.run(debug=True)