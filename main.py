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
from datetime import datetime , timedelta
from pytz import timezone
import pytz
from goalsDatabase import Goal
from goalsDatabase import Profile
from goalsDatabase import User

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

        timeHours=int(self.request.get('hour'))
        timeMinutes=int(self.request.get('minutes'))

        goal_end_time = datetime.now(tz = pytz.utc) + timedelta(hours = timeHours, minutes = timeMinutes)
        goal_end_time = goal_end_time.astimezone(timezone('US/Pacific'))
        logging.info('The current time'+ '{:%H:%M:%S}'.format(datetime.now(tz = pytz.utc)))
        logging.info('The new goal time'+ '{:%H:%M:%S}'.format(goal_end_time))

        goal = Goal(target=self.request.get('goal'),
                   expected_time = (goal_end_time))

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


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create_goal', CreateGoals),
    ('/create_profile', CreateProfile),
    ('/create_user',CreateUser),
    ('/test', TestHandler),
], debug=True)
