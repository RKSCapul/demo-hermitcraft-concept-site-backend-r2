import os
import sys

from requests import get

API_URL = 'https://api.twitch.tv/helix/streams?'

def getTwitchUserLogin(data):
  userLogins = ''

  for user in data:
    channel = user['channel']

    try:
      if userLogins == '':
        userLogins = 'user_login=' + channel['twitch']
      else:
        if not channel['twitch'] == '':
          userLogins = userLogins + '&user_login=' + channel['twitch']
    except:
      catcher = ''

  return userLogins

def fetchTwitchData(parameters):
  dataUrl = API_URL + parameters

  response = get(
    dataUrl, 
    headers = {
      'client-id': os.environ.get('TWITCH_API_CL'),
      'Authorization': 'Bearer ' + os.environ.get('TWITCH_API_AUTH'),
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  )

  returnData = response.json()
  return returnData['data']

def getUserData(channel, twitchData):
  try:
    for data in twitchData:
      if data['user_name'].lower() == channel['twitch'].lower():
        return data
  except:
    return 'no data'

  return 'no data'

def organizeTwitchChannelData(data, twitchData):
  channelData = []

  for user in data:
    channel = user['channel']
    userData = getUserData(channel, twitchData)
    
    isLiveOnTwitch = False
    livestreamLink = 'channel-is-not-live'

    if not userData == 'no data':
      isLiveOnTwitch = True
      livestreamLink = channel['twitch']

    if not "livestreams" in user:
      user['livestreams'] = {}

    liveData = {
      'isChannelLive': isLiveOnTwitch,
      'feed': livestreamLink
    }

    if not "twitch" in user['livestreams']:
      user['livestreams']['twitch'] = liveData
    
    channelData.insert(-1, user)

  return channelData  

def getTwitchDataAll(data):
  parameters = getTwitchUserLogin(data)
  twitchData = fetchTwitchData(parameters)

  return organizeTwitchChannelData(data, twitchData)

def getTwitchDataUser(data):
  dataArr = [ data ]

  if isinstance(data, (list)) == True:
    dataArr = data

  parameters = getTwitchUserLogin(dataArr)
  twitchData = fetchTwitchData(parameters)

  return organizeTwitchChannelData(dataArr, twitchData)