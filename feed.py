import json
import buzz
import urllib

    

class Feed():
    baseURL = 'http://www.buzzfeed.com/api/v2/feeds/'
    fullURL = baseURL
    
    feedURL = None
    buzzes = []

    sorted_buzzes = []

    #feedtype is a string of either "lol", "news", "omg", etc.
    def __init__(self, feedtype): #initialize...takes a very long time...i guess because I'm going through all the pages? :/
        self.fullURL = self.baseURL + feedtype #make full url
        self.feedURL = urllib.urlopen(self.fullURL) #open url
        feedJSON = json.loads(self.feedURL.read()) #read url into json
	self.buzzes = []
	self.sorted_buzzes = []
        uri = {} #uri is unique
        i = 2
        #go through feed pages until "buzzes = []"...?p=#
        while feedJSON["buzzes"] != []: #take the nested buzzes json out
            #when testing this, duplicates appeared and looking through the api, articles are repeated :C
            #so skip over the duplicates...
            #list of dicts...comparing dicts...
            for abuzz in feedJSON["buzzes"]:
		thing = buzz.Buzz(abuzz)
                if thing in uri.values(): #hopefully the overloaded operator will fix the duplicates...
                    continue
                uri[thing.geturi()] = thing #make dict of buzzes from uris
                self.buzzes.append(thing) #make buzz and append to buzzes
            temp = self.fullURL+"?p="+str(i)
            feedJSON = json.loads(urllib.urlopen(temp).read())
            i = i + 1
        #self.buzzes = list(set(self.buzzes)) ###previous attempt at getting rid of duplicates

	#It appears to make duplicates when you reload the page... hmmmm

        return

    def reload_buzzes(self): #reload buzzes incase of updates...
        self.buzzes = []
        self.sorted_buzzes = []
        self.feedURL = urllib.urlopen(self.fullURL) #open url
        feedJSON = json.loads(self.feedURL.read()) #save json

        i = 2
        #go through feed pages until "buzzes = []"...?p=#
        while feedJSON["buzzes"] != []:
            uri = {}
            for abuzz in feedJSON["buzzes"]:
                if abuzz["uri"] in uri.values():
                    continue
                uri[abuzz["uri"]] = abuzz["uri"] #might as well make it equal itself
                self.buzzes.append(buzz.Buzz(abuzz)) #make buzz and append to buzzes
            temp = self.fullURL+"?p="+str(i)
            feedJSON = json.loads(urllib.urlopen(temp).read())
            i = i + 1
        return        

    def get_buzzes_json(self):
        jsons = []
        for abuzz in self.sorted_buzzes:
            jsons.append(abuzz.getjson())
        return jsons

    ## <link>Title: Description</a>
    def get_buzzes_links(self):
	
	self.sorted_buzzes = sorted(self.sorted_buzzes)

        links = ""
        for abuzz in self.sorted_buzzes:
            links = links + '<a href = "' + abuzz.getlink() + '">' + abuzz.gettitle() + '</a><br><br>'
        return links

    #1. endpoint given feed, start, end...get buzzes within start&end
    def get_buzzes_in_date_range(self, start, end):
        self.sorted_buzzes = []
        for abuzz in self.buzzes:
            if start <= abuzz.getpubdate() <= end:
                self.sorted_buzzes.append(abuzz)
        return

    #3. endpoint given feed, start, end, threshold...get buzzes
    def get_buzzes_in_dates_threshold(self, start, end, threshold):
        self.get_buzzes_in_date_range(start, end)

        temp_buzzes = self.sorted_buzzes #save the buzzes in the date range
        self.sorted_buzzes = []
        for abuzz in temp_buzzes:
            cURL = urllib.urlopen(abuzz.getcomments()) #open url
            cJSON = json.loads(cURL.read()) #read url into json

            if cJSON["total_count"] >= str(threshold): #already confirmed that threshold is number so it can compare this way
                self.sorted_buzzes.append(abuzz)
        return

    #sort by just comments
    def get_buzzes_in_threshold(self, threshold):
        self.sorted_buzzes = []

        for abuzz in self.buzzes:
            cURL = urllib.urlopen(abuzz.getcomments()) #open url
            cJSON = json.loads(cURL.read()) #read url into json

            if cJSON["total_count"] >= str(threshold): #already confirmed that threshold is number so it can compare this way
                self.sorted_buzzes.append(abuzz)
        return

    #sort by author
    def get_buzzes_by_author(self, author):
        self.sorted_buzzes = []

        for abuzz in self.buzzes: #go through buzzes and returns all articles by author in that feed
            if author == abuzz.getauthor():
                self.sorted_buzzes.append(abuzz)
        return

    #sort by tags    
    def get_tags(self, inputtags):
        self.sorted_buzzes = []

        for abuzz in self.buzzes:
            if abuzz.hastags(inputtags) == True:
                self.sorted_buzzes.append(abuzz)
        return
