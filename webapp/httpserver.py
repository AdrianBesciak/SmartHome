from flask import Flask, render_template, request, redirect, url_for, flash
from webapp.forms import RegistrationForm, LoginForm

app = Flask(__name__)

system_core_pipe = None

app.config['SECRET_KEY'] = 'afaa73978854986497574dcae8357ba7'


def valid_login(username, password):
    if username == 'Adrian' and password == 'kij':
        return True
    return False


def log_user_in(username):
    return app.route('login/username');


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        system_core_pipe.send({'command': 'register',
                               'username': form.username.data,
                               'email': form.email.data,
                               'password': form.password.data
                               })
        received = system_core_pipe.recv()
        if received['command'] == 'registered' and received['status'] == 'success':
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'Account not created - system failure', 'danger')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        system_core_pipe.send({'command': 'login',
                               'email': form.email.data,
                               'password': form.password.data
                               })
        received = system_core_pipe.recv()
        if received['command'] == 'registered' and received['status'] == 'success':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccesfull. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


def main(pipe):
    global system_core_pipe
    system_core_pipe = pipe
    pipe.send('Proces zyje')
    app.run(debug=True, host='0.0.0.0')
    pipe.send('Strona dziala')
    while True:
        if pipe.poll(1):
            rec = pipe.recv()


if __name__ == '__main__':
    main(None)
