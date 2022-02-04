from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "Shh SHhh Shh"
app.config.from_pyfile('configuration.py')

DATABASE = "mailing_list_db"

bcrypt = Bcrypt(app)