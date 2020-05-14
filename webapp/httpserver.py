from flask import Flask, render_template, request, redirect, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)


app.config['SECRET_KEY'] = 'afaa73978854986497574dcae8357ba7'


def valid_login(username, password):
    if username == 'Adrian' and password == 'kij':
        return True
    return False


def log_user_in(username):
    return app.route('login/username');


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
