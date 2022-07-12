from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(120))
    activated = db.Column(db.Integer)
    

    def __init__(self, email, password, activated=0):
        self.email = email
        self.password = password
        self.activated = activated

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'address': self.password,
            'activated': self.activated    
        }
