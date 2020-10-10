from application import db
from flask import jsonify

class groups(db.Model):
  __table_args__ = { 'schema': 'hermits' }
  __tablename__ = 'groups_'

  group_code = db.Column(db.String(), primary_key=True)
  name = db.Column(db.String())
  group_duration = db.Column(db.String())

  def __init__(self, name = ''):
    self.name = name

  def serialize(self):
    return {
      'name': self.name,
      'duration': self.group_duration
    }

class group_members(db.Model):
  __table_args__ = { 'schema': 'hermits' }
  __tablename__ = 'groups_view'

  id = db.Column(db.String(), primary_key = True)
  group = db.Column(db.String())
  group_duration = db.Column(db.String())
  username = db.Column(db.String())
  member = db.Column(db.String())
  active = db.Column(db.Boolean)

  def serializeMembers(self):
    return {
      'member': self.member,
      'active': self.active
    }

  def serializeGroups(self):
    return {
      'name': self.group,
      'duration': self.group_duration
    }