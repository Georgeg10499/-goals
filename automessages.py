
import datetime

def reminder(self, desired_time):
    if datetime.now.strftime('%Y-%m-%d %H:%M:%S') < desired_time:
        self.request.write("You still have time to complpete the # goal")
#634129030301-2kc45h1819kipes074le7kal5lruko2p.apps.googleusercontent.com (client ID)
#oVYt5kj6Zpl30O99tUhAteAN (client secret)
