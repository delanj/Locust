import inspect
import json
import os
import cv2
import numpy as np
import face_recognition

class User:
    def __init__(self, id ,firstName, lastName, gender, company, title, photos, faceEncoding):
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.company = company
        self.title = title
        self.photos = photos
        self.faceEncoding = faceEncoding

    def getUser(self):
        person = User(self.id, self.firstName, self.lastName, self.gender,
                      self.company, self.title, self.photos, self.faceEncoding)
        return person


class UserDatabase:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.json_file_path, "r") as json_file:
                users_data = json.load(json_file)
            users = []
            for user_data in users_data:
                user = User(
                    user_data.get("id"),
                    user_data.get("firstName"),
                    user_data.get("lastName"),
                    user_data.get("gender"),
                    user_data.get("company"),
                    user_data.get("title"),
                    user_data.get("photos"),
                    user_data.get("faceEncodings")
                )
                users.append(user)
            return users
        except FileNotFoundError:
            return []

    def save_users(self):
        users_data = []
        for user in self.users:
            user_data = {
                "id": user.id,
                "firstName": user.firstName,
                "lastName": user.lastName,
                "gender": user.gender,
                "company": user.company,
                "title": user.title,
                "photos": user.photos,
                "faceEncodings": user.faceEncoding
            }
            users_data.append(user_data)
        with open(self.json_file_path, "w") as json_file:
            json.dump(users_data, json_file, indent=4)

    def add_user(self, user):
        self.users.append(user)
        self.save_users()

    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def edit_user(self, user_id, new_data):
        for user in self.users:
            if user.id == user_id:
                if "firstName" in new_data:
                    user.firstName = new_data["firstName"]
                if "lastName" in new_data:
                    user.lastName = new_data["lastName"]
                if "gender" in new_data:
                    user.gender = new_data["gender"]
                if "company" in new_data:
                    user.company = new_data["company"]
                if "title" in new_data:
                    user.title = new_data["title"]
                if "photos" in new_data:
                    user.photos = new_data["photos"]
                if "faceEncodings" in new_data:
                    user.faceEncoding = new_data["faceEncodings"]
                self.save_users()
                return True
        return False















