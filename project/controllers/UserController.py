import sys
from models.User import users
from flask import render_template, redirect, url_for, request
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from controllers.midware import error_handlers as e
from controllers.midware import security_handlers as s


db = SQLAlchemy()


user_details = reqparse.RequestParser()
user_details.add_argument("email", type=str, help="Input user email", required=True)
user_details.add_argument("password", type=str, help="Input user password", required=True)
user_details.add_argument("confirm_password", type=str, help="Confirm User password", required=True)



class register(Resource):

    def post(self):
        args = user_details.parse_args()
        e.abort_wrong_email(args.email)
        e.abort_user_exist(args.email)
        e.abort_password_dont_match(args.password, args.confirm_password)
        args.password = s.harsh_password(args.password)
        this = users(args.email, args.password)
        db.session.add(this)
        db.session.commit()
        return 201

    def get(self):
        return "Hello World"