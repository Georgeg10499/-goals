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

        if user:
            cssi_user = User.get_by_id(user.user_id())
            link = users.create_logout_url('/')
            sign_out = {
            'sign_out_link' : link}

            if cssi_user:
                template = env.get_template('main.html')
                self.response.write(template.render(sign_out))
            else:
                self.redirect("/create_user")
        else:
            template = env.get_template('login.html')
            link = users.create_login_url('/')
            sign_in = {
            'sign_in_link' : link}
            self.response.write(template.render(sign_in))


class CreateUser(webapp2.RequestHandler):
    def get(self):
        self.redirect("/sign_up")

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

        cssi_user.put()
        self.response.write('Thanks for signing up, %s! Click here to access the <a href="/"> site </a> ' %
            (cssi_user.username))

class SignUpHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('signup.html')
        user = users.get_current_user()
        nick_name = user.nickname()
        user_info_dict = { 'email_address' : nick_name }
        self.response.write(template.render(user_info_dict))

class CreateGoals(webapp2.RequestHandler):
     def get(self):
        template = env.get_template('main.html')
        self.response.write(template.render())

     def post(self):
        template = env.get_template('results.html')
        num_of_goals = int(self.request.get("number_of_goals"))
        goals_list = []
        for i in range(1,num_of_goals+1):
            timeHours=int(self.request.get('hour' + str(i)))
            timeMinutes=int(self.request.get('minutes' + str(i)))

            goal_end_time = datetime.now() + timedelta(hours = timeHours, minutes = timeMinutes)
            #goal_end_time = goal_end_time.astimezone(timezone('US/Pacific'))
            logging.info('The current time'+ '{:%H:%M:%S}'.format(datetime.now(tz = pytz.utc)))
            logging.info('The new goal time'+ '{:%H:%M:%S}'.format(goal_end_time))

            goal = Goal(target=self.request.get('goal' + str(i)),
                        expected_time = (goal_end_time),
                        username=self.request.get("username"),
                        completed = False,
                        number_of_hours = int(self.request.get('hour' + str(i)))
                        # expected_day = self.request.get('day_of_goal')
                        )
            goal.put()
            final_time = datetime.now(tz = pytz.utc) + timedelta(hours = timeHours, minutes = timeMinutes)
            final_time = final_time.astimezone(timezone('US/Pacific'))

            goal.expected_time = final_time
            goals_list.append(goal)

        goal_display = {
            'input_forum': '',
        }
        checkbox_counter = 0
        for goal_obj in goals_list:
            filler = '%s %s' % (goal_obj.target, goal_obj.expected_time.strftime('%m-%d-%Y %H:%M'))
            goal_display['input_forum'] += '''
                     <input type="checkbox" name="is_complete''' + str(checkbox_counter) + ''' " >
                     ''' + filler + ''' <br> '''
            checkbox_counter += 1



        # user = users.get_current_user()
        # cssi_user = User.get_by_id(user.user_id())
        # user_info = { 'username' : cssi_user.username,
        #             'phone_number' : cssi_user.phone_number,
        #             'quote': cssi_user.quote,
        #             'photo' : cssi_user.photo,
        #             'goald' : cssi_user.goald,
        #             'goals_created' : cssi_user.goals_created,
        #             'goals_completed' : cssi_user.goals_completed
        #             }
        # goal_display.update({'user_info': user_info})
        self.response.write(template.render(goal_display))

