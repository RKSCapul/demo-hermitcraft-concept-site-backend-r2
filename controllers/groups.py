import data
import urllib

from flask_restful import Resource, abort
from flask import jsonify

from data import groups
from data import group_members

class List(Resource):
  def get(self):
    _groups = groups()

    data = _groups.query.order_by(_groups.group_duration).all()
    groupsData = [e.serialize() for e in data]

    return groupsData

class Members(Resource):
  def get(self, _name): 
    _group_members = group_members()
    _groups = groups()

    groupData = _groups.query.filter_by(name = _name).first();
    group = groupData.serialize()

    data = _group_members.query.filter_by(group = _name).all()
    tmpMembers = [e.serializeMembers() for e in data]

    group["members"] = tmpMembers

    return group

class UserAssociations(Resource):
  def get (self, _username):
    _group_members = group_members()

    data = _group_members.query.filter_by(username = _username).all()
    associatedGroups = [e.serializeGroups() for e in data]

    return associatedGroups