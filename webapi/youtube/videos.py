import os
import sys

from requests import get

API_URL = 'https://www.googleapis.com/youtube/v3/'
CHANNEL_PART = "playlistItems?part=snippet&maxResults="
VIDEO_PART = "videos?part=statistics"
KEY = '&key=' + os.environ.get('YOUTUBE_API_CL')

def getYouTubeRecentUploadsID(data):
  parameter = '&playlistId=UU' + data['youtube'][2:]

  return parameter

def getYouTubeVideoID(data):
  videoIDs = ''

  for videos in data:
    if videoIDs == '':
      videoIDs = '&id=' + videos['id']
    else:
      videoIDs = videoIDs + ',' + videos['id']

  return videoIDs

def getStatistics(videoId, videoStatistics):
  try:
    for statistics in videoStatistics:
      if statistics['id'] == videoId:
        return statistics

  except:
    return 'no data'

def organizeVideoData(videos, statistics):
  mappedVideoData = []

  for video in videos:
    videoId = video['id']
    videoStatistics = getStatistics(videoId, statistics)

    video['statistics'] = videoStatistics['statistics']

    mappedVideoData.insert(-1, video)
  
  return mappedVideoData


def fetchYouTubeChannelVideos(parameters, payloadLength = 10):
  dataUrl = API_URL + CHANNEL_PART + str(payloadLength) + KEY + parameters
  response = get(dataUrl)
  videos = response.json()

  youtubeChannels = []
  
  for video in videos['items']:
    videoDetails = video['snippet']

    videoId = videoDetails['resourceId']['videoId']
    videoThumbnail = videoDetails['thumbnails']['high']['url']
    videoTitle = videoDetails['title']
    videoPublishTime = videoDetails['publishedAt']


    videoData = {
      'id': videoId,
      'title': videoTitle,
      'thumbnail': videoThumbnail,
      'publishTime': videoPublishTime
    }

    youtubeChannels.insert(-1, videoData)

  return youtubeChannels

def fetchYouTubeStatistics(parameters):
  dataUrl = API_URL + VIDEO_PART + KEY + parameters
  response = get(dataUrl)
  responseJson = response.json()
  
  videoStatistics = responseJson['items']

  mappedVideoStatistics = []

  for statistics in videoStatistics:
    videoId = statistics['id']
    countViews = statistics['statistics']['viewCount']
    countLikes = statistics['statistics']['likeCount']
    countComments = statistics['statistics']['commentCount']

    mappedStatistics = {
      'views': countViews,
      'likes': countLikes,
      'comments': countComments
    }

    mappedVideoStatistics.insert(-1, {
      'id': videoId,
      'statistics': mappedStatistics
    })

  return mappedVideoStatistics


def getYouTubeChannelVideos(data):
  parameters = getYouTubeRecentUploadsID(data)
  youtubeVideos = fetchYouTubeChannelVideos(parameters)
  
  youtubeVideoParameters = getYouTubeVideoID(youtubeVideos)
  youtubeStatistics = fetchYouTubeStatistics(youtubeVideoParameters)

  videoData = organizeVideoData(youtubeVideos, youtubeStatistics)
  organizedVideoData = sorted(videoData, key=lambda k: k['publishTime'].lower(), reverse=True)

  return organizedVideoData
  
def getAllRecentYouTubeChannelVideos(data):
  tmpYouTubeVideos = [];
  allYouTubeVideos = [];

  for channel in data:
    parameters = getYouTubeRecentUploadsID(channel)
    youtubeVideos = fetchYouTubeChannelVideos(parameters, 1)
    
    youtubeVideoParameters = getYouTubeVideoID(youtubeVideos)
    youtubeStatistics = fetchYouTubeStatistics(youtubeVideoParameters)

    videoData = organizeVideoData(youtubeVideos, youtubeStatistics)
    tmpYouTubeVideos.insert(-1, videoData[0]);

  allYouTubeVideos = sorted(tmpYouTubeVideos, key=lambda k: k['publishTime'].lower(), reverse=True)

  return allYouTubeVideos