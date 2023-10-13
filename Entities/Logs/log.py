from Entities.IndirectUser import User
from Entities.Employee import Employee
import datetime

class Log:
    def __init__(self, timeStamp, techID, userID, firstName, lastName, company, title):
        self.timestamp = timeStamp
        self.techID = techID
        self.userID = userID
        self.firstName = firstName
        self.lastName = lastName
        self.company = company
        self.title = title

    def getLog(self):
        l = Log(self.timestamp, self.techID, self.userID, self.firstName, self.lastName, self.company, self.title)
        return l

