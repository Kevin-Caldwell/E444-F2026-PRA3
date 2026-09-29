from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from datetime import datetime, timezone
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'toodalooo'
bootstrap = Bootstrap(app)
moment = Moment(app)

def validate_phrase(phrase):
    def _validator(form, field):
        if phrase.lower() not in field.data.lower():
            raise ValidationError(f"Email must contain the phrase '{phrase}'.")
    return _validator

class NameForm(FlaskForm):
  name = StringField("What is your name?", validators=[DataRequired()])
  email = StringField("What is your email?", validators=[DataRequired(), Email(message="Please include an '@' and a valid domain") ,validate_phrase("utoronto")])
  submit = SubmitField("Submit")

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():

        old_name = session.get('name')
        old_email = session.get('email')

        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')

        session['name'] = form.name.data
        session['email'] = form.email.data

        return redirect(url_for('index'))

    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',
                           name=name,
                           current_time=datetime.now(timezone.utc))