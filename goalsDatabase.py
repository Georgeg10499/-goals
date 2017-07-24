from google.appengine.ext import ndb
from datetime import time

class CreateGoal(ndb.Model):
    goal = ndb.StringProperty()
    timeHours = ndb.IntegerProperty()
    timeMinutes = ndb.IntegerProperty()
