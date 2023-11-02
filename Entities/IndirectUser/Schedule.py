import json
import os

import Database


class Schedule:
    def __init__(self, user_id, workdays):
        self.user_id = user_id
        self.workdays = workdays

class ScheduleDatabase:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.schedules = self.load_schedules()

    def load_schedules(self):
        try:
            with open(self.json_file_path, "r") as json_file:
                schedules_data = json.load(json_file)
            schedules = []
            for schedule_data in schedules_data:
                schedule = Schedule(
                    schedule_data.get("user_id"),
                    schedule_data.get("schedule")  # Notice the key here is "schedule", not "workdays"
                )
                schedules.append(schedule)
            return schedules
        except FileNotFoundError:
            return []
    def save_schedules(self):
        schedules_data = []
        for schedule in self.schedules:
            schedule_data = {
                "user_id": schedule.user_id,
                "schedule": schedule.workdays
            }
            schedules_data.append(schedule_data)
        with open(self.json_file_path, "w") as json_file:
            json.dump(schedules_data, json_file, indent=4)

    def add_schedule(self, schedule):
        self.schedules.append(schedule)
        self.save_schedules()

    def get_schedule_by_user_id(self, user_id):
        for schedule in self.schedules:
            if schedule.user_id == user_id:
                return schedule
        return None

    def edit_schedule(self, user_id, new_workdays):
        for schedule in self.schedules:
            if schedule.user_id == user_id:
                schedule.workdays = new_workdays
                self.save_schedules()
                return True
        return False



