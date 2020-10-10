import data

from flask_restful import Resource

from webapi import getYouTubeChannelDataAll

from data import users

class AllUsers(Resource):
  def get(self):
    _users = users()
    
    data = _users.query.order_by(_users.name).all()

    hermitData = [e.serialize() for e in data]

    youTubeData = getYouTubeChannelDataAll(hermitData)

    organizedData = sorted(youTubeData, key=lambda k: k['name'].lower())
    return organizedData