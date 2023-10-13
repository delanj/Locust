import cv2

from FaceRec import process_frame, load_face_encodings
from Entities.IndirectUser.User import UserDatabase, User


def faceRecognitionMain():
    """
        Perform face recognition using a webcam and a database of known users.

        This function initializes a webcam, captures video frames, and performs face recognition
        against a database of known users. It returns the user instance of the recognized person.

        Returns:
        - Entities instance: The user instance of the recognized person, or None if no match is found.
        """
    output_file = "../Entities/IndirectUser/face_encodings/"  # Path to the face encoding directory
    user_db = UserDatabase("../Entities/IndirectUser/jsonFile/users.json")  # Initialize the user database


    print(user_db)

    for user_data in user_db.load_users():
        user_instance = User.getUser(user_data)



        # Load known face encodings for the current user
        known_face_encodings = load_face_encodings(output_file + user_instance.faceEncoding)
        print(output_file+user_instance.faceEncoding)

        # Initialize webcam capture
        video_capture = cv2.VideoCapture(0)
        match_found = False
        count = 0

        while True:
            ret, frame = video_capture.read()
            matched_name = process_frame(frame, known_face_encodings, threshold=0.6)

            if matched_name:
                print("Matched")
                return user_instance.getUser()


            if not match_found:
                print("not found")
                count += 1
                if count == 10:
                    break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the webcam and close all windows
        video_capture.release()
        cv2.destroyAllWindows()





if __name__ == "__main__":
    print(faceRecognitionMain().displayUser())
