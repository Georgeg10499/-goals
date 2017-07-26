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
from pytz import timezone
import pytz
from goalsDatabase import Goal
from goalsDatabase import Profile
from goalsDatabase import User
from automessages import reminder
from google.appengine.api import users



env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('user.html')
        # If the user is logged in...
        if user:
            email_address = user.nickname()
            # We could also do a standard query, but ID is special and it
            # has a special method to retrieve entries using it.
            cssi_user = User.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
            # If the user has previously been to our site, we greet them!
            if cssi_user:
                template = env.get_template('main.html')
                self.response.write(template.render())
            else:
                self.redirect("/create_user")
        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (
                    users.create_login_url('/')))


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

        goal_end_time = datetime.now() + timedelta(hours = timeHours, minutes = timeMinutes)
        #goal_end_time = goal_end_time.astimezone(timezone('US/Pacific'))
        logging.info('The current time'+ '{:%H:%M:%S}'.format(datetime.now(tz = pytz.utc)))
        logging.info('The new goal time'+ '{:%H:%M:%S}'.format(goal_end_time))

        goal = Goal(target=self.request.get('goal'),
                    expected_time = (goal_end_time),
                    expected_day = self.request.get('day_of_goal'))
        goal.put()
        final_time = datetime.now(tz = pytz.utc) + timedelta(hours = timeHours, minutes = timeMinutes)
        final_time = final_time.astimezone(timezone('US/Pacific'))

        goal.expected_time = final_time

        goal_display = {
            'goal': goal,
        }
        self.response.write(results_templates.render(goal_display))

        #goal.put()
        #goal = CreateGoal(goal=self.request.get('goal')).put()

        self.response.write('Done')

class CreateProfile(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('profile.html')
        self.response.write(template.render())

    def post(self):
        results_templates = env.get_template('profileResults.html')

        profile = Profile(name=self.request.get('user_name'))
        profile.put()
        profile_display = {
            'profile': profile,
        }
        self.response.write(results_templates.render(profile_display))

class Feed(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('feed.html')
        self.response.write(template.render())
        goals = Goal.query().fetch()
        # goals_dict = {}
        # for task in goals:

class CreateUser(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('profile.html')
        # If the user is logged in...
        if user:
            email_address = user.nickname()
            # We could also do a standard query, but ID is special and it
            # has a special method to retrieve entries using it.
            cssi_user = User.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
            # If the user has previously been to our site, we greet them!
            if cssi_user:
                self.response.write('''
                    Welcome %s %s (%s)! <br> %s <br>''' % (
                        cssi_user.username,
                        cssi_user.phone_number,
                        email_address,
                        signout_link_html))
            # If the user hasn't been to our site, we ask them to sign up
            else:
                self.response.write('''
                    Welcome to our site, %s!  Please sign up! <br>
                    <form method="post" action=""> <br>
                    Enter your username:
                    <input type="text" name="username"> <br>
                    Enter your phone number:
                    <input type="text" name="phone_number"> <br>
                    <input type="submit">
                    </form><br> %s <br>
                    ''' % (email_address, signout_link_html))
        # Otherwise, the user isn't logged in!
        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (
                    users.create_login_url('/')))

    def post(self):
        user = users.get_current_user()
        if not user:
            # You shouldn't be able to get here without being logged in
            self.error(500)
            return
        cssi_user = User(
            username=self.request.get('username'),
            phone_number=self.request.get('phone_number'),
            # ID Is a special field that all ndb Models have, and esnures
            # uniquenes (only one user in the datastore can have this ID.
            id=user.user_id())
        cssi_user.put()
        self.response.write('Thanks for signing up, %s! Click here to access the <a href="/"> site </a>' %
            cssi_user.username, )

# class TokenHandler(webapp2.RequestHandler):
#     def get(self):


class TestHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello')
        # Your Account SID from twilio.com/console
        account_sid = "AC421e208e540df7fc2f79ece8da7ef47a"
        # Your Auth Token from twilio.com/console
        auth_token  = ""

        url = 'https://api.twilio.com/2010-04-01/Accounts/%s/Messages' % account_sid
        payload_dict = {'To': '', 'From': '', 'Body': 'Hello'}
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
    ('/feed', Feed)
    ('/token', TokenHandler)
], debug=True)
