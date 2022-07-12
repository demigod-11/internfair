# from models.User import db
from controllers.UserController import register
from controllers.midware import *
from flask import Flask, jsonify, request, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_object('config')
api = Api(app)
db.init_app(app)
migrate = Migrate(app, db)

api.add_resource(register,'/')
if __name__ == '__main__':
    app.run(debug=True)