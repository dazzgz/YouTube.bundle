# -*- coding: utf-8 -*-
PREFIX = '/video/youtube'

YOUTUBE_STANDARD_FEEDS = 'http://gdata.youtube.com/feeds/api/standardfeeds'

YOUTUBE_STANDARD_TOP_RATED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'top_rated')
YOUTUBE_STANDARD_MOST_VIEWED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_viewed')
YOUTUBE_STANDARD_RECENTLY_FEATURED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'recently_featured')
YOUTUBE_STANDARD_WATCH_ON_MOBILE_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'watch_on_mobile')
YOUTUBE_STANDARD_TOP_FAVORITES_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'top_favorites')
YOUTUBE_STANDARD_MOST_RECENT_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_recent')
YOUTUBE_STANDARD_MOST_DISCUSSED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_discussed')
YOUTUBE_STANDARD_MOST_LINKED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_linked')
YOUTUBE_STANDARD_MOST_RESPONDED_URI = '%s/REGIONID/%s' % (YOUTUBE_STANDARD_FEEDS, 'most_responded')

YOUTUBE_USER_FEED = 'http://gdata.youtube.com/feeds/api/users/%s'
YOUTUBE_OTHER_USER_FEED = 'http://gdata.youtube.com/feeds/api/users/%s/uploads?alt=json'
YOUTUBE_USER_PROFILE = 'http://gdata.youtube.com/feeds/api/users/%s?alt=json'
YOUTUBE_USER_VIDEOS = YOUTUBE_USER_FEED+'/uploads?v=2'
YOUTUBE_USER_ACTIVITY = YOUTUBE_USER_FEED+'/events?v=2'
YOUTUBE_USER_FAVORITES = YOUTUBE_USER_FEED+'/favorites?v=2'
YOUTUBE_USER_PLAYLISTS = YOUTUBE_USER_FEED+'/playlists?v=2'
YOUTUBE_USER_WATCHLATER = YOUTUBE_USER_FEED+'/watch_later?v=2'
YOUTUBE_USER_SUBSCRIPTIONS = YOUTUBE_USER_FEED+'/subscriptions?v=2'
YOUTUBE_USER_NEWSUBSCRIPTIONS = YOUTUBE_USER_FEED+'/newsubscriptionvideos?v=2'
YOUTUBE_USER_RECOMMENDATIONS = YOUTUBE_USER_FEED+'/recommendations?v=2'
YOUTUBE_USER_CONTACTS = YOUTUBE_USER_FEED+'/contacts?v=2&alt=json'

YOUTUBE_VIDEO_FEED = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2'
YOUTUBE_VIDEO_COMMENT_BASE = 'https://gdata.youtube.com/feeds/api/videos/%s/comments/%s'
YOUTUBE_VIDEO_COMMENT = YOUTUBE_VIDEO_COMMENT_BASE+'?v=2'
YOUTUBE_COMMENT = 'http://gdata.youtube.com/feeds/api/videos/%s/comments'
YOUTUBE_COMMENT_FEED = YOUTUBE_COMMENT+'?v=2'
YOUTUBE_RATE_VIDEO = 'https://gdata.youtube.com/feeds/api/videos/%s/ratings'
YOUTUBE_SUBSCRIBE_CHANNEL = 'https://gdata.youtube.com/feeds/api/users/default/subscriptions'

YOUTUBE_RELATED_FEED = 'http://gdata.youtube.com/feeds/api/videos/%s/related?v=2'

YOUTUBE_CHANNELS_FEEDS = 'http://gdata.youtube.com/feeds/api/channelstandardfeeds/%s?v=2'

YOUTUBE_CHANNELS_MOSTVIEWED_URI = YOUTUBE_CHANNELS_FEEDS % ('most_viewed')
YOUTUBE_CHANNELS_MOSTSUBSCRIBED_URI = YOUTUBE_CHANNELS_FEEDS % ('most_subscribed')

YOUTUBE_QUERY = 'http://gdata.youtube.com/feeds/api/%s?q=%s&v=2'

YOUTUBE = 'http://www.youtube.com'

MAXRESULTS = 50
MAX_ACTIVITY_RESULTS = 10

DEVELOPER_KEY = 'AI39si7PodNU93CVDU6kxh3-m2R9hkwqoVrfijDMr0L85J94ZrJFlimNxzFA9cSky9jCSHz9epJdps8yqHu1wb743d_SfSCRWA'

YOUTUBE_VIDEO_DETAILS = 'http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=jsonc'

YOUTUBE_VIDEO_PAGE = 'http://www.youtube.com/watch?v=%s'

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0'

YT_NAMESPACE = 'http://gdata.youtube.com/schemas/2007'

RE_VIDEO_ID = Regex('v=([^&]+)')
RE_COMMENT_ENTRY_ID = Regex('comment:(.*)')
RE_SUBSCRIPTION_ID = Regex('subscription:(.*)')

TITLE = L('YouTube')
ART = 'art-default.jpg'
ICON = 'icon-default.png'
PREFS = 'icon-prefs.png'
ACTIVITY = 'icon-activity.png'
CHANNELS = 'icon-channels.png'
COMMENT = 'icon-comment.png'
COMMENTS = 'icon-comments.png'
DISLIKE = 'icon-dislike.png'
FAVORITES = 'icon-favorites.png'
LIKE = 'icon-like.png'
MYACCOUNT = 'icon-myaccount.png'
PLAYLISTS = 'icon-playlists.png'
RECOMMENDATIONS = 'icon-recommendations.png'
RELATED = 'icon-related.png'
SAVEFORLATER = 'icon-saveforlater.png'
SUBSCRIBE = 'icon-subscribe.png'
SUBSCRIPTIONS = 'icon-subscriptions.png'
UNSUBSCRIBE = 'icon-unsubscribe.png'
VIDEOS = 'icon-videos.png'
WATCHLATER = 'icon-watchlater.png'

