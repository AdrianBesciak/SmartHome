from typing import Type

from flask import Flask, render_template, request, redirect, url_for, flash
from webapp.forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from system.user import User

app = Flask(__name__)

system_core_pipe = None

app.config['SECRET_KEY'] = 'afaa73978854986497574dcae8357ba7'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    user_dict = User.db.get('email', user_id)
    if user_dict is not None:
        return User(user_dict['username'], user_dict['email'], user_dict['password'], user_dict['privileges'])
    else:
        return None
