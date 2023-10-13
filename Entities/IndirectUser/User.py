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


    def addPhoto(self, user):
        profile = self.get_user_by_id(user)
        profile = User.getUser(profile)
        photos = []
        for filename in os.listdir("../Entities/IndirectUser/photos"):
            if filename.endswith((".jpg", ".jpeg", ".png", ".gif")) and filename.startswith(profile.id):
                photos.append(filename)
        photoName = f"{profile.id}_{len(photos)}.jpg"

        faceEncoding = []
        for filename in os.listdir("../Entities/IndirectUser/face_encodings"):
            if filename.endswith((".npy")) and filename.startswith(profile.id):
                faceEncoding.append(filename)


        file_path = f"../Entities/IndirectUser/photos/{profile.id}_{len(photos)}.jpg"
        try:
            cap = cv2.VideoCapture(0)

            if not cap.isOpened():
                print("Error: Could not open webcam")
                return False

            while True:
                ret, frame = cap.read()
                cv2.imshow("Camera", frame)
                key = cv2.waitKey(1)

                if key == ord('s'):
                    cv2.imwrite(file_path, frame)
                    print(f"Photo saved to {file_path}")
                    photos.append(photoName)
                    break
                # Press 'q' to quit
                elif key == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()


        except Exception as e:
            print(f"Error: {e}")

        input_image_path = f'../Entities/IndirectUser/photos/{photoName}'

        faceEnc = photoName.split(".")
        faceEncodingFile = f"{faceEnc[0]}.npy"
        output_file_path = f'../Entities/IndirectUser/face_encodings/{faceEncodingFile}'

        # Load the input image
        image = face_recognition.load_image_file(input_image_path)

        # Find face locations and encodings
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        if face_encodings:
            # Save the face encoding to a .npy file
            np.save(output_file_path, face_encodings[0])  # Assuming there's only one face in the image

        faceEncoding.append(faceEncodingFile)

        # id ,firstName, lastName, gender, company, title, photos, faceEncoding
        updatedUserData = {
            "firstName": profile.firstName,
            "lastName": profile.lastName,
            "gender": profile.gender,
            "company": profile.company,
            "title": profile.title,
            "photos": photos,
            "faceEncoding": faceEncoding
        }
        self.edit_user(profile.id, updatedUserData)















