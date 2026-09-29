from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime, timezone

app = Flask(__name__)
moment = Moment(app)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/user/<name>')
def user(name):
  return render_template('user.html', name=name, current_time=datetime.now(timezone.utc))

bootstrap = Bootstrap(app)

app.add_url_rule('/', 'index', index)


if __name__ == '__main__':
  app.run()