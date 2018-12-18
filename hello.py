from datetime import datetime
from flask import Flask, request, make_response, redirect, abort, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', temp_name=name)

@app.route('/browser')
def browser():
    user_agent = request.headers.get('User-Agent')
    return '<h1>Your browser is %s</h1>' % user_agent

@app.route('/cookie')
def cookie():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/red')
def red():
    return redirect('http://www.example.com')

@app.route('/abortuser/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name

@app.route('/filters')
def get_filters():
    phrase = "this is a phrase to test filters"
    lower = "lower"
    upper = "UPPER"
    return render_template('filters.html', phrase=phrase, lower=lower, upper=upper)

if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()
