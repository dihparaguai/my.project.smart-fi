from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '@chave_secreta@'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB='mysql+mysqlconnector',
        usuario='root',
        senha='admin',
        servidor='localhost',
        database='smart_fi')

db = SQLAlchemy(app)