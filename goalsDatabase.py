from google.appengine.ext import ndb
from datetime import time

class Goal(ndb.Model):
    target = ndb.StringProperty()
    expected_time = ndb.DateTimeProperty()
    # expected_day = ndb.DateProperty()
    username = ndb.StringProperty()
    completed = ndb.BooleanProperty(default = False)

class User(ndb.Model):
    username = ndb.StringProperty()
    phone_number = ndb.StringProperty()
    quote = ndb.StringProperty()
    photo = ndb.StringProperty()
    goald = ndb.IntegerProperty()
    goals_created = ndb.IntegerProperty()
    goals_completed = ndb.IntegerProperty()

goals = Goal.query().fetch()

def addGoals(self,currentStars, numberOfHours, isCompleted):
    if(isCompleted == True):
        modifiedGoal = currentStars + numberOfHours
    return modifiedGoal

class Friend(ndb.Model):
    friend_id = ndb.StringProperty()
    your_id = ndb.StringProperty()
