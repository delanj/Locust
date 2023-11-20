import json
import os


class User:
    """Represents a user of the system"""
    def __init__(self, id: str, first_name: str, last_name: str, gender: str,
                 company: str, title: str, photos: str, face_encoding: str):

        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.company = company
        self.title = title
        self.photos = photos
        self.face_encoding = face_encoding

    def getUser(self):
        """Returns a User object"""
        person = User(self.id, self.first_name, self.last_name, self.gender,
                      self.company, self.title, self.photos, self.face_encoding)
        return person


class UserDatabase:
    """Represents a database of users"""
    def __init__(self):
        """Represents a database of users"""
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        locust_directory = os.path.abspath(os.path.join(current_file_directory, '..', '..'))
        json_file_path = os.path.join(locust_directory, "Database", "DatabaseIndirectUsers", "jsonFile", "users.json")

        self.json_file_path = json_file_path
        self.users = self.load_users()

    def load_users(self):
        """Loads users from the json file and returns a list of User objects"""
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
        """Saves users to the json file with error handling."""
        users_data = []
        for user in self.users:
            user_data = {
                "id": user.id,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "gender": user.gender,
                "company": user.company,
                "title": user.title,
                "photos": user.photos,
                "faceEncodings": user.face_encoding
            }
            users_data.append(user_data)

        try:
            with open(self.json_file_path, "w") as json_file:
                json.dump(users_data, json_file, indent=4)
        except IOError as e:
            print(f"Error saving users to file: {e}")

    def add_user(self, user):
        """Adds a user to the database"""
        self.users.append(user)
        self.save_users()

    def get_user_by_id(self, user_id):
        """Returns a user with the given id"""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

















