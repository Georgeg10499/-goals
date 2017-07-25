from google.appengine.ext import ndb
from datetime import time

class Goal(ndb.Model):
    target = ndb.StringProperty()
    expected_time = ndb.DateTimeProperty()


class Profile(ndb.Model):
    name = ndb.StringProperty()


class User(ndb.Model):
    username = ndb.StringProperty()
