from google.appengine.ext import ndb
from datetime import time

class Goal(ndb.Model):
    goal = ndb.StringProperty()
    timeHours = ndb.IntegerProperty()
    timeMinutes = ndb.IntegerProperty()

class Profile(ndb.Model):
    name = ndb.StringProperty()


class User(ndb.Model):
    username = ndb.StringProperty()
