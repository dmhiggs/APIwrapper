import json

class Buzz():
    buzz_json = ""
    commentsurl = 'http://www.buzzfeed.com/api/v2/comments/'
    articleurl = 'http://www.buzzfeed.com/'

    metavertical = None #not all have this...
    country_code = None
    status = None
    bylines = None #this is a json value...avatar, twitter page url, displayname, username, email, description id, title, bio, description visual, facebook page url
    comment_stats = None
    datelines = None #possibly also a json? []...width, language, zoom, name, location_id, height, marker_lng, map_center_lat, marker_lat, map_center_lng, dateline_img
    impressions = None
    category_id = None
    disclaimer_top = None
    buzz_id = None
    category = None
    published_date = None
    images = None #json? dict?...small, standard, big, wide, dblbig, dblwide
    last_updated = None
    flags = None #json??? dict? reactions_enabled, comments_enabled, mobile_safe, ad, brand_safe, sensitive, nsfw, raw, partner, developing_mode
    language = None
    description = None
    tags = [] #list of tags on it...
    username = None
    uri = None
    disclaimer_bottom = None
    published = None
    short_description = None
    buzz_format = None #dict? page_width, page_type
    title = None
    user_id = None

    def __init__(self, buzzjson):
        self.buzz_json = buzzjson
        self.commentsurl = self.commentsurl + buzzjson["id"]
        self.articleurl = self.articleurl + buzzjson["username"] + "/" + buzzjson["uri"]

        self.published_date = buzzjson["published_date"]
        self.description = buzzjson["description"]
        self.tags = buzzjson["tags"]
        self.username = buzzjson["username"]
        self.title = buzzjson["title"]
        self.uri = buzzjson["uri"]
        return

    def __eq__(self, other):
	if self.uri == other.uri:
		return True
        return False
    def __lt__(self, other):
	if self.title < other.title:
		return True
	return False
    def __ge__(self, other):
	if self.title >= other.title:
		return True
	return False
    
    def getcommentsnum(self):
        return self.comments_number

    def getpubdate(self):
        return self.published_date

    def getauthor(self):
        return self.username

    def getjson(self):
        return self.buzz_json

    def getcomments(self):
        return self.commentsurl

    def getlink(self):
        return self.articleurl

    def gettitle(self):
        return self.title + ": " + self.description
    
    def hastags(self, tag_array):
        if len(list(set(tag_array).intersection(self.tags))) > 0:
            return True
        return False

    def geturi(self):
        return self.uri

