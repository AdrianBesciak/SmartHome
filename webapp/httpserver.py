from flask import Flask, render_template, request


app = Flask(__name__)


def valid_login(username, password):
    if username == 'Adrian' and password == 'kij':
        return True
    return False


def log_user_in(username):
    return app.route('login/username');


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['pwd']):
            #return log_user_in(request.form['username'])
            print('Zalogowano')
            return render_template(logged_in, username=request.form['username'])
        else:
            print('Nie Zalogowano')
            error = 'Invalid username or password'
    print("Nie wiem co sie dzieje")
    return render_template('login.html', error=error)


@app.route('/login/<name>')
def logged_in(name):
    return render_template('loggedIn.html', name=name)


@app.route('/register')
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
