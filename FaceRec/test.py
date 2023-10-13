import face_recognition
import cv2
import numpy as np
import os

import Entities.IndirectUser.User

db = Entities.handleUser.UserDatabase("../Entities/IndirectUser/users.json")
user = Entities.handleUser.User

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(1)  # Change this to 1 if you have multiple cameras

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Directory containing .npy files for each person
encodings_directory = "../Entities/face_encodings"

# Load known face encodings and their corresponding names from the directory
known_face_encodings = []
known_face_names = []

for filename in os.listdir(encodings_directory):
    if filename.endswith(".npy"):
        name = os.path.splitext(filename)[0]  # Extract the name from the filename
        face_encoding = np.load(os.path.join(encodings_directory, filename))
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Only process every other frame of video to save time
    if process_this_frame:

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)


        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all the faces in the current frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for any known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, use the name of the first matching person.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                id = name[:4]

                for i in db.load_users():
                    u = user.getUser(i)
                    if u.id == id:
                        face_names.append(u.name)
                        print(u.displayUser())





            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
