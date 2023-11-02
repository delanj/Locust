from Entities.IndirectUser import User, Schedule
from Entities.Employee import Employee


# Instantiate the schedule database and the user database
schedule_database = Schedule.ScheduleDatabase('../Database/IndirectUsers/jsonFile/schedule.json')
user_database = User.UserDatabase('../Database/IndirectUsers/jsonFile/users.json')

# Load schedules and users
schedules = schedule_database.load_schedules()
users = user_database.load_users()


def getSchedule(workDay):
    s = []
    schedules_sorted = sorted(schedules, key=lambda x: x.user_id)
    users_sorted = sorted(users, key=lambda x: x.id)

    # Iterate over both lists in parallel
    for schedule, user in zip(schedules_sorted, users_sorted):
        #print(f"{user.firstName} {schedule.workdays}")
        if workDay in schedule.workdays:
            day = f"{user.firstName}: {schedule.workdays[workDay]}"
            s.append(day)
    return s