####################################################################################################
def Start():
  InputDirectoryObject.thumb = R('Search.png')
  InputDirectoryObject.art = R(ART)

  HTTP.CacheTime = CACHE_1HOUR
  HTTP.Headers['User-Agent'] = USER_AGENT
  HTTP.Headers['X-GData-Key'] = "key=%s" % DEVELOPER_KEY

  Dict.Reset()
  Authenticate()

####################################################################################################
@route(PREFIX + '/validate')
def ValidatePrefs():
  Authenticate()

####################################################################################################
@handler(PREFIX, TITLE, R(ART), R(ICON))
def MainMenu():
  oc = ObjectContainer(no_cache = True)
  regionName = Prefs['youtube_region'].split('/')[0]
  if regionName == 'All':
    localizedVideosName = L('Videos')
  else:
    localizedVideosName = L('Videos for ')+ regionName
  if Authenticate():
    oc.add(DirectoryObject(key = Callback(ParseSubscriptions, title=L('Subscriptions'), url=YOUTUBE_USER_SUBSCRIPTIONS % 'default'),title = L('Subscriptions'), thumb=R(SUBSCRIPTIONS)))
    oc.add(DirectoryObject(key=Callback(PlaylistMenu, title=L('Play Lists')), title=L('Play Lists'), thumb=R(PLAYLISTS)))
  oc.add(DirectoryObject(key = Callback(MyAccount, title = L('My Account')), title = L('My Account'), thumb=GetChannelThumb('default')))
  oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('Recommendations'), url = YOUTUBE_USER_RECOMMENDATIONS % 'default'),title = L('Recommendations'), thumb = R(RECOMMENDATIONS)))
    oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('New Subscriptions Videos'), url = YOUTUBE_USER_NEWSUBSCRIPTIONS % 'default', video_only = True),title = L('New Subscriptions Videos'), thumb = R(VIDEOS)))
  oc.add(DirectoryObject(key = Callback(VideosMenu, title = localizedVideosName), title = localizedVideosName, thumb=R(VIDEOS)))
  oc.add(DirectoryObject(key = Callback(ChannelsMenu, title = L('Channels')), title = L('Channels'), thumb=R(CHANNELS)))
  oc.add(InputDirectoryObject(key = Callback(Search, search_type = 'videos', title = L('Search Videos')), prompt = L('Search Videos'), title = L('Search Videos')))
  oc.add(InputDirectoryObject(key = Callback(Search, search_type = 'videos', title = L('Search Videos (long)'), search_options = '&duration=long'), prompt = L('Search Videos (long)'), title = L('Search Videos (long)')))
  return oc

####################################################################################################
## VIDEOS
####################################################################################################
@route(PREFIX + '/videos')
def VideosMenu(title):
  oc = ObjectContainer(title2 = title)
  oc.add(DirectoryObject(key = Callback(SubMenu, title = L('Today'), category = 'today'), title = L('Today')))
  oc.add(DirectoryObject(key = Callback(SubMenu, title = L('This Week'), category = 'this_week'), title = L('This Week'))) 
  oc.add(DirectoryObject(key = Callback(SubMenu, title = L('This Month'), category = 'this_month'), title = L('This Month'))) 
  oc.add(DirectoryObject(key = Callback(SubMenu, title = L('All Time'), category = 'all_time'), title = L('All Time'))) 
  oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('Most Recent'), url = YOUTUBE_STANDARD_MOST_RECENT_URI), title = L('Most Recent'))) 
  oc.add(InputDirectoryObject(key = Callback(Search, search_type = 'videos', title = L('Search Videos')), title = L('Search Videos'), prompt = L('Search Videos')))
  return oc
####################################################################################################
## PLAYLIST MENU
####################################################################################################
@route(PREFIX + '/playlists')
def PlaylistMenu(title):
  oc = ObjectContainer(title2 = title)
  AddPlaylists( oc, 'default', '' )
  oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('Favorites'), url = YOUTUBE_USER_FAVORITES % 'default', author = 'lookup'),title = L('Favorites'), thumb = R(FAVORITES)))
  oc.add(DirectoryObject(key = Callback(ParseFeed, title=L('Watch Later'), url=YOUTUBE_USER_WATCHLATER % 'default'),title = L('Watch Later'), thumb=R(SAVEFORLATER)))
  return oc
  
####################################################################################################
## CHANNELS
####################################################################################################
@route(PREFIX + '/channels')
def ChannelsMenu(title):
  oc = ObjectContainer(title2 = title)

  oc.add(DirectoryObject(
    key = Callback(ParseChannelFeed, title = L('Most Viewed'), url = YOUTUBE_CHANNELS_MOSTVIEWED_URI), 
    title = L('Most Viewed'))) 
  oc.add(DirectoryObject(
    key = Callback(ParseChannelFeed, title = L('Most Subscribed'), url = YOUTUBE_CHANNELS_MOSTSUBSCRIBED_URI), 
    title = L('Most Subscribed'))) 
  oc.add(InputDirectoryObject(
    key = Callback(Search, search_type = 'channels', title = L('Search Channels')), 
    title = L('Search Channels'), prompt = L('Search Channels')))

  return oc

####################################################################################################
## MY ACCOUNT
####################################################################################################
@route(PREFIX + '/myaccount')
def MyAccount(title):
  oc = ObjectContainer(title2 = title)
  if Authenticate(): 
    oc.add(DirectoryObject(key = Callback(ParseSubscriptionFeed, title = L('Videos'), url = YOUTUBE_USER_VIDEOS % 'default'),title = L('Videos'), thumb = R(VIDEOS)))
    oc.add(DirectoryObject(key = Callback(ParseActivityFeed, title = 'Activity', url = YOUTUBE_USER_ACTIVITY % 'default'), title = 'Activity', thumb=R(ACTIVITY)))
  oc.add(PrefsObject(title = L('Preferences')))
  return oc

####################################################################################################
## AUTHENTICATION
####################################################################################################
@route(PREFIX + '/authenticate')
def Authenticate():

  # Only when username and password are set
  if Prefs['youtube_user'] and Prefs['youtube_passwd']:
    if 'Session' in Dict:
      try:
        req = HTTP.Request('https://www.youtube.com/', values=dict(
            session_token = Dict['Session'],
            action_logout = "1"
          )) 
      except:
         pass
    try:
      req = HTTP.Request('https://www.google.com/accounts/ClientLogin', values=dict(
        Email = Prefs['youtube_user'],
        Passwd = Prefs['youtube_passwd'],
        service = "youtube",
        source = DEVELOPER_KEY
      ))
      data = req.content

      for keys in data.split('\n'):
        if 'Auth=' in keys:
          AuthToken = keys.replace("Auth=",'')
          HTTP.Headers['Authorization'] = "GoogleLogin auth="+AuthToken
          Dict['loggedIn'] = True
          Log("Login Successful")
        if 'SID=' in keys:
          Dict['Session'] = keys.replace("SID=",'')

      return True

    except:
      Dict['loggedIn'] = False
      Log("Login Failed")
      return False

  else:
    return False

####################################################################################################
@route(PREFIX + '/submenu')
def SubMenu(title, category):
  oc = ObjectContainer(title2 = title)

  oc.add(DirectoryObject(
    key = Callback(
      ParseFeed, 
      title = L('Most Viewed'), 
      url = YOUTUBE_STANDARD_MOST_VIEWED_URI + '?time=%s' % category), 
    title = L('Most Viewed')))
  oc.add(DirectoryObject(
    key = Callback(
      ParseFeed, 
      title = L('Top Rated'), 
      url = YOUTUBE_STANDARD_TOP_RATED_URI + '?time=%s' % category), 
    title = L('Top Rated')))
  oc.add(DirectoryObject(
    key = Callback(
      ParseFeed, 
      title = L('Most Discussed'), 
      url = YOUTUBE_STANDARD_MOST_DISCUSSED_URI + '?time=%s' % category), 
    title = L('Most Discussed')))

  return oc

####################################################################################################
# We add a default query string purely so that it is easier to be tested by the automated channel tester
@route(PREFIX + '/search')
def Search(query = 'dog', title = '', search_type = 'videos', search_options = '' ):

  url = YOUTUBE_QUERY % (search_type, String.Quote(query, usePlus = False))
  url = url + search_options
  if search_type == 'videos':
    return ParseFeed(title = title, url = url)
  else:
    return ParseChannelSearch(title = title, url = url)

  return oc

####################################################################################################
@route(PREFIX + '/clean')
def CleanString(string):
  return String.StripTags(string).replace('&amp;','&')

@route(PREFIX + '/addparam')
def AddUrlParameter(url, parameter):
  if '?' in url:
    return url + '&' + parameter
  else:
    return url + '&' + parameter

@route(PREFIX + '/json')
def AddJSONSuffix(url):
  if '?' in url:
    return url + '&alt=json'
  else:
    return url + '?alt=json'

@route(PREFIX + '/region')
def Regionalize(url):
  regionid = Prefs['youtube_region'].split('/')[1]
  if regionid == 'ALL':
    return  url.replace('/REGIONID', '')
  else:
    return url.replace('/REGIONID', '/' + regionid) 

@route(PREFIX + '/rejected', entry=dict)
def CheckRejectedEntry(entry):
  try:
    status_name = entry['app$control']['yt$state']['name']

    if status_name in ['deleted', 'rejected', 'failed']:
      return True

    if status_name == 'restricted':
      status_reason = entry['app$control']['yt$state']['reasonCode']

      if status_reason in ['private', 'requesterRegion']:
        return True

  except:
    pass

  return False

@route(PREFIX + '/parsefeed', page=int, suppresschannel=bool, video_only=bool)
def ParseFeed(title, url, page = 1, author = 'author', suppresschannel = False, video_only = False):
  oc = ObjectContainer(title2=(u'%s' % title), replace_parent=(page > 1))

  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  local_url = Regionalize(local_url)

  try:
    rawfeed = JSON.ObjectFromURL(local_url)
  except:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))

  if rawfeed['feed'].has_key('entry'):
    for video in rawfeed['feed']['entry']:

      # If the video has been rejected, ignore it.
      if CheckRejectedEntry(video):
        continue

      # Determine the actual HTML URL associated with the view. This will allow us to simply redirect
      # to the associated URL Service, when attempting to play the content.
      video_url = None
      for video_links in video['link']:
        if video_links['type'] == 'text/html':
          video_url = video_links['href']
          break

      # This is very unlikely to occur, but we should at least log.
      if video_url is None:
        Log('Found video that had no URL')
        continue

      # As well as the actual video URL, we need the associate id. This is required if the user wants
      # to see related content.
      video_id = None
      try: video_id = RE_VIDEO_ID.search(video_url).group(1).split('&')[0]
      except: pass

      video_title = video['media$group']['media$title']['$t']
      video_author = '??'
      try: video_author = video['author'][0]['name']['$t']
      except: pass

      if (author == 'credit'):
        try: video_author = video['media$group']['media$credit']['$t']
        except: pass
      elif (author == 'lookup'):
        try:
          video_info = VideoInfo(video_id)['entry']
          video_author = video_info['author'][0]['name']['$t']
        except: pass

      thumb = video['media$group']['media$thumbnail'][0]['url']
      duration_units = L('seconds')
      video_duration = int(video['media$group']['yt$duration']['seconds'])
      duration = video_duration * 1000
      if video_duration > 59:
        duration_units = L('minutes')
        video_duration = video_duration / 60
      video_title += ' [%s %s]'%(video_duration, duration_units)

      summary = None
      try: summary = video['media$group']['media$description']['$t']
      except: pass

      # [Optional]
      rating = None
      try: rating = float(video['gd$rating']['average']) * 2
      except: pass

      # [Optional]
      date = None
      try: date = Datetime.ParseDate(video['published']['$t'].split('T')[0]).date()
      except:
        try: date = Datetime.ParseDate(video['updated']['$t'].split('T')[0]).date()
        except: pass

      if video_id is not None and '/playlists/' not in url and not video_only:
        oc.add(DirectoryObject(
          key = Callback(
            VideoSubMenu,
            title = video_title,
            video_id = video_id,
            video_url = video_url,
            summary = summary,
            thumb = thumb,
            originally_available_at = date,
            rating = rating,
            duration = duration, suppresschannel = suppresschannel),
          title = video_title,
          summary = summary,
          duration = duration,
          tagline = 'tagline',
          thumb = Callback(GetThumb, url = thumb)))
      else:
        oc.add(VideoClipObject(
          url = video_url,
          title = video_title,
          summary = summary,
          thumb = Callback(GetThumb, url = thumb),
          originally_available_at = date,
          rating = rating,
          duration = duration,
          tagline = 'tagline'))

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseFeed, title = title, url = url, page = page + 1, author = author, video_only = video_only), 
          title = L('Next Page')))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
  else:
    return oc

@route(PREFIX + '/parsesub', page=int, previous=int, suppresschannel=bool)
def ParseSubscriptionFeed(title, url = '',page = 1, previous = 0, suppresschannel = False):
  oc = ObjectContainer(title2 = title, replace_parent = (page > 1 or previous > 0))

  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  local_url = Regionalize(local_url)

  rawfeed = JSON.ObjectFromURL(local_url)
  for video in rawfeed['feed']['entry']:
    if (1 == 1):
      details = video
      if (1 == 1):
        if details.has_key('yt$videoid'):
          video_id = details['yt$videoid']['$t']
        elif details['media$group'].has_key('media$player'):
          try:
            video_page = details['media$group']['media$player'][0]['url']
          except:
            video_page = details['media$group']['media$player']['url']
            video_id = RE_VIDEO_ID.search(video_page).group(1)
        else:  
          video_id = None

        video_title = details['title']['$t']

        if (video_id != None):# and not(video.has_key('app$control')):
          video_url = YOUTUBE_VIDEO_PAGE % video_id

          try:
            date = Datetime.ParseDate(details['published']['$t'].split('T')[0]).date()
          except: 
            date = Datetime.ParseDate(details['updated']['$t'].split('T')[0]).date()

          try: 
            summary = details['content']['$t']
          except:
            summary = details['media$group']['media$description']['$t']
            summary = summary.split('!express')[0]
          duration_units = L('seconds')
          video_duration = int(details['media$group']['yt$duration']['seconds'])
          duration = video_duration * 1000
          if video_duration > 59:
            duration_units = L('minutes')
            video_duration = video_duration / 60
          video_title += ' [%s %s]'%(video_duration, duration_units)
          try:
            rating = float(details['gd$rating']['average']) * 2
          except:
            rating = None
          thumb = details['media$group']['media$thumbnail'][0]['url']
          if video_id is not None:
            oc.add(DirectoryObject(
              key = Callback(
                VideoSubMenu, 
                title = video_title, 
                video_id = video_id,
                video_url = video_url, 
                summary = summary,
                thumb = thumb,
                originally_available_at = date,
                rating = rating,
                duration = duration, suppresschannel = True),
              title = video_title,
              summary = summary,
              duration = duration,
              thumb = Callback(GetThumb, url = thumb)))
          else:
            oc.add(VideoClipObject(
              url = video_url,
              title = video_title,
              summary = summary,
              thumb = Callback(GetThumb, url = thumb),
              originally_available_at = date,
              rating = rating,
              duration = duration))

  # Check to see if there are any futher results available.
  if rawfeed['feed'].has_key('openSearch$totalResults'):
    total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
    items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
    start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
    if (start_index + items_per_page) < total_results:
      oc.add(NextPageObject(
        key = Callback(ParseSubscriptionFeed, title = title, url = url, page = page + 1, previous = page, suppresschannel = True),
        title = L('Next Page')))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
  else:
    return oc

@route(PREFIX + '/parseactivity', page=int, previous=int)
def ParseActivityFeed(title, url = '', page = 1, previous = 0):
  oc = ObjectContainer(title2 = title, replace_parent = (page > 1 or previous > 0))

  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAX_ACTIVITY_RESULTS + 1)
  local_url += '&max-results=' + str(MAX_ACTIVITY_RESULTS)
  local_url = Regionalize(local_url)
  rawfeed = JSON.ObjectFromURL(local_url)
  for video in rawfeed['feed']['entry']:
    entry_type = None
    for category in video['category']:
      if 'userevents' in category['scheme']:
        entry_type = category['term']
    if entry_type is None:
      break
    details = None
    video_id = None
    duration = 0
    video_duration = 0
    video_title = 'a video'
    video_author = 'UNK'
    summary = ''
    thumb = None
    rating = 0
    views = '?'
    strdate = ''
    strdate = video['updated']['$t'].split('T')[0]
    date = None
    date = Datetime.ParseDate(strdate).date()
    if entry_type == 'user_subscription_added':
      channelid = video['yt$userId']['$t']
      try:
        channel_details = GetChannelInfo(channelid)['entry']
        channel_name = u'%s' % channel_details['title']['$t']
        thumb = channel_details['media$thumbnail']['url']
        summary = channel_details['content']['$t']
      except:
        channel_name = channelid
      entry_title = 'Subscribed to %s on %s'%(channel_name, strdate)
      oc.add(DirectoryObject(key = Callback(ChannelMenu, author = channel_name, authorId = channelid),title = entry_title ,summary = summary,thumb = Callback(GetThumb, url = thumb)))
    elif ( [entry_type == 'video_rated' or entry_type == 'video_favorited' or entry_type == 'video_uploaded' or entry_type == 'video_commented'] ):
      video_id = video['yt$videoid']['$t']
      details = VideoInfo(video_id)['entry'] #Get video details
      video_title = details['title']['$t']
      video_author = details['author'][0]['name']['$t']
      thumb = details['media$group']['media$thumbnail'][0]['url']
      duration_units = L('seconds')
      video_duration = int(details['media$group']['yt$duration']['seconds'])
      duration = video_duration * 1000 #milliseconds?
      if video_duration > 59:
        duration_units = L('minuntes')
        video_duration = video_duration / 60
      try: rating = float(details['gd$rating']['average']) * 2
      except: pass
      summary = video_title + ' [%s %s]'%(video_duration, duration_units)
      if entry_type == 'video_rated':
        entry_title = L('Liked on ') + strdate
      elif entry_type == 'video_uploaded':
        entry_title = L('Uploaded on ') + strdate
      elif entry_type == 'video_commented':
        entry_title = L('Commented on ') + "%s-%s" % (strdate, summary)
        summary = GetVideoComment(video)
      elif entry_type == 'video_favorited':
        entry_title = L('Added to Favorites on ') + strdate
      oc.add(DirectoryObject(key = Callback(VideoSubMenu,title = video_title,video_id = video_id,video_url = YOUTUBE_VIDEO_PAGE%(video_id),summary = summary,thumb = thumb,originally_available_at = date,rating = rating,duration = duration),title = entry_title,summary = summary,duration = duration,thumb = Callback(GetThumb, url = thumb)))
    else:
      oc.add(DirectoryObject(key = Callback(NoOp, title = entry_type, message = entry_type), title = entry_type))

  # Check to see if there are any futher results available.
  if rawfeed['feed'].has_key('openSearch$totalResults'):
    total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
    items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
    start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
    if (start_index + items_per_page) < total_results:
      oc.add(NextPageObject(
        key = Callback(ParseActivityFeed, title = title, url = url, page = page + 1, previous = page), title = L('Next Page')))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any entries'))
  else:
    return oc

@route(PREFIX + '/parsechannel', page=int)
def ParseChannelFeed(title, url, page = 1):
  oc = ObjectContainer(title2 = title, replace_parent = (page > 1))

  # Construct the appropriate URL
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  local_url = Regionalize(local_url)

  rawfeed = JSON.ObjectFromURL(local_url)
  if rawfeed['feed'].has_key('entry'):
    for video in rawfeed['feed']['entry']:

      feedpage = video['author'][0]['uri']['$t']+'?v=2&alt=json'

      try: title = video['title']['$t']
      except: title = video['author'][0]['name']['$t']
      try: summary = video['summary']['$t']
      except: summary = ''
      thumb = video['media$group']['media$thumbnail'][0]['url']
      oc.add(DirectoryObject(
        key = Callback(ParsePreFeed, title = title, feedpage = feedpage),
        title = title,
        summary = summary,
        thumb = Callback(GetThumb, url = thumb)))

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseFeed, title = title, url = url, page = page + 1), 
          title = L('Next Page')))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This query did not return any result'))
  else:
    return oc

@route(PREFIX + '/parseprefeed')
def ParsePreFeed(title, feedpage):
  videos = JSON.ObjectFromURL(feedpage)['entry']['gd$feedLink']
  for vid in videos:
    if 'upload' in vid['rel']:
      link = vid['href']
      
  return ParseFeed(title, url = link)

@route(PREFIX + '/parsesearch', page=int)
def ParseChannelSearch(title, url, page = 1):
  oc = ObjectContainer(replace_parent = (page > 1))

  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  rawfeed = JSON.ObjectFromURL(local_url)
  if rawfeed['feed'].has_key('entry'):
    for video in rawfeed['feed']['entry']:
      link = video['gd$feedLink'][0]['href']
      title = CleanString(video['title']['$t'])
      summary = CleanString(video['summary']['$t'])
      author = video['author'][0]['name']['$t']
      channelId = video['yt$channelId']['$t'] #.strip()
      oc.add(DirectoryObject(
        key = Callback(ParseFeed, title = title, url = link),
        title = title,
        thumb = Callback(GetChannelThumb, channelid = channelId)))

    # Check to see if there are any futher results available.
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseChannelSearch, title = title, url = url, page = page + 1), 
          title = L('Next Page')))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This feed does not contain any video'))
  else:
    return oc

@route(PREFIX + '/parseplaylist', page=int)
def ParsePlaylists(title, url, page = 1):
  oc = ObjectContainer(title2=title, replace_parent=(page > 1))

  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)
  
  rawfeed = JSON.ObjectFromURL(local_url)
  if rawfeed['feed'].has_key('entry'):
    for video in rawfeed['feed']['entry']:
      link = video['content']['src']
      title = video['title']['$t']
      summary = video['summary']['$t']
      oc.add(DirectoryObject(
        key = Callback(ParseFeed, title = title, url = link),
        title = title,
        summary = summary))

  # Check to see if there are any futher results available.
  if rawfeed['feed'].has_key('openSearch$totalResults'):
    total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
    items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
    start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
    if (start_index + items_per_page) < total_results:
      oc.add(NextPageObject(
        key = Callback(ParseFeed, title = title, url = url, page = page + 1), 
        title = L('Next Page')))

  if len(oc) == 0:
    return ObjectContainer(header=L('Error'), message=L('This query did not return any result'))
  else:
    return oc

#Adds playlists to subscription menu
def AddPlaylists( objContainer, authorId, authorName ):
  local_url = AddJSONSuffix(YOUTUBE_USER_PLAYLISTS) % authorId
  try:
    rawfeed = JSON.ObjectFromURL(local_url)
  except:
    return 0 # No playlists
  if rawfeed['feed'].has_key('entry'):
    for playlist in rawfeed['feed']['entry']:
      videos = playlist['yt$countHint']['$t']
      if videos <> 0 :
        title = u'%s: %s (%d videos)' % (L('Playlist'), playlist['title']['$t'], videos) #display playlist title and number of videos
        link = playlist['content']['src']
        # link = AddUrlParameter(link, 'orderby=title') #list of videos in play list to be sorted by title
        thumbUrl = playlist['media$group']['media$thumbnail'][0]['url'].replace('default.jpg', 'hqdefault.jpg')
        summary = playlist['summary']['$t']
        objContainer.add(DirectoryObject(
          key = Callback(ParseFeed, title = title, url = link),
          title = title, thumb=thumbUrl, summary=summary))
  return objContainer

#builds list of subscriptions
@route(PREFIX + '/parsesubs', page=int)
def ParseSubscriptions(title, url = '', page = 1):
  oc = ObjectContainer(title2 = title, replace_parent = (page > 1))
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)

  rawfeed = JSON.ObjectFromURL(local_url, cacheTime = 1)
  entries = {}
  if rawfeed['feed'].has_key('entry'):
    for subscription in rawfeed['feed']['entry']:
      link = subscription['content']['src']
      thumbUrl = subscription['media$thumbnail']['url'].replace('default.jpg', 'hqdefault.jpg') #URL for thubnail image for channel/subscription
      author = subscription['title']['$t'].split(':',1)[1].strip()
      title = u'%s' % author
      try:
        authorId = subscription['yt$channelId']['$t']
      except:
        authorId = author
      try:
        subscription_id = RE_SUBSCRIPTION_ID.search(subscription['id']['$t']).group(1)
      except:
        subscription_id = authorId
      link = YOUTUBE_USER_VIDEOS % (authorId)
      item = DirectoryObject(
        key = Callback(SubscriptionMenu, author = title, authorId = authorId, subscriptionId = subscription_id),
        title = title, thumb = thumbUrl, summary='')
      entries[author.lower()] = item
  authors = entries.keys()
  authors.sort()
  for author in authors:
    oc.add(entries[author])
  oc.add(DirectoryObject(key = Callback(ParseFeed, title = L('New Videos'), url = YOUTUBE_USER_NEWSUBSCRIPTIONS % 'default'), title = L('New Videos'), thumb = R(VIDEOS)))

  if len(oc) == 0:
    if 'default' in url:
      return ObjectContainer(header=L('Error'), message=L('You have no subscriptions'))
    else:
      return ObjectContainer(header=L('Error'), message=L('This user has no subscriptions'))
  else:
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(ParseSubscriptions, title = title, url = url, page = page + 1), 
          title = L('Next Page')))
    return oc

@route(PREFIX + '/subs')
def SubscriptionMenu(author, authorId, subscriptionId):
  oc = ObjectContainer(title2 = author)
  videos = YOUTUBE_USER_VIDEOS % (authorId)
  activity = YOUTUBE_USER_ACTIVITY % (authorId)
  oc.add(DirectoryObject(
    key = Callback(ParseSubscriptionFeed, title = author+L(' (Videos)'), url = videos),
    title = L('Videos'), thumb = R(VIDEOS)))
  oc = AddPlaylists( objContainer = oc, authorId = authorId, authorName = author )
  oc.add(DirectoryObject(
    key = Callback(ParseActivityFeed, title = author+L(' (Activity)'), url = activity),
    title = L('Activity'), thumb=R(ACTIVITY)))
  oc.add(DirectoryObject(
    key = Callback(UnSubscribe, author = author, authorId = subscriptionId),
    title = L('Unsubscribe'), thumb = R(UNSUBSCRIBE)))
  return oc

@route(PREFIX + '/channelmenu')
def ChannelMenu(author, authorId):
  oc = ObjectContainer(title2 = author)
  videos = YOUTUBE_USER_VIDEOS % (authorId)
  activity = YOUTUBE_USER_ACTIVITY % (authorId)
  oc.add(DirectoryObject(
    key = Callback(ParseSubscriptionFeed, title = author+L(' (Videos)'), url = videos),
    title = L('Videos'), thumb = R(VIDEOS)))
  AddPlaylists(objContainer = oc, authorId = authorId, authorName = author )
  oc.add(DirectoryObject(
    key = Callback(ParseActivityFeed, title = author+L(' (Activity)'), url = activity),
    title = L('Activity'), thumb = R(ACTIVITY)))
  oc.add(DirectoryObject(
    key = Callback(Subscribe, author = author, authorId = authorId),
    title = L('Subscribe to channel'), thumb = R(SUBSCRIBE)))
  oc.add(DirectoryObject(
    key = Callback(Subscribe, author = author, authorId = authorId, subscription_type = 'activity'),
    title = L('Subscribe to activity'), thumb = R(SUBSCRIBE)))
  return oc

@route(PREFIX + '/like')
def LikeVideo(title, video_id, rating = 'like'):
  url = YOUTUBE_RATE_VIDEO % (video_id)
  elements = ['<yt:rating value="%s"/>'%(rating)]
  try:
    result = PostCommand(url, elements)
    return ObjectContainer(header = 'Video rated', message = 'You ' + rating + 'd: ' + title)
  except:
    return ObjectContainer(header = L('Error'), message = 'Failed to ' + rating + ' ' + title)

@route(PREFIX + '/subscribe')
def Subscribe(author, authorId, subscription_type = 'channel'):
  url = YOUTUBE_SUBSCRIBE_CHANNEL
  if subscription_type == 'channel':
    action = 'channel'
  else:
    action = 'user'
  elements = ['<category scheme="%s/subscriptiontypes.cat" term="%s"/>'%(YT_NAMESPACE, action),
    '<yt:username>%s</yt:username>'%(authorId)]
  try:
    result = PostCommand(url, elements)
    return ObjectContainer(header = L('Subscribed'), message = L('Successfully subscribed to ') + '%s\'s %s' % (author, subscription_type))
  except:
    return ObjectContainer(header = L('Error'), message = L('Failed to subscribe to ') + '%s\'s %s' % (author, subscription_type))

@route(PREFIX + '/unsubscribe')
def UnSubscribe(author, authorId):
  url = '%s/%s'%(YOUTUBE_SUBSCRIBE_CHANNEL, authorId)
  headers = {'Content-Type': 'application/atom+xml', 'GData-Version': '2', 'X-HTTP-Method-Override': 'DELETE'}
  try:
    result = HTTP.Request(url, headers = headers, data = '').content
    return ObjectContainer(header = L('Unsubscribed'), message = L('Successfully unsubscribed from channel: ') + author)
  except:
    return ObjectContainer(header = L('Error'), message = L('Failed to unsubscribe from channel: ') + author)

####################################################################################################
#Adds video to watch later playlist
@route(PREFIX + '/watchlater')
def WatchLater(video_id):
  url=YOUTUBE_USER_WATCHLATER % 'default'
  request_data = '<?xml version="1.0" encoding="UTF-8"?>\n'
  request_data += '<entry xmlns="http://www.w3.org/2005/Atom"\n'
  request_data += 'xmlns:yt="http://gdata.youtube.com/schemas/2007">\n'
  request_data += '<id>%s</id>\n'%(video_id)
  request_data += '</entry>'
  headers = {'Content-Type': 'application/atom+xml', 'GData-Version': '2'}
  req = HTTP.Request(url, headers = headers, data = request_data)
  if video_id in req.content:
    return ObjectContainer(header = L('Added to Watch Later'), message = L('Successfully added video to Watch Later playlist'))
  else:
    return ObjectContainer(header = L('Error'), message = L('Failed to add video to Watch Later playlist'))
 
@route(PREFIX + '/comments', page=int, previous=int)  
def CommentMenu(title, video_id, thumb = None, page = 1, previous = 0):
  oc = ObjectContainer(title2 = title, replace_parent = (page > 1 or previous > 0))

  url = YOUTUBE_COMMENT_FEED%(video_id)
  local_url = AddJSONSuffix(url)
  local_url += '&start-index=' + str((page - 1) * MAXRESULTS + 1)
  local_url += '&max-results=' + str(MAXRESULTS)

  rawfeed = JSON.ObjectFromURL(local_url, cacheTime = 1)
  if rawfeed['feed'].has_key('entry'):
    for comment in rawfeed['feed']['entry']:
      try:
        comment_id = RE_COMMENT_ENTRY_ID.search(comment['id']['$t']).group(1)
        message = comment['content']['$t']
        title = comment['title']['$t']
        if message == "" and title == "":
          continue
        published = comment['published']['$t']
        author = comment['author'][0]['name']['$t']
        comment_title = '%s %s: %s'%(timestamp(published), author, title)
        prompt = L('Follow up to: ')+title
        oc.add(InputDirectoryObject(
          key = Callback(PostComment, video_id = video_id, comment_id = comment_id),
          title = comment_title,
          prompt = prompt,
          summary = message,
          thumb = Callback(GetThumb, url = thumb)))
      except: pass

  if len(oc) == 0:
    return ObjectContainer(header=L('There are no comments'), message=L('Be the first to comment on this video'))
  else:
    if rawfeed['feed'].has_key('openSearch$totalResults'):
      total_results = int(rawfeed['feed']['openSearch$totalResults']['$t'])
      items_per_page = int(rawfeed['feed']['openSearch$itemsPerPage']['$t'])
      try: start_index = int(rawfeed['feed']['openSearch$startIndex']['$t'])
      except: start_index = 0
      if (start_index + items_per_page) < total_results:
        oc.add(NextPageObject(
          key = Callback(CommentMenu, title = title, video_id = video_id, page = page + 1, previous = page), 
          title = L('Next Page')))
    return oc

@route(PREFIX + '/postcomment')
def PostComment(video_id, query = None, comment_id = None):
  if (query is None) or (query == ''):
    return ObjectContainer(header = L('Error'), message = L('No comment supplied!'))
  url = YOUTUBE_COMMENT%(video_id)
  elements = []
  if comment_id is not None:
    href = YOUTUBE_VIDEO_COMMENT_BASE%(video_id, comment_id)
    elements.append('<link rel="%s#in-reply-to" type="application/atom+xml" href="%s"/>'%(YT_NAMESPACE, href))
  elements.append('<content>%s</content>'%(encodeTags(query)))
  try:
    result = PostCommand(url, elements)
    return ObjectContainer(header = L('Comment posted OK'), message = query)
  except:
    return ObjectContainer(header = L('Error'), message = L('Comment failed to post'))

####################################################################################################
@route(PREFIX + '/postcommand', elements=list)
def PostCommand(url, elements):
  request_data = '<?xml version="1.0" encoding="UTF-8"?>\n'
  request_data += '<entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="%s">\n'%(YT_NAMESPACE)
  for element in elements:
    request_data += element + '\n'
  request_data += '</entry>'
  headers = {'Content-Type': 'application/atom+xml', 'GData-Version': '2'}
  Log('PostCommand %s'%request_data)
  req = HTTP.Request(url, headers = headers, data = request_data)
  return req.content

@route(PREFIX + '/thumb')
def GetThumb(url):
  if url:
    try:
      if url[0:2] == '//':
        url = 'http:%s' % url

      data = HTTP.Request(url.replace('default.jpg', 'hqdefault.jpg'), cacheTime = CACHE_1WEEK).content
      return DataObject(data, 'image/jpeg')
    except:
      Log.Exception("Error when attempting to get the associated thumb")
      pass
  return Redirect(R(ICON))

@route(PREFIX + '/userthumb')
def GetUserThumb(user):
  try:
    details = JSON.ObjectFromURL(YOUTUBE_USER_PROFILE % user)
    return Redirect(GetThumb(details['entry']['media$thumbnail']['url']))
  except:
    Log.Exception("Error when attempting to get the associated user thumb")
    return Redirect(R(ICON))

@route(PREFIX + '/channelthumb')
def GetChannelThumb(channelid):
  try:
    details = JSON.ObjectFromURL(YOUTUBE_USER_PROFILE % channelid)
    return details['entry']['media$thumbnail']['url']
  except:
    return R(MYACCOUNT)

####################################################################################################
@route(PREFIX + '/videosubmenu', rating=float, duration=int, suppresschannel=bool)
def VideoSubMenu(title, video_id, video_url, summary = None, thumb = None, originally_available_at = None, rating = None, duration = 0, suppresschannel = False):
  oc = ObjectContainer(title2 = title)

  if video_id == None:
    video_id = RE_VIDEO_ID.search(video_url).group(1)

  author = '?'
  author_id = None
  try:
    details = VideoInfo(video_id)['entry']
    author = details['author'][0]['name']['$t']
    author_id = details['author'][0]['yt$userId']['$t']
  except:
    pass

  oc.add(VideoClipObject(
    url = video_url,
    title = L('Play Video'),
    summary = summary,
    thumb = Callback(GetThumb, url = thumb),
    originally_available_at = Datetime.ParseDate(originally_available_at).date(),
    rating = rating,
    duration = duration))
#if we have the author id (channelid) and we have not come directly from the channel as a subscription, display the channel thumb
  oc.add(DirectoryObject(
    key = Callback(ParseFeed, title = L('View Related'), url = YOUTUBE_RELATED_FEED % video_id),
    title = L('View Related'), thumb = R(RELATED)))
  if author_id is not None and suppresschannel == False:
    oc.add(DirectoryObject(
      key = Callback(ChannelMenu, author = author, authorId = author_id),
      title = author +' (Channel)', thumb = GetChannelThumb(author_id)))
  oc.add(DirectoryObject(
    key = Callback(CommentMenu, title = title, video_id = video_id),
    title = L('Comments'), thumb = R(COMMENTS)))
  ''' Currently disabled due to broken implementation
  oc.add(InputDirectoryObject(
    key = Callback(PostComment, video_id = video_id),
    title = L('Post Comment'),
    thumb = R(COMMENT),
    prompt = L('Enter comment')))
  '''
  oc.add(DirectoryObject(
    key = Callback(LikeVideo, title = title, video_id = video_id, rating = 'like'),
    title = L('Like'),
    thumb = R(LIKE),
    summary = summary))
  oc.add(DirectoryObject(
    key = Callback(LikeVideo, title = title, video_id = video_id, rating = 'dislike'),
    title = 'Dislike',
    thumb = R(DISLIKE), 
    summary = summary))
  oc.add(DirectoryObject(
    key = Callback(WatchLater, video_id = video_id),
    title = L('Watch Later'), thumb = R(WATCHLATER)))
  return oc

@route(PREFIX + '/videoinfo')
def VideoInfo(videoId):
  url = YOUTUBE_VIDEO_FEED % (videoId)
  local_url = AddJSONSuffix(url)
  rawfeed = JSON.ObjectFromURL(local_url)
  return rawfeed

@route(PREFIX + '/getcomments', activity=dict)
def GetVideoComment(activity):
  comment = ''
  for link in activity['link']:
    if 'comments' in link['rel']:
      href = AddJSONSuffix(link['href'])
      commentfeed = JSON.ObjectFromURL(href)
      comment = commentfeed['entry']['content']['$t'].encode('ascii', 'ignore') #encode needed to ignore chrs that cannot be decoded and could cause an error
      break
  return comment

@route(PREFIX + '/channelinfo')
def GetChannelInfo(channelId):
  url = YOUTUBE_USER_FEED%(channelId)
  local_url = AddJSONSuffix(url)
  rawfeed = ''
  try:
    rawfeed = JSON.ObjectFromURL(local_url)
  except:
    pass
  return rawfeed
  
@route(PREFIX + '/noop')
def NoOp(title = 'No Op', message = 'Does nothing'):
  return ObjectContainer(header = title, message = message)

@route(PREFIX + '/intwithcommas')
def intWithCommas(intVal):
  x = int(intVal)
  if x < 0:
    return '-' + intWithCommas(-x)
  result = ''
  while x >= 1000:
    x, r = divmod(x, 1000)
    result = ",%03d%s" % (r, result)
  return "%d%s" % (x, result)

@route(PREFIX + '/timestamp')
def timestamp(timeinfo):
  date_time = timeinfo.split('T')
  date = date_time[0]
  date_parts = date.split('-')
  time = date_time[1].split('.')[0]
  time_parts = time.split(':')
  return '%s/%s/%s %s:%s'%(date_parts[2], date_parts[1], date_parts[0][2:4], time_parts[0], time_parts[1])

@route(PREFIX + '/encodetags')
def encodeTags(s):
  result = s
  result = result.replace('&', '&amp;')
  result = result.replace('<', '&lt;')
  result = result.replace('>', '&gt;')
  return result
