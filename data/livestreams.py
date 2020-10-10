from application import db
from flask import jsonify
from datetime import datetime, timedelta

class lists(db.Model):
  __table_args__ = { 'schema': 'livestreams' }
  __tablename__ = 'list'

  livestream_code = db.Column(db.String(), primary_key=True)
  title = db.Column(db.String())
  date = db.Column(db.String())
  completed = db.Column(db.Boolean())
  ongoing = db.Column(db.Boolean())

  def serialize(self):
    return {
      'livestreamCode': self.livestream_code,
      'title': self.title,
      'date': self.date,
      'ongoing': self.ongoing,
    }

class schedule(db.Model):
  # Table data #
  __table_args__ = { 'schema': 'livestreams' }
  __tablename__ = 'schedule_view'

  # Columns #
  schedule_id = db.Column(db.String(), primary_key=True)
  livestream_code = db.Column(db.String())
  hermit_code = db.Column(db.String())
  member = db.Column(db.String())
  youtube_channel = db.Column(db.String())
  twitch_channel = db.Column(db.String())
  date = db.Column(db.String())
  start_time_utc = db.Column(db.String())
  end_time_utc = db.Column(db.String())
  platform = db.Column(db.String())

  # Variables #
  dateFormat = '%Y-%m-%d'
  date_ = -1
  prevHour = -1

  def constructISOTime(self, date, time):
    hour = time.split(":")[0]

    # Initialize
    if (self.prevHour == -1 and self.date_ == -1):
      self.prevHour = int(hour)
      self.date_ = self.date

    # Adjust date by one day when previous hour < current hour.
    if int(hour) < self.prevHour:
      self.date_ = datetime.strptime(self.date_, self.dateFormat).date() + timedelta(days=1)

    self.prevHour = int(hour)

    return str(self.date_) + 'T' + time + '+00:00'

  def serializeWithId(self, lastRecordedDate_):
    self.date_ = lastRecordedDate_

    return {
      'results': {
        'livestreamCode': self.livestream_code,
        'hermitCode': self.hermit_code,
        'member': self.member,
        'startTimeUTC': self.constructISOTime(self.date_, self.start_time_utc),
        'endTimeUTC': self.constructISOTime(self.date_, self.end_time_utc),
        'platform': self.platform,
        'channel': {
          'twitch': self.twitch_channel,
          'youtube': self.youtube_channel
        }
      },
      'lastRecordedDate': str(self.date_)
    }

  def serialize(self, lastRecordedDate_):
    self.date_ = lastRecordedDate_

    return {
      'results': {
        'hermitCode': self.hermit_code,
        'member': self.member,
        'startTimeUTC': self.constructISOTime(self.date_, self.start_time_utc),
        'endTimeUTC': self.constructISOTime(self.date_, self.end_time_utc),
        'platform': self.platform,
        'channel': {
          'twitch': self.twitch_channel,
          'youtube': self.youtube_channel
        }
      },
      'lastRecordedDate': str(self.date_),
    }

  def serializeStatus(self):
    return {
      'hermitCode': self.hermit_code,
      'channel': {
        'twitch': self.twitch_channel,
        'youtube': self.youtube_channel
      }
    }