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

def getEmployees():
    print("here")
    employees_sorted = sorted(employees, key=lambda x: x.employee_id)
    return employees_sorted

def getUsers():
    users_sorted = sorted(users, key=lambda x: x.id)
    return users_sorted






