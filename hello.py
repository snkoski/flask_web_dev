from datetime import datetime
from flask import Flask, request, make_response, redirect, abort, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=session.get('name'))

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
