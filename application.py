import flask
import os

from flask import request, jsonify
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, origins="*", allow_headers=["Content-Type", "Access-Control-Allow-Credentials"])

api = Api(app)
db = SQLAlchemy(app)

if __name__ == '__main__':
  app.run(host='0.0.0.0')