import sys, os
sys.path.append(os.path.abspath('.')) 
from config import db

class User(db.Model):
    # o nome do campo 'id' é diferente no banco de dados
    id = db.Column('user_id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(100), nullable=False)
        
    # def __repr__(self):
    #     return f'''
    #     id = {self.id}
    #     email = {self.email}
    #     nome = {self.name}
    #     birthdate = {self.birthdate}
    #     password = {self.password}
    #     '''