class CreateProfile(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = User.get_by_id(user.user_id())
        goal_count = len(Goal.query(User.username == cssi_user.username).fetch())
        goal_count2 = len(Goal.query(User.username == cssi_user.username, Goal.completed == True).fetch())
        user_info = { 'username' : cssi_user.username,
                    'phone_number' : cssi_user.phone_number,
                    'quote': cssi_user.quote,
                    'photo' : cssi_user.photo,
                    'goald' : cssi_user.goald,
                    'goals_created' : goal_count,
                    'goals_completed' : goal_count2
                    }
        goal_display = {
            'input_forum': '',
        }

        goals_list = Goal.query(User.username == cssi_user.username).fetch()
        # for task in goals_list:
        #
        #     task.expected_time = task.expected_time.astimezone(timezone('US/Pacific'))

        checkbox_counter = 0
        for goal_obj in goals_list:
            filler = '%s %s' % (goal_obj.target, goal_obj.expected_time.strftime('%m-%d-%Y %H:%M'))
            goal_display['input_forum'] += '''
                        <input type="checkbox" name="is_complete" value = "''' + str(goal_obj.key.id()) + '''" >
                        ''' + filler + ''' <br> '''

        goal_display.update({'user_info': user_info})
        account_sid = "AC421e208e540df7fc2f79ece8da7ef47a"
        # Your Auth Token from twilio.com/console
        auth_token  = ""

        url = 'https://api.twilio.com/2010-04-01/Accounts/%s/Messages' % account_sid
        payload_dict = {'To': '', 'From': '', 'Body': 'Here are your goals'}
        payload = urllib.urlencode(payload_dict)
        authorization_header = "Basic %s" % base64.b64encode("%s:%s" % (account_sid, auth_token))
        urlfetch.fetch(url, payload=payload, headers={
        "Authorization": authorization_header
        }, method="POST", validate_certificate=True)
        template = env.get_template('profile.html')
        self.response.write(template.render(goal_display))

class Feed(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('feed.html')
        user = users.get_current_user()
        cssi_user = User.get_by_id(user.user_id())
        your_id = cssi_user.username
        friends = Friend.query(Friend.your_id == your_id).fetch()
        friend_usernames = [ friend.friend_id for friend in friends ]

        goals = Goal.query().fetch()
        usernames = []
        for goal in goals:
            if goal.username in friend_usernames:
                usernames.append( {'name':goal.username} )

        #data  = {'usernames':usernames }
        tasks =[]
        for goal in goals:
            if goal.username in friend_usernames:
                tasks.append( {'goal':goal.target} )


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
        user = users.get_current_user()
        cssi_user = User.get_by_id(user.user_id())
        your_id = cssi_user.username
        friend_username = self.request.get('username')
        friend_user = User.query(User.username==friend_username).get()
        if friend_user:
            new_friend = Friend(friend_id= friend_username, your_id= your_id)
            new_friend.put()
            self.response.write("Friend added")
        else:
            self.response.write('User does not exist, please try again <a href="/add_friend"> Search for Friends </a>')

class GoalComplete (webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = User.get_by_id(user.user_id())
        your_id = cssi_user.username
        user_goals = Goals.query(your_id).fetch()

    def post(self):
        completed_list = self.request.get('is_complete', allow_multiple = True)
        for goal_id in completed_list:
            goal = Goal.get_by_id(int(goal_id))
            goal.completed = True
            goal.put()
            self.redirect("/")




# class TestHandler(webapp2.RequestHandler):
#     def get(self):
#         self.response.write('Hello')
#         # Your Account SID from twilio.com/console
#         account_sid = "AC421e208e540df7fc2f79ece8da7ef47a"
#         # Your Auth Token from twilio.com/console
#         auth_token  = ""
#
#         url = 'https://api.twilio.com/2010-04-01/Accounts/%s/Messages' % account_sid
#         payload_dict = {'To': '', 'From': '', 'Body': 'Hello'}
#         payload = urllib.urlencode(payload_dict)
#         authorization_header = "Basic %s" % base64.b64encode("%s:%s" % (account_sid, auth_token))
#         urlfetch.fetch(url, payload=payload, headers={
#         "Authorization": authorization_header
#         }, method="POST", validate_certificate=True)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create_goal', CreateGoals),
    ('/create_profile', CreateProfile),
    ('/create_user',CreateUser),
    # ('/test', TestHandler),
    ('/feed', Feed),
    ('/sign_up', SignUpHandler),
    ('/add_friend', FriendHandler),
    ('/goal_complete', GoalComplete)
], debug=True)
