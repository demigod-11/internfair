from flask_restful import abort
from flask import  request, Response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from models.User import users
import json
import hashlib
import datetime
import jwt

db = SQLAlchemy()

class error_handlers():

    def abort_wrong_email(text):
        if '@' not in text:
            abort(400, message="Email is not valid")

    def abort_user_exist(text):
        if  db.session.query(users.email).filter_by(email=text).first() is not None:
            abort(400, message="User already exists")

    def abort_password_dont_match(text_1, text_2):

        if text_1 != text_2:
            abort(400, message="Password doesn't match")


class security_handlers():

    def harsh_password(text):
        return hashlib.pbkdf2_hmac('sha256', text.encode(), b'SECRET', 100000).hex()

    def create_token(id):
        token = jwt.encode({ 'id' : id, 'exp': datetime.datetime.now() + datetime.timedelta(seconds=600)}, b'SECRET_KEY', algorithm='HS256')
        return token

    def check_for_token(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            auth = request.headers.get('authorization')
            if not auth:
                return Response(json.dumps({'message': 'no token'}), status = 400)
            
            token = auth.split(' ')[1]
            try:
                data = jwt.decode(token, b'SECRET_KEY', algorithms=['HS256'])
                setattr(request, 'data', data)
            except:
                return Response(json.dumps({'message': 'Invalid token'}), status = 403)
            return func(*args, **kwargs)
        return wrapped
    