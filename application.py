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

from controllers import hermits
from controllers import livestreams
from controllers import groups

api.add_resource(hermits.AllUsers, '/api/hermit/all')
api.add_resource(hermits.AllVideos, '/api/hermit/all/videos')
api.add_resource(hermits.Search, '/api/hermit/user/<string:_username>')
api.add_resource(hermits.Videos, '/api/hermit/user/<string:_username>/videos')

api.add_resource(livestreams.User, '/api/hermit/user/<string:_username>/live')
api.add_resource(livestreams.ActiveStatus, '/api/live/activehermits')

api.add_resource(livestreams.Schedule, '/api/live/schedules')
api.add_resource(livestreams.SlotStatus, '/api/live/status')

api.add_resource(groups.UserAssociations, '/api/hermit/user/<string:_username>/groups')

api.add_resource(groups.List, '/api/group/all')
api.add_resource(groups.Members, '/api/group/<string:_name>')

if __name__ == '__main__':
  app.run(host='0.0.0.0')