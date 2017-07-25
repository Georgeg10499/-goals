#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import logging
import urllib
import base64
from google.appengine.api import urlfetch
from datetime import datetime , timedelta
from goalsDatabase import Goal
from goalsDatabase import Profile
from goalsDatabase import User
from twilio.rest import Client

env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('main.html')
        self.response.write(template.render())

# class CreateUser(webbapp2.RequestHandler):
#     def get(self):
#
#
class CreateGoals(webapp2.RequestHandler):
     def get(self):
        #goal1 = Goal(goal ="The first goal")
        template = env.get_template('main.html')
        self.response.write(template.render())

     def post(self):
        results_templates = env.get_template('results.html')

        goal = Goal(target=self.request.get('goal'),
                   timeHours=int(self.request.get('hour')),
                   timeMinutes=int(self.request.get('minutes')))

        goal_end_time = datetime.now() + timedelta(hours = goal.timeHours)
        logging.info('The current time'+ '{:%H:%M:%S}'.format(datetime.now()))
        logging.info('The new goal time'+ '{:%H:%M:%S}'.format(goal_end_time))
        goal_display = {
            'goal': goal,
        }
        self.response.write(results_templates.render(goal_display))
        #goal = CreateGoal(goal=self.request.get('goal')).put()

        self.response.write('Done')

class CreateProfile(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('profile.html')
        self.response.write(template.render())

    def post(self):
        results_templates = env.get_template('profileResults.html')

        profile = Profile(name=self.request.get('name')).put()
        profile_display = {
            'profile': profile,
        }
        self.response.write(profileResults_templates.render(profile))

class Feed(webapp2.RequestHandler):
    def get(self):
        goals = Goal.query().fetch()
        # goals_dict = {}
        # for task in goals:

class CreateUser(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('user.html')
        self.response.write(template.render())

    def post(self):
        results_templates = env.get_template('.html')

        profile = Profile(username=self.request.get('username')).put()
        profile_display = {
            'user': user,
        }
        self.response.write(_templates.render(user))

class TestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello')
        # Your Account SID from twilio.com/console
        account_sid = "AC421e208e540df7fc2f79ece8da7ef47a"
        # Your Auth Token from twilio.com/console
        auth_token  = "8e0096db271053be309e3308653ed7bf"

        url = 'https://api.twilio.com/2010-04-01/Accounts/%s/Messages' % account_sid
        payload_dict = {'To': '+18188541422', 'From': '+19095528646', 'Body': 'Hello'}
        payload = urllib.urlencode(payload_dict)
        authorization_header = "Basic %s" % base64.b64encode("%s:%s" % (account_sid, auth_token))
        urlfetch.fetch(url, payload=payload, headers={
        "Authorization": authorization_header
        }, method="POST", validate_certificate=True)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create_goal', CreateGoals),
    ('/create_profile', CreateProfile),
    ('/create_user',CreateUser),
    ('/test', TestHandler),
], debug=True)
