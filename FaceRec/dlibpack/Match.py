import dlib
import cv2
import numpy as np
import pickle
import os

# Initialize the face detector, shape predictor, and face recognition model
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Directory containing pickle files with known face descriptors
pickle_directory = "/Users/nick/Desktop/Locust/FaceRec/plkFiles"

# Load known face descriptors from pickle files
known_face_descriptors = {}
for filename in os.listdir(pickle_directory):
    if filename.endswith(".pkl"):
        name = os.path.splitext(filename)[0]
        pickle_path = os.path.join(pickle_directory, filename)

        with open(pickle_path, "rb") as f:
            known_face_data = pickle.load(f)
            known_face_descriptors[name] = known_face_data["face_descriptors"]

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Detect faces in the frame
    faces = face_detector(frame)

    # Compute face descriptors for the detected faces
    for face in faces:
        shape = shape_predictor(frame, face)
        face_descriptor = face_recognizer.compute_face_descriptor(frame, shape)

        # Compare with known face descriptors
        match_found = False
        for name, known_descriptors in known_face_descriptors.items():
            for known_descriptor in known_descriptors:
                distance = np.linalg.norm(np.array(known_descriptor) - np.array(face_descriptor))
                if distance < 0.6:  # Adjust the threshold as needed
                    print(f"Match found with known person: {name}")
                    match_found = True
                    break

            if match_found:
                break

    # Display the frame with rectangles and labels for recognized faces
    for i, face in enumerate(faces):
        left, top, right, bottom = face.left(), face.top(), face.right(), face.bottom()
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        if match_found:
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
