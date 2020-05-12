from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/<name>')
def logged_in(name):
    return render_template('login.html', name=name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
