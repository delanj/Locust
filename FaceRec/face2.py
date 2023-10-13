import cv2
import numpy as np
import face_recognition

# Load the known face encodings and corresponding user names from .npy files
def load_known_faces(file_paths):
    known_face_encodings = []
    known_face_names = []
    for file_path in file_paths:
        data = np.load(file_path, allow_pickle=True)

        # Check the data structure and access it accordingly
        if isinstance(data, np.ndarray) and data.size == 1:
            # If the data is a single-element array, extract the item
            data = data.item()

        # Check if data is a dictionary with 'encoding' and 'name' keys
        if isinstance(data, dict) and 'encoding' in data and 'name' in data:
            known_face_encodings.append(data['encoding'])
            known_face_names.append(data['name'])
        else:
            # Handle the case where the data structure is not as expected
            print(f"Invalid data structure in {file_path}. Skipping this file.")

    return known_face_encodings, known_face_names


# Load the webcam
video_capture = cv2.VideoCapture(0)

# Load the known faces
known_face_encodings, known_face_names = load_known_faces([
    '../Entities/face_encodings/0001.npy',
    '../Entities/face_encodings/0002.npy',
    # Add more .npy files as needed
])

while True:
    # Capture a frame from the webcam
    ret, frame = video_capture.read()

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        # Compare the current face encoding with known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match is found, use the name of the first matching user
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Draw a box and label around the face
        top, right, bottom, left = face_recognition.face_locations(frame)[0]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Display the frame
    cv2.imshow('Video', frame)

    # Break the loop when 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
video_capture.release()
cv2.destroyAllWindows()
