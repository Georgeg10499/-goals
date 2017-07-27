
# import datetime
#
# def reminder(self, desired_time):
#     if datetime.now.strftime('%Y-%m-%d %H:%M:%S') < desired_time:
#         self.request.write("You still have time to complpete the # goal")

def addGoals(self,currentStars, numberOfHours, isCompleted):
    if(isCompleted == True):
        modifiedGoal = currentStars + numberOfHours
    return modifiedGoal
