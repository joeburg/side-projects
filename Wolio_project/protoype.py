# initial prototype for Wolio

# Joe Burg
# 02/21/2015

import sys

#----------------------------------------------------------------------------#

def LoadEvents(eventsFile):
    # data structre = {eventID : {eventData : {decisionFactor : value}},
    # {eventMeta : {metaData : specs}}}
    Events = {}
    f = open(eventsFile)
    for line in f:
        line = line.strip()
        if line[0] == '>':
            eventID = line[1:]
            Events[eventID] = {}
            Events[eventID]['eventData'] = {}
            eventData = True
        else:
            if line[0] == '#':
                eventName = line[1:]
                Events[eventID]['eventMeta'] = {}
                Events[eventID]['eventMeta']['name'] = eventName
                eventData = False
            else:
                if eventData:
                    fields = line.split()
                    Events[eventID]['eventData'][fields[0]] = map(int, fields[1:])
##                    if len(fields) > 2:
##                        Events[eventID]['eventData'][fields[0]] = map(int, fields[1:])
##                    else:
##                        Events[eventID]['eventData'][fields[0]] = int(fields[1])
                        
                else:
                    idx = line.find('_')
                    spec = line[:idx]
                    spec_data = line[idx+1:]
                    Events[eventID]['eventMeta'][spec] = spec_data
    return Events

def LoadUsers(usersFile):
    # data structure = {userID : {decisionFactor : value}}; ranking is also a key
    Users = {}
    f = open(usersFile)
    for line in f:
        if line[0] == '>':
            line = line.strip()
            userID = line[1:]
            Users[userID] = {}
            newuser = True
        else:
            fields = line.strip().split()
            if newuser:
                Users[userID]['rankings'] = fields
                newuser = False
            else:
                Users[userID][fields[0]] = int(fields[1])
    return Users

def ComputeEventRankings(Events,Users):
    ''' naive implementation with just seeing how many matches there are'''
    # data structure = {userID : [eventID,..]}
    UsersFeed = {}
    for userID in Users:
        UsersFeed[userID] = []
        for eventID in Events:
            matchRating = 0
            for decisionFactor in Events[eventID]['eventData']:
                if Users[userID][decisionFactor] in Events[eventID]['eventData'][decisionFactor]:
                    matchRating += 1

            if matchRating >= 6:
                UsersFeed[userID].append(eventID)
    return UsersFeed

def ComputeEventRankings2(Events,Users):
    ''' makes use of user decision factors rankings and democracy algo '''
        # data structure = {userID : [eventID,..]}
    UsersFeed = {}
    for userID in Users:
        UsersFeed[userID] = []
        userRankings = Users[userID]['rankings']
        for eventID in Events:
            matchRating = 0
            for decisionFactor in Events[eventID]['eventData']:
                if Users[userID][decisionFactor] in Events[eventID]['eventData'][decisionFactor]:
                    '''algo counts matches in top 6 DFs and substracts matches in last 2 DFs'''
                    if decisionFactor in userRankings[:6]: # top 6 
                        matchRating += 1
                    elif decisionFactor in userRankings[-2:]: # bottom 2
                        matchRating -= 1

            '''Must have total rating of 3 to have event listed''' 
            if matchRating >= 3:
                UsersFeed[userID].append(eventID)
    return UsersFeed

def ShowUserFeed(UserFeed,Events):
    for userID in UsersFeed:
        print '################################################################################\n'
        print '%s screen will have these events...\n\n' %userID
        for eventID in UsersFeed[userID]:
            print '-----------------------------------------------------------------------------'
            print 'Event name: %s\n' %Events[eventID]['eventMeta']['name']
            print 'Event date: %s\n' %Events[eventID]['eventMeta']['date']
            print 'Event location: %s\n' %Events[eventID]['eventMeta']['location']
            print 'Event venue: %s\n' %Events[eventID]['eventMeta']['venue']
            print 'Event organizer: %s\n' %Events[eventID]['eventMeta']['organizer']
            print 'Event description: %s\n' %Events[eventID]['eventMeta']['description']              
    return

#----------------------------------------------------------------------------#
'''main program'''

# Analyze the command line arguments and setup the corresponding parameters
if len(sys.argv) < 1:
  print 'Usage:'
  print '  python %s' % sys.argv[0]
  exit()

eventsFile = 'testEvents.txt'
usersFile = 'testUsers.txt'


users = LoadUsers(usersFile)
##print users
##print users['Joe']['rankings']

events = LoadEvents(eventsFile)
##print events

UsersFeed = ComputeEventRankings(events,users)
ShowUserFeed(UsersFeed,events)
print UsersFeed

UsersFeed2 = ComputeEventRankings2(events,users)
##ShowUserFeed(UsersFeed2,events)
print UsersFeed2


