'''
This script is to test and play around with youtube API
using Python.

'''

# Libraries
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import httplib2
from httplib2 import socks
import os
import sys

# Setup a proxy
## ANZ proxy is used below
p = httplib2.ProxyInfo(proxy_type=socks.PROXY_TYPE_HTTP,
                        proxy_host='10.62.36.14',
                        proxy_port=80)

# http connection
# theHttp = httplib2.Http(proxy_info=p)

# https connection (need to disable ssl)
theHttp = httplib2.Http(proxy_info=p, disable_ssl_certificate_validation=True)


# Building youtube connection

DEVELOPER_KEY = "AIzaSyBBHyzwTo0G-F6q3_aL59fYHshiRNS9Sow"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY, http=theHttp)


# 1. Youtube search by keyword
def youtube_search(keyword, max_results=5):
    '''
    input keyword and this function will search the keyword and returning
    maximum top 5 results
    '''
    res = youtube.search().list(
        q=keyword,
        maxResults=max_results,
        part='id',
        ).execute()

    # will return search result and the video id and also optional snippet
    # snippet is the details information about video results
    return res

# 2. Getting video statistics (single and multiple query)
def youtube_stats(keyword):
    '''
    get the statistics of a youtube video including likes/dislikes,
    view counts, comment counts
    '''
    res = youtube.video().list(
        ).execute()

    return res

# 3. Getting all comments from a single video
def youtube_comments():
    '''
    get the maximum number of comments in a video and return all
    the comments in text format
    '''

    res = youtube.comment().list(
        ).execute()


    return res

# 4. getting all trending videos from certain countries

# 5. retrieve top 10 videos by view counts

# 6. get all videos from certain channel

# 7. get video by categories

# 8. Youtube search video by location

# 9. inquire daily quota limit






# video_id = 'LGtNgpzI6tc'
# results = youtube.commentThreads().list(part='snippet',
#                                         videoId=video_id,
#                                         textFormat='plainText').execute()

# print(results)





# End script
print('youtube script success')
