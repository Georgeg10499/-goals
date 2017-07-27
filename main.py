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
from goalsDatabase import User
from goalsDatabase import Friend
#from functions import addGoals
from google.appengine.api import users


env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('user.html')

        if user:
            email_address = user.nickname()

            cssi_user = User.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
            link = users.create_logout_url('/')
            sign_out = {
            'sign_out_link' : link}

            if cssi_user:
                template = env.get_template('main.html')
                self.response.write(template.render(sign_out))
            else:
                self.redirect("/create_user")
        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (
                    users.create_login_url('/')))

class CreateUser(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        template = env.get_template('profile.html')

        if user:
            email_address = user.nickname()
            cssi_user = User.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">sign out</a>' % (
                users.create_logout_url('/'))
            self.redirect("/sign_up")

        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (
                    users.create_login_url('/')))

    def post(self):
        user = users.get_current_user()
        cssi_user = User(
            username=self.request.get('username'),
            phone_number=self.request.get('phone_number'),
            quote=self.request.get('quote'),
            photo=self.request.get('photo'),
            goald = 0,
            goals_created = 0,
            goals_completed = 0,
            id=user.user_id())
        test = repr(cssi_user)

        cssi_user.put()
        self.response.write('Thanks for signing up, %s! Click here to access the <a href="/"> site </a> %s' %
            (cssi_user.username, test))

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('signup.html')
        user = users.get_current_user()
        nick_name = user.nickname()
        user_info_dict = { 'email_address' : nick_name }
        self.response.write(template.render(user_info_dict))

class CreateGoals(webapp2.RequestHandler):
     def get(self):
        #goal1 = Goal(goal ="The first goal")
        template = env.get_template('main.html')
        self.response.write(template.render())

     def post(self):
         goals_length = int(self.request.get("number_of_goals"))
         results_templates = env.get_template('profile.html')
         goals_list = []
         for i in range(1, goals_length+1):
             goals_dict = {}
             timeHours = int(self.request.get('hour' + str(i)))
             timeMinutes= int(self.request.get('minutes' + str(i)))
             logging.info(timeHours)
             goal_end_time = datetime.now() + timedelta(hours = timeHours, minutes = timeMinutes)
            #  goal_end_time = goal_end_time.astimezone(timezone('US/Pacific'))
             logging.info('The current time'+ '{:%H:%M:%S}'.format(datetime.now(tz = pytz.utc)))
             logging.info('The new goal time'+ '{:%H:%M:%S}'.format(goal_end_time))
             goal = Goal(target= self.request.get('goal' + str(i)),
                         expected_time = goal_end_time,
                         username=self.request.get("username")
                         # expected_day = self.request.get('day_of_goal')
                       )
             goal.put()
             final_time = datetime.now(tz = pytz.utc) + timedelta(hours = int(timeHours), minutes = int(timeMinutes))
             final_time = final_time.astimezone(timezone('US/Pacific'))

             goal.expected_time = final_time

             goals_list.append(goal)

         goal_display = {'input_forum': ''}
         for goal_obj in goals_list:
             logging.info(goal_obj.target)
             goal_display['input_forum'] += '<div>%s</div><div>%s</div><br>' % (goal_obj.expected_time, goal_obj.target)
         self.response.write(results_templates.render(goal_display))

         self.response.write('Done')

class CreateProfile(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = User.get_by_id(user.user_id())
        user_info = { 'username' : cssi_user.username,
                    'phone_number' : cssi_user.phone_number,
                    'quote': cssi_user.quote,
                    'photo' : cssi_user.photo,
                    'goald' : cssi_user.goald,
                    'goals_created' : cssi_user.goals_created,
                    'goals_completed' : cssi_user.goals_completed
                    }
        template = env.get_template('profile.html')
        self.response.write(template.render(user_info))


class Feed(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('feed.html')
        goals = Goal.query().fetch()
        usernames = []
        for task in goals:
            usernames.append( {'name':task.username} )

        #data  = {'usernames':usernames }
        tasks =[]
        for task in goals:
            tasks.append( {'goal':task.target} )


        data  = {'usernames':usernames , 'tasks':tasks}
        self.response.write(template.render(data))
        # self.response.write(str(goals))
        # goals_dict = {}
        # for task in goals:

class FriendHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('search.html')
        self.response.write(template.render())

    def post(self):
        friend_username = self.request.get('username')
        friend_user = User.query(User.username==friend_username).get()
        if friend_user:
            new_friend = Friend(friend_id= friend_username)
            new_friend.put()
        else:
            self.response.write('User does not exist, please try again <a href="/add_friend"> Search for Friends </a>')


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
    ('/feed', Feed),
    ('/sign_up', SignUpHandler),
    ('/add_friend', FriendHandler)
], debug=True)
