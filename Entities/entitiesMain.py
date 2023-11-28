from datetime import datetime

import pytz

from Entities.Employee.Employee import DeskTechnician, SecurityManager
from Entities.IndirectUser import User, Schedule
from Entities.Employee import Employee
from Entities.IndirectUser.User import UserDatabase

# Instantiate the schedule database, the user database and the employee database
schedule_database = Schedule.ScheduleDatabase()
user_database = UserDatabase()
employee_database = Employee.EmployeeDatabase()

# Load schedules, users and employees
schedules = schedule_database.load_schedules()
users = user_database.load_users()
employees = employee_database.get_all_employees()


def getSchedule(workDay):
    """
    Returns a list of strings containing the name of the employee and the time he/she is working on the given day
    @param workDay: The day of the week
    """
    s = []
    schedules_sorted = sorted(schedules, key=lambda x: x.user_id)
    users_sorted = sorted(users, key=lambda x: x.id)

    # Iterate over both lists in parallel
    for schedule, user in zip(schedules_sorted, users_sorted):
        #print(f"{user.firstName} {schedule.workdays}")
        if workDay in schedule.workdays:
            day = f"{user.first_name}: {schedule.workdays[workDay]}"
            s.append(day)
    return s

def is_within_user_schedule(user_id):
    # Define a helper function to check time within interval
    def is_time_within_interval(current_time, start_time, end_time):
        current = datetime.strptime(current_time, '%I:%M %p').time()
        start = datetime.strptime(start_time, '%I:%M %p').time()
        end = datetime.strptime(end_time, '%I:%M %p').time()
        return start <= current <= end

    # Get the current date and time
    now = datetime.now(pytz.timezone('America/New_York'))  # replace 'Your_Timezone' with your timezone
    current_day = now.strftime("%A")
    current_time = now.strftime("%I:%M %p")

    # Find the user's schedule
    for schedule in schedule_database.schedules:
        if schedule.user_id == user_id:
            user_schedule = schedule.workdays

            # Check if today's schedule exists for the user
            if current_day in user_schedule:
                start_time, end_time = user_schedule[current_day].split(' - ')
                start_time = start_time.strip()
                end_time = end_time.strip()
                return is_time_within_interval(current_time, start_time, end_time)

    return False  # User ID not found or current time is not within working hours


is_within_schedule = is_within_user_schedule("0001")
print("Is within schedule:", is_within_schedule)

def getEmployees():
    print("here")
    employees_sorted = sorted(employees, key=lambda x: x.employee_id)
    return employees_sorted

def getUsers():
    users_sorted = sorted(users, key=lambda x: x.id)
    return users_sorted






