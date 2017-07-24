from google.appengine.ext import ndb

class CreateGoal(ndb.Model):
    goal = ndb.StringProperty()
