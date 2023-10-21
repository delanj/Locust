import dlib
import numpy as np
import pickle

# Initialize the face detector, shape predictor, and face recognition model
face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("../FaceRec/dlibpack/shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1("../FaceRec/dlibpack/dlib_face_recognition_resnet_model_v1.dat")

# Path to the single image
image_path = "../Entities/IndirectUser/photos/0001_0.jpg"  # Replace with the path to your image

# Load the image
image = dlib.load_rgb_image(image_path)

# Detect faces in the image
faces = face_detector(image)

# Create a dictionary to store the face descriptors and image path
known_face_data = {
    "name": "Your_Person_Name",
    "face_descriptors": [],
    "image_path": image_path,
}

# Compute face descriptors for each face
for face in faces:
    shape = shape_predictor(image, face)
    face_descriptor = face_recognizer.compute_face_descriptor(image, shape)
    known_face_data["face_descriptors"].append(face_descriptor)

# Save the known_face_data to a pickle file
pickle_file_path = "../Entities/IndirectUser/face_encodings/0001_0.pkl"  # Choose a filename for your pickle file
with open(pickle_file_path, "wb") as f:
    pickle.dump(known_face_data, f)



