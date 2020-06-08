from flask import Flask, render_template, request, redirect, url_for, flash
from webapp.forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from webapp import *
import time
from system.interprocess_communication import Webapp2CoreMessages, Webapp2CoreKeys, Core2WebappKeys, Core2WebappMessages

from system.user import User


@app.route('/')
@app.route('/home')
def home():
    system_core_pipe.send({Webapp2CoreKeys.COMMAND: Webapp2CoreMessages.GET_DEVICES})
    try:
        devices = system_core_pipe.recv()
        while devices.get(Core2WebappKeys.TYPE) == Core2WebappMessages.DEV_RESPONSE:  #TUTAJ BUG, BO NIE UZYWAM GETA
            flash(devices[Core2WebappKeys.RESPONSE], 'info')
            devices = system_core_pipe()
        for dev in devices[Core2WebappKeys.DEVICES_LIST]:
            print('httpserver', dev)
    except:
        flash('Reload page', 'danger')
        devices[Core2WebappKeys.DEVICES_LIST] = []

    return render_template('index.html', title='Home', devices=devices[Core2WebappKeys.DEVICES_LIST])


@app.route('/dev/<dev_name>')
def dev(dev_name):
    system_core_pipe.send({Webapp2CoreKeys.COMMAND: Webapp2CoreMessages.DEV_SERVICES, Webapp2CoreKeys.DEV_NAME: dev_name})
    services = system_core_pipe.recv()
    while services[Core2WebappKeys.TYPE] != Core2WebappMessages.DEV_SERVICES:
        services = system_core_pipe.recv()
    if services[Core2WebappKeys.TYPE] == Core2WebappMessages.DEV_SERVICES:
        for service in services[Core2WebappKeys.SERVICES_LIST]:
            print('httpserver', service)
    return render_template('dev.html', title=dev_name, dev_name=dev_name, services=services[Core2WebappKeys.SERVICES_LIST])



@app.route('/dev/<dev_name>/<service>')
def run_service(dev_name, service):
    print('wysylam do ', dev_name, 'komende ', service)
    system_core_pipe.send({Webapp2CoreKeys.COMMAND: Webapp2CoreMessages.RUN_SERVICE, Webapp2CoreKeys.DEV_NAME: dev_name, Webapp2CoreKeys.SERVICE: service})
    print('Wyslalem')
    time.sleep(1)
    received = system_core_pipe.recv()
    if received[Core2WebappKeys.TYPE] == Core2WebappMessages.DEV_RESPONSE:
        flash(received[Core2WebappMessages.RESPONSE], 'info')

    return redirect(url_for('dev', dev_name=dev_name))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if received['command'] == 'registered' and received['status'] == 'success':
            hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        else:
            flash(f'Account not created - system failure', 'danger')
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        system_core_pipe.send({'command': Webapp2CoreMessages.LOGIN,
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
#    pipe.send('Proces zyje')
    app.run(debug=True, host='0.0.0.0')
#    pipe.send('Strona dziala')
    while True:
        if pipe.poll(1):
            rec = pipe.recv()


if __name__ == '__main__':
    main(None)
