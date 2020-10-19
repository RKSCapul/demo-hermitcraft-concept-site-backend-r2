from application import db
from flask import jsonify

class socials(db.Model):
  __table_args__ = { 'schema': 'hermits' }
  __tablename__ = 'socials'

  id = db.Column(db.Integer, primary_key=True)
  hermit_code = db.Column(db.String())
  account = db.Column(db.String())
  title = db.Column(db.String())
  url = db.Column(db.String())

  def __init__(self, hermit_code = ''):
    self.hermit_code = hermit_code

  def serialize(self):
    return {
      'id': self.id,
      'hermitCode': self.hermit_code,
      'account': self.account,
      'title': self.title,
      'url': self.url
    }
    