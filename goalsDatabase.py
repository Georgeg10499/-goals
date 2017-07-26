from google.appengine.ext import ndb
from datetime import time

class Goal(ndb.Model):
    target = ndb.StringProperty()
    expected_time = ndb.DateTimeProperty()
    # expected_day = ndb.DateProperty()
    username = ndb.StringProperty()

class User(ndb.Model):
    name = ndb.StringProperty()
    username = ndb.StringProperty()
    phone_number = ndb.StringProperty()
