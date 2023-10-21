import dlib
import cv2
import numpy as np
import pickle

# Initialize the face detector, shape predictor, and face recognition model
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Load known images of individuals
known_images = [dlib.load_rgb_image("../../Database/IndirectUsers/photos/0001_0.jpg"), dlib.load_rgb_image(
    "../../Database/IndirectUsers/photos/0001_1.jpg")]
known_face_descriptors = []

# Compute face descriptors for known individuals
for image in known_images:
    faces = face_detector(image)
    for face in faces:
        shape = shape_predictor(image, face)
        face_descriptor = face_recognizer.compute_face_descriptor(image, shape)
        known_face_descriptors.append(face_descriptor)

# Capture an unknown image from the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default camera, 1 for an external camera

while True:
    ret, frame = cap.read()

    # Detect faces in the unknown image
    unknown_faces = face_detector(frame)

    # Compute face descriptors for unknown faces
    unknown_face_descriptors = []
    for face in unknown_faces:
        shape = shape_predictor(frame, face)
        face_descriptor = face_recognizer.compute_face_descriptor(frame, shape)
        unknown_face_descriptors.append(face_descriptor)

    # Compare unknown face descriptors with known descriptors
    for i, unknown_descriptor in enumerate(unknown_face_descriptors):
        distances = [np.linalg.norm(np.array(known_descriptor) - np.array(unknown_descriptor)) for known_descriptor in known_face_descriptors]

        # Choose a threshold for a match (you can adjust it)
        threshold = 0.6

        if min(distances) < threshold:
            cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)
            cv2.putText(frame, f"Match found with known person {distances.index(min(distances)) + 1}", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        else:
            cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 0, 255), 2)
            cv2.putText(frame, "Unknown Person", (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display the frame with face recognition results
    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit
        break

# Release the webcam and close OpenCV windows
cap.release()
cv2.destroyAllWindows()