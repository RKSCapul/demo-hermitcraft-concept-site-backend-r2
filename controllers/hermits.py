import data

from flask_restful import Resource, abort

from webapi import getYouTubeChannelDataAll
from webapi import getYouTubeChannelDataUser
from webapi import getYouTubeChannelVideos

from data import users

class AllUsers(Resource):
  def get(self):
    _users = users()
    
    data = _users.query.order_by(_users.name).all()

    hermitData = [e.serialize() for e in data]

    youTubeData = getYouTubeChannelDataAll(hermitData)

    organizedData = sorted(youTubeData, key=lambda k: k['name'].lower())
    return organizedData

class Search(Resource):
  def get(self, _username):
    _users = users()
    
    data = _users.query.filter_by(username=_username).first()
    hermitData = data.serialize()

    if hermitData:
      youtubeChannelData = getYouTubeChannelDataUser(hermitData)
      
      return youtubeChannelData
    else:
      abort(404, message='User not found in database')

class Videos(Resource):
  def get(self, _username):
    _users = users()
    
    data = _users.query.filter_by(username=_username).first()
    youtubeChannel = data.serializeYouTubeChannel()

    return getYouTubeChannelVideos(youtubeChannel)