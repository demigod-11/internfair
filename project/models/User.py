from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.email,
            'address': self.password
        }
