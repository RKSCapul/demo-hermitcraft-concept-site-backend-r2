from application import db
from flask import jsonify

class users(db.Model):
  __table_args__ = { 'schema': 'hermits' }
  __tablename__ = 'user'

  hermit_code = db.Column(db.String(), primary_key=True)
  name = db.Column(db.String())
  username = db.Column(db.String())
  active = db.Column(db.Boolean)
  youtube_channel = db.Column(db.String())
  twitch_channel = db.Column(db.String())

  def __init__(self, username = ''):
    self.username = username

  def serialize(self):
    channels = {}
    channels['youtube'] = self.youtube_channel

    active = 'active'

    if self.twitch_channel:
      channels['twitch'] = self.twitch_channel

    if self.active == False:
      active = 'inactive'

    return {
      'name': self.name,
      'username': self.username,
      'status': active,
      'channel': channels
    }