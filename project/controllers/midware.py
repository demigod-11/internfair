from flask_restful import abort
from flask import  request, Response, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message
from functools import wraps
from models.User import users
from models.User import db
import json
import hashlib
import datetime
import jwt
import smtplib




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


class handlers():

    def harsh_password(text):
        return hashlib.pbkdf2_hmac('sha256', text.encode(), b'SECRET', 100000).hex()

    def create_token(id):
        token = jwt.encode({ 'id' : id, 'exp': datetime.datetime.now() + datetime.timedelta(seconds=600)}, b'SECRET_KEY', algorithm='HS256')
        return token


    def decode_email_token(id):
        token = jwt.decode(id, b'SECRET_KEY', algorithms=['HS256'])
        return token


    def mail_settings(user, password,link, address=[]):
        
        print(type(user), type(password), link, address)
        smtp_host = 'smtp.gmail.com'
        smtp_starttls = True
        smtp_ssl = False
        smtp_user = user
        smtp_password = password 
        smtp_port = 587
        smtp_mail_from = user

        toaddrs = address
        message_text = f"""
        Click on this {request.base_url}/activate/{link} to activate your account
        """
        print(message_text)

        subject = 'Verify your Account'
        msg = (
            "Subject: %s\r\nFrom: %s\r\nTo: %s\r\n\r\n%s"
            % (
                subject, smtp_mail_from,
                ", ".join(toaddrs),
                message_text)
            )

        try:
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.set_debuglevel(1)
            if smtp_starttls:
                server.starttls()
            server.login(smtp_user, smtp_password)

            server.sendmail(smtp_mail_from, toaddrs, msg)
            server.quit()
            return "Message Sent"
        except Exception as e:
            file = open('errorMails.txt', mode='a+')
            file.write(f'email validation link not sent to {address[0]} \n')
            file.close()
            return "Message not Sent"
        


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
    