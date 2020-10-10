import data
import urllib

from datetime import datetime, timezone

from flask_restful import Resource, abort
from flask import jsonify

from data import lists
from data import schedule
from data import users

from webapi import getYouTubeAccountPictureAll
from webapi import getTwitchDataAll
from webapi import getTwitchDataUser

class Schedule(Resource):
  previousDate = -1

  def serialize(self, e):
    data = e.serialize(self.previousDate)

    self.previousDate = data['lastRecordedDate']

    return data['results']

  def get(self):
    _lists = lists()
    _schedule = schedule()

    data = _lists.query.order_by(_lists.livestream_code).filter_by(completed = False).all()
    listData = [e.serialize() for e in data]

    livestreamScheduleData = []

    for item in data:
      scheduleData = _schedule.query.filter_by(livestream_code = item.livestream_code).order_by(_schedule.schedule_id).all()

      serializedSchedule = []
      for e in scheduleData:
        serializedSchedule.insert(len(serializedSchedule), self.serialize(e))

      # Data stored in variable will include account pictures obtained from YouTube API.
      scheduleWithYouTubeData = getYouTubeAccountPictureAll(serializedSchedule)

      # Data stored in variable will be the livestream in order by startTimeUTC.
      organizedSchedule = sorted(scheduleWithYouTubeData, key=lambda k: k['startTimeUTC'])

      scheduleGroup = {
        'livestreamCode': item.livestream_code,
        'title': item.title,
        'date': item.date,
        'ongoing': item.ongoing,
        'schedule': organizedSchedule
      }

      livestreamScheduleData.insert(-1, scheduleGroup) 
      self.previousDate = -1

    organizedData = sorted(livestreamScheduleData, key=lambda k: datetime.strptime(k['date'], '%Y-%m-%d'))

    return organizedData

class SlotStatus(Resource):
  def get(self):
    _lists = lists()
    _schedule = schedule()

    data = _lists.query.filter_by(ongoing = True).all()
    listData = [e.serialize() for e in data]

    livestreamScheduleData = {}

    for item in data:
      scheduleData = _schedule.query.filter_by(livestream_code = item.livestream_code).all()
      serializedSchedule = [e.serializeStatus() for e in scheduleData]

      # Data stored in variable will include account pictures obtained from Twitch API.
      organizedSchedule = getTwitchDataAll(serializedSchedule)

      livestreamScheduleData[item.livestream_code] = organizedSchedule

    return livestreamScheduleData

class ActiveStatus(Resource):
  def get(self):
    _users = users();

    hermits = _users.query.filter_by(active = True).all()
    listHermits = [e.serializeChannels() for e in hermits]

    activeTwitchLivestreamStatus = getTwitchDataAll(listHermits)
    
    return activeTwitchLivestreamStatus

class User(Resource):
  def get(self, _username):
    _users = users()
    
    data = _users.query.filter_by(username=_username).first()
    hermitData = data.serializeChannels()

    if hermitData:
      twitchChannelLive = getTwitchDataUser(hermitData)
      
      return twitchChannelLive
    else:
      abort(404, message='User not found in database')

