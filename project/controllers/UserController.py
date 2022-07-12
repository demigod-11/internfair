import sys
from models.User import users
from flask import render_template, redirect, url_for, request, Response
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from controllers.midware import error_handlers as e
from controllers.midware import handlers as h
from flask_mail import Message
from flask import current_app


db = SQLAlchemy()

user_details = reqparse.RequestParser()
user_details.add_argument("email", type=str, help="Input user email", required=True)
user_details.add_argument("password", type=str, help="Input user password", required=True)
user_details.add_argument("confirm_password", type=str, help="Confirm User password", required=True)



class register(Resource):

    def post(self):
        args = user_details.parse_args()
        e.abort_wrong_email(args.email)
        # e.abort_user_exist(args.email)
        e.abort_password_dont_match(args.password, args.confirm_password)
        token = h.create_token(args.email) 
        # detoken = h.decode_email_token(token) 
        args.password = h.harsh_password(args.password)
        # this = users(args.email, args.password)
        # db.session.add(this)
        # db.session.commit()
        msg = h.mail_settings(current_app.config["MAIL_USERNAME"],current_app.config["MAIL_PASSWORD"],token,address=[args.email])

        return msg

    def get(self):
        print(current_app.config["MAIL_PORT"])
        # msg = Message("Hello",
        #           sender="llousvamel11@gmail.com",
        #           recipients=["atumasaake@gmail.com"])

        
        # mail.send(msg)
        return 201


# class mail_confirm(Resource):

#     def get(self, token):
#         email = s.decode_email_token(token)
#         db = sql.connect(user_database)
#         cur = db.cursor()
        
#         user = User()
#         user_exists = user.email_exists(email)
#         if user_exists:
#             user.update_email(email)      
#         else:
#             return 'Email not found. Please try again'           
#         return 'Email confirmation successful'

# class login(Resource):

#     def post(self):
#         args = user_details.parse_args()
#         e.abort_wrong_email(args.email)
#         e.abort_user_exist(args.email)
#         e.abort_password_dont_match(args.password, args.confirm_password)
#         args.password = s.harsh_password(args.password)
#         this = users(args.email, args.password)
#         db.session.add(this)
#         db.session.commit()
#         return 201

#     def get(self):
#         return "Hello World"