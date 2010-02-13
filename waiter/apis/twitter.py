from waiter import Waiter, Menu, JSONConsumer
from waiter.chefs import LaxRecipeChef

def grab_oauth_library(what):
    try:
        return __import__(what)
    except ImportError:
        return None

class TwitterException(Exception):
    pass

class TwitterMenu(Menu):
    def set_waiter_http(self, waiter):
        waiter._http = self.value
        return waiter

    def __init__(self, value, oauth_importer=grab_oauth_library, *args, **kwargs):
        dispatch_update = {}
        oauth_library = oauth_importer('oauth2')
        if oauth_library:
            dispatch_update = {
                oauth_library.Client:self.set_waiter_http
            }
        super(TwitterMenu, self).__init__(value, dispatch_update=dispatch_update, *args, **kwargs)

class TwitterConsumer(JSONConsumer):
    def handle(self, response, data):
        if response.status in (404, 500, 503):
            raise TwitterException("Got a bad response - %d" % response.status)
        parsed_data = super(TwitterConsumer, self).handle(response, data)
        if 'error' in parsed_data.keys():
            raise TwitterException("Bad request - %s" % parsed_data['error'])
        return parsed_data

class TwitterRecipeChef(LaxRecipeChef):
    def __init__(self):
        return super(TwitterRecipeChef, self).__init__('https://twitter.com', TWITTER_ENDPOINTS)

class Twitter(Waiter):
    def __init__(self, *args, **kwargs):
        return super(Twitter, self).__init__(menu_class=TwitterMenu, consumer=TwitterConsumer(), chef=TwitterRecipeChef(), *args,**kwargs)

TWITTER_ENDPOINTS = LaxRecipeChef.string_recipe_to_dict("""
    search - GET
    trends - GET
    trends/current - GET
    trends/daily - GET
    trends/weekly - GET
    statuses/public_timeline - GET
    statuses/home_timeline - GET
    statuses/friends_timeline - GET
    statuses/user_timeline - GET
    statuses/mentions - GET
    statuses/retweeted_by_me - GET
    statuses/retweeted_to_me - GET
    statuses/retweets_of_me - GET
    statuses/show - GET
    statuses/update - POST
    statuses/destroy - POST
    statuses/retweet - POST
    statuses/retweets - GET
    users/show - GET
    users/search - GET
    statuses/friends - GET
    statuses/followers - GET
    direct_messages - GET
    direct_messages/sent - GET
    direct_messages/new - POST
    direct_messages/destroy - POST
    friendships/create - POST
    friendships/destroy - POST
    friendships/exists - GET
    friendships/show - GET
    friends/ids - GET
    followers/ids - GET
    account/verify_credentials - GET
    account/rate_limit_status - GET
    account/end_session - POST
    account/update_delivery_device - POST
    account/update_profile_colors - POST
    account/update_profile_image - POST
    account/update_profile_background_image - POST
    account/update_profile - POST
    favorites - GET
    favorites/create - POST
    favorites/destroy - POST
    notifications/follow - POST
    notifications/leave - POST
    blocks/create - POST
    blocks/destroy - POST
    blocks/exists - GET
    blocks/blocking - GET
    blocks/blocking/ids - GET
    report_spam - GET
    saved_searches - GET
    saved_searches/show - GET
    saved_searches/create - POST
    saved_searches/destroy - POST
    oauth/request_token - GET
    oauth/authorize - GET
    oauth/authenticate - GET
    oauth/access_token - POST
    trends/available - GET
    trends/location - GET
""")
