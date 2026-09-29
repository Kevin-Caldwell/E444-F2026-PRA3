import re
from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
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

        return redirect(url_for('chat_page'))

    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',
                           name=name,
                           current_time=datetime.now(timezone.utc))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    msg_lower = message.lower()

    if 'chat_memory' not in session:
        session['chat_memory'] = {}

    memory = session['chat_memory']

    # 1. Detect user introducing their name (e.g., "My name is Alice")
    name_match = re.search(r'my name is\s+([a-zA-Z]+)', message, re.IGNORECASE)

    if name_match:
        extracted_name = name_match.group(1).capitalize()
        memory['user_name'] = extracted_name
        session.modified = True
        reply = f'Nice to meet you, {extracted_name}!'

    elif 'what is my name' in msg_lower or 'what\'s my name' in msg_lower:
        if 'user_name' in memory:
            reply = f"I know you! Your name is {memory['user_name']}."
        else:
            reply = "I'm not sure. You can tell me by saying 'My name is [Name]'."

    elif 'hello' in msg_lower or 'hi' in msg_lower:
        reply = 'Hello!'

    else:
        reply = "Ask me what your name is."

    return ({'reply': reply})

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out and memory cleared.')
    return redirect(url_for('index'))


@app.route('/chat_page')
def chat_page():
    if not session.get('name') or not session.get('email'):
        flash('Please submit your name and UofT email first.')
        return redirect(url_for('index'))

    return render_template(
        'chat.html', name=session.get('name'), email=session.get('email')
    )