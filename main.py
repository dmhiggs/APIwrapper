from bottle import Bottle, route, run, template, ServerAdapter
import feed
import buzz
import requests


#for right now it's just a console interface...

#sort by tags, date published, number of comments, author
baseurl = 'http://www.buzzfeed.com/'
feedurl = 'api/v2/feeds/'
commenturl = 'api/v2/comments/'


def getfeed():
    goodurl = False
    thefeed = None
    feeds = ""
    
    #choose feed...loop ends when get a feed
    while goodurl == False:
        feeds = raw_input("type in a feed name: ")

        temp = feedurl+feeds
        
        #check if there's api at that url
        goodurl = checkurl(temp)

    thefeed = feed.Feed(feeds) #instantiate json feed

    #well, I guess you have to choose what to do by numbered list :/
    #maybe make tkinter thing later to make it...prettier???
    choice = -1
    while choice <= 0:
        choice = inputnumber("Sort by \n1. daterange \n2. daterange & minimum number of comments \n3. minimum number of comments \n4. by author \n5. tags\ninput number: ")
        if choice == 0 or choice >= 6:
            print "choose a good number..."

            
    startdate = "" #2017-01-30 15:30:08
    enddate = ""
    #1 through 5 are choices
    if 1<= choice <= 2: #if 1 or 2 do this
        startdate, enddate = getdates() #get dates

        if choice == 1: #sort through feed via dates
            thefeed.get_buzzes_in_date_range(startdate, enddate)
            
        
    if 2<= choice <= 3: #if 2 or 3 do this
        comments = inputnumber("Input minimum number of comments: ")

        if choice == 2: #sort through by dates and comments threshold
            thefeed.get_buzzes_in_dates_threshold(startdate, enddate, comments)
        else: #sort just by comments
            thefeed.get_buzzes_in_threshold(comments)
        
    elif choice == 4:
        #input author userid
        #check to see if userid even exists? then sort...
        while True:
            userid = raw_input("Input author's userid to sort by author: ")
            
            if checkurl(userid): #author webpage exists...so author probably exists...schroedinger's author...
                break
            print "put in good name...like daves4..."                
        #sort by author
        thefeed.get_buzzes_by_author(userid)
        
    elif choice == 5:
        #input tags separated by ", " or maybe just ","
        tags = gettags()
        
        #sort by tags
        thefeed.get_tags(tags)

    return thefeed





###post links to articles on webpage instead of anything else...
###post json to console...? or maybe to another page?
#link is ...com/username/uri


def inputnumber(string):
    while True:
        try:
            number = int(raw_input(string))
            return number;
            break;
        except ValueError:
            print "try putting in a number"
    return 0

def getdates():
    #input date range
    while True:
        startdate = raw_input("Input start date as 'year-month-day hour:minutes:seconds': ")

        #check date to see if it's correct
        if checkdate(startdate) == True:
            #print "good date"
            break

    while True:
        enddate = raw_input("Input end date as 'year-month-day hour:minutes:seconds': ")

        #check date to see if it's correct
        if checkdate(enddate) == True:
            break
        
    return startdate, enddate

def checkdate(date):
    #year-month-day hours:minutes:seconds
    #0000-00-00
    #00:00:00
    date = date.split(' ')
    if len(date) != 2:
        #print "didn't break into 2"
        return False

    date[0] = date[0].split('-')
    if len(date[0]) != 3: #year month day
        #print "didn't break into 3"
        return False
    if checkdateisnumbers(date[0]) == False: #check that everything is digits
        return False

    date[1] = date[1].split(':')
    if len(date[1]) != 3: #hour min sec
        #print "didn't break into 3"
        return False
    if checkdateisnumbers(date[1]) == False: #check that everything is digits
        return False

    return True
    

def checkdateisnumbers(array):
    for item in array:
        i = 0
        for char in item:
            if char < '0' or char > '9': #chars are integers
                #print "char instead of int"
                return False
            i = i + 1
        if item is array[0] and i == 4:
            #print "year is good"
            continue
        if i != 2:
            #print "wrong number of numbers"
            return False
    return True

def gettags():
    tags = []
    string = raw_input("Input tags separated by a comma: ")

    tags = string.split(',')

    for item in tags:
        item = item.split()
        "".join(item)
    return tags


def checkurl(url):
    try:
        if requests.get(baseurl+url).status_code == 200: #webpage exists...
            return True
        else:
            print "try something else\n"
            return False
    except:
        print "maybe something wrong with internet"
        return False



@route('/index')
def index():
    afeed = getfeed()
    return afeed.get_buzzes_links() #return links of buzzes that fit search parameters

run(host='localhost', port=8080)
