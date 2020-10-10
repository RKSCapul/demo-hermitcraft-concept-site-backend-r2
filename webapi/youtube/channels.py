import os

from requests import get

API_URL = 'https://www.googleapis.com/youtube/v3/'
CHANNEL_PART = "channels?part=statistics%2Csnippet%2CcontentDetails"
KEY = '&key=' + os.environ.get('YOUTUBE_API_CL')

def createEstimatedSubscriberCount(subChunks):
  subChunksLength = len(subChunks) - 1
  mainDigit = subChunks[0]
  minorDigit = ''
  suffix = ''

  if subChunksLength == 2:                      # 1+ million subscriblers
    suffix = 'M'
    minorLength = 2

    if subChunks[1][1] == '0':
      minorLength = 1

    minorDigit = '.' + subChunks[1][0:(minorLength)]
  elif subChunksLength == 1:                    # 1+ thousand subscribers
    suffix = 'K'

    if len(mainDigit) <= 2:                     # perform only if mainDigit is less than or equal to 2
      minorDigit = '.' + subChunks[1][0:1]
      
  output = ''.join([str(mainDigit), str(minorDigit), str(suffix)])
  
  return output

def getEstimatedSubscriberCount(subscriberCount):
  estimatedSubscriberCount = ''

  subCountLength = len(subscriberCount)
  subChunks = []

  while subCountLength != 0:
    index = 3
    chunk = ''

    if (subCountLength <= 3):
      index = subCountLength

    for x in range(subCountLength, (subCountLength - index), -1):
      _chunk = subscriberCount[x-1] + chunk
      chunk = _chunk
    
    subChunks.insert(0, chunk)
    subCountLength = subCountLength - index

  estimatedSubscriberCount = createEstimatedSubscriberCount(subChunks)

  return estimatedSubscriberCount

def getChannelData(channel, youtubeData):
  try:
    for data in youtubeData:
      if data['id'] == channel['youtube']:
        return data

  except:
    return 'no data'

def getYoutubeChannelID(data):
  channelIDs = ''

  for user in data:
    channel = user['channel']

    if channelIDs == '':
      channelIDs = '&id=' + channel['youtube']
    else:
      channelIDs = channelIDs + ',' + channel['youtube']

  return channelIDs

def fetchYouTubeChannelData(parameters):
  dataUrl = API_URL + CHANNEL_PART + KEY + parameters
  response = get(dataUrl)
  channels = response.json()

  return channels['items'] 

def organizeYouTubeChannelData(data, youtubeData):
  channelData = []

  for user in data:
    channel = user['channel']
    userData = getChannelData(channel, youtubeData)
    rawSubscriberCount = userData['statistics']['subscriberCount']

    estimatedSubscriberCount = getEstimatedSubscriberCount(rawSubscriberCount)

    user['channelDescription'] = userData['snippet']['description']
    user['accountPicture'] = userData['snippet']['thumbnails']['medium']['url']
    user['subCount'] = estimatedSubscriberCount

    channelData.insert(-1, user)

  return channelData  

def organizeYouTubeChannelLivestreamData(data, youtubeData):
  channelData = []

  for user in data:
    channel = user['channel']
    userData = getChannelData(channel, youtubeData)

    isLiveOnYouTube = False
    livestreamLink = 'channel-is-not-live'

    if not "livestreams" in user:
      user['livestreams'] = {}

    liveData = {
      'isChannelLive': isLiveOnYouTube,
      'feed': livestreamLink
    }

    if not "youtube" in user['livestreams']:
      user['livestreams']['youtube'] = liveData

    channelData.insert(-1, user)

  return channelData  

def organizeYouTubeChannelAccountPictures(data, youtubeData):
  channelData = []

  for user in data:
    channel = user['channel']
    userData = getChannelData(channel, youtubeData)

    user['accountPicture'] = userData['snippet']['thumbnails']['medium']['url']

    channelData.insert(-1, user)

  return channelData

def getYouTubeChannelDataAll(data):
  parameters = getYoutubeChannelID(data)
  youtubeData = fetchYouTubeChannelData(parameters)

  return organizeYouTubeChannelData(data, youtubeData)

def getYouTubeChannelLivestreamDataAll(data):
  parameters = getYoutubeChannelID(data)
  youtubeData = fetchYouTubeChannelData(parameters)

  return organizeYouTubeChannelLivestreamData(data, youtubeData)

def getYouTubeChannelDataUser(data):
  parameters = [ data ]
  parametersArr = getYoutubeChannelID(parameters)
  youtubeData = fetchYouTubeChannelData(parametersArr)

  return organizeYouTubeChannelData(parameters, youtubeData)

def getYouTubeAccountPictureAll(data):
  parameters = getYoutubeChannelID(data)
  youtubeData = fetchYouTubeChannelData(parameters)

  return organizeYouTubeChannelAccountPictures(data, youtubeData)