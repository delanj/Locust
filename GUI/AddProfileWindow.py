import os
import sys
import cv2
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QLinearGradient, QColor, QPen
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, \
    QPushButton, QSpacerItem, QSizePolicy, QFrame
import dlib
import pickle
import Entities.IndirectUser.User
import shutil


"""
I want to premake the files load the directory then when accepted move the files to where they need to be

For taking the photo I want it to take the photo and replace the stream with the taken photo and change the button as
an option to retake the photo if retaking the photo the button and stream will go back to normal

get filled in text 
read it when the add button is hit 
place paths in label 

cancel button will exit 


"""
# Link to data base
db = Entities.IndirectUser.User.UserDatabase("../Database/IndirectUsers/jsonFile/users.json")
# Entities
user = Entities.IndirectUser.User.User

class CustomWidgetGradient(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(250, 250, 250))
        gradient.setColorAt(1, QColor(230, 230, 230))
        painter.setBrush(gradient)
        painter.drawRect(self.rect())
class BlackLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(3)
        self.setStyleSheet("color: black; background-color:black;")
        self.setContentsMargins(0,0,0,0)

class FadingLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(3)
        self.setStyleSheet(
            """
            QFrame {
                border: 1px solid transparent;
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 rgba(0, 0, 0, 0), 
                    stop:0.5 black, 
                    stop:0.5 black, 
                    stop:1 rgba(0, 0, 0, 0));
            }
            """
        )

class MainWindow(QMainWindow):
    def __init__(self, employee=None):
        super().__init__()
        screen_geometry = QApplication.desktop().screenGeometry()
        window_width = screen_geometry.width()
        window_height = screen_geometry.height()
        line = BlackLine()
        fadingLine = FadingLine()
        lableColor = "black"

        self.setWindowTitle("Main Application Window")
        self.showMaximized()
        self.showFullScreen()
        central_widget = CustomWidgetGradient()
        central_widget.setStyleSheet("background-color: rgb(230, 230, 230);")
        u_central_layout = QVBoxLayout(central_widget)
        u_central_layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)

        headerWidget = QWidget()
        u_central_layout.addWidget(headerWidget)
        headerWidget.setStyleSheet("background-color: white")
        mainHeaderLayout = QVBoxLayout(headerWidget)


        headerLayout = QHBoxLayout()
        mainHeaderLayout.addLayout(headerLayout)
        headerWidget.setFixedHeight(150)


        labels_container_size = 200 + 30 + 50
        middleLabels = labels_container_size / 2
        middleWindow = window_width / 2






        # Create a container for the labels
        labels_container = QWidget()
        labels_layout = QHBoxLayout(labels_container)
        labels_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("L")
        label.setStyleSheet(f'font-size: 72pt; font-family: Copperplate; color: {lableColor};')
        label.setFixedSize(42, 50)

        image_label = QLabel(self)
        pixmap = QPixmap("Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")  # Replace with your image path
        image_label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setFixedSize(60, 60)

        label2 = QLabel("cUST")
        label2.setStyleSheet(f'font-size: 72pt; font-family: Copperplate; color: {lableColor};')
        label2.setFixedSize(200, 50)

        # Add the labels to the container layout
        labels_layout.addSpacing(int(middleWindow) - int(middleLabels))
        labels_layout.addWidget(label)
        labels_layout.addWidget(image_label)
        labels_layout.addWidget(label2)


        labels_layout.addStretch()
        # Add the labels container to the header layout
        headerLayout.addWidget(labels_container)
        mainHeaderLayout.addWidget(fadingLine)


        mainHeaderLayout.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
















        u_main_layout = QHBoxLayout()
        u_central_layout.addLayout(u_main_layout)

        u_leftLayout = QVBoxLayout()
        u_leftLayout.addSpacing(50)
        u_main_layout.addLayout(u_leftLayout)
        uleftLayoutRow1 = QHBoxLayout()
        uleftLayoutRow2 = QHBoxLayout()
        uleftLayoutRow3 = QHBoxLayout()
        uleftLayoutRow4 = QHBoxLayout()
        u_leftLayout.addLayout(uleftLayoutRow1)
        u_leftLayout.addLayout(uleftLayoutRow2)
        u_leftLayout.addLayout(uleftLayoutRow3)
        u_leftLayout.addLayout(uleftLayoutRow4)

        uleftLayoutRow1.setAlignment(Qt.AlignLeft)
        uleftLayoutRow2.setAlignment(Qt.AlignLeft)
        uleftLayoutRow3.setAlignment(Qt.AlignLeft)
        uleftLayoutRow4.setAlignment(Qt.AlignLeft)



        # id
        idLayout = QVBoxLayout()
        idLabel = QLabel("ID")
        idLabel.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: {lableColor};')
        idLayout.addWidget(idLabel)
        self.idLineEdit = QLineEdit()
        self.idLineEdit.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black')
        self.idLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        self.idLineEdit.setFixedWidth(100)
        idLayout.addWidget(self.idLineEdit)
        uleftLayoutRow1.addLayout(idLayout)
        idLayout.addSpacing(50)
        idLayout.setContentsMargins(10, 10, 10, 10)



        # firstName
        firstNameLayout = QVBoxLayout()
        firstNameLabel = QLabel("First Name")
        firstNameLabel.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: {lableColor};')
        firstNameLayout.addWidget(firstNameLabel)
        self.firstNameLineEdit = QLineEdit()
        self.firstNameLineEdit.setMaximumWidth(250)
        self.firstNameLineEdit.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black')
        self.firstNameLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        firstNameLayout.addWidget(self.firstNameLineEdit)
        uleftLayoutRow2.addLayout(firstNameLayout)
        firstNameLayout.addSpacing(50)
        firstNameLayout.setContentsMargins(10, 10, 10, 10)

        # lastName
        lastNameLayout = QVBoxLayout()
        lastNameLabel = QLabel("Last Name")
        lastNameLabel.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: {lableColor};')
        lastNameLayout.addWidget(lastNameLabel)
        self.lastNameLineEdit = QLineEdit()
        self.lastNameLineEdit.setMaximumWidth(250)
        self.lastNameLineEdit.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.lastNameLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        lastNameLayout.addWidget(self.lastNameLineEdit)
        uleftLayoutRow2.addLayout(lastNameLayout)
        lastNameLayout.addSpacing(50)
        lastNameLayout.setContentsMargins(10, 10, 10, 10)


        # gender
        genderLayout = QVBoxLayout()
        genderLabel = QLabel("Gender")
        genderLabel.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: {lableColor};')
        genderLayout.addWidget(genderLabel)
        self.genderLineEdit = QLineEdit()
        self.genderLineEdit.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.genderLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        self.genderLineEdit.setFixedWidth(100)
        genderLayout.addWidget(self.genderLineEdit)
        uleftLayoutRow2.addLayout(genderLayout)
        genderLayout.addSpacing(50)
        genderLayout.setContentsMargins(10, 10, 10, 10)

        # company
        companyLayout = QVBoxLayout()
        companyLabel = QLabel("Company")
        companyLabel.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: {lableColor};')
        companyLayout.addWidget(companyLabel)
        self.companyLineEdit = QLineEdit()
        self.companyLineEdit.setMaximumWidth(315)
        self.companyLineEdit.setStyleSheet('background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.companyLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        companyLayout.addWidget(self.companyLineEdit)
        uleftLayoutRow3.addLayout(companyLayout)
        companyLayout.addSpacing(50)
        companyLayout.setContentsMargins(10, 10, 10, 10)

        # title
        titleLayout = QVBoxLayout()
        titleLabel = QLabel("Title")
        titleLabel.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: {lableColor};')
        titleLayout.addWidget(titleLabel)
        self.titleLineEdit = QLineEdit()
        self.titleLineEdit.setMaximumWidth(315)
        self.titleLineEdit.setStyleSheet('background-color: white; padding: 5px; border: 1px solid lableColor; color:black')
        self.titleLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        titleLayout.addWidget(self.titleLineEdit)
        uleftLayoutRow3.addLayout(titleLayout)
        titleLayout.addSpacing(50)
        titleLayout.setContentsMargins(10, 10, 10, 10)

        # photos
        photoLayout = QVBoxLayout()
        photoLabel = QLabel("Photo")
        photoLabel.setMaximumWidth(200)
        photoLabel.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: {lableColor};')
        photoLayout.addWidget(photoLabel)
        self.photo = QLabel()
        self.photo.setMaximumWidth(200)
        self.photo.setStyleSheet('background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.photo.setAttribute(Qt.WA_MacShowFocusRect, 0);
        photoLayout.addWidget(self.photo)
        uleftLayoutRow4.addLayout(photoLayout)
        photoLayout.addSpacing(25)
        photoLayout.setContentsMargins(10, 10, 10, 10)

        # faceEncoding
        faceEncodingLayout = QVBoxLayout()
        faceEncodingLabel = QLabel("Face Encoding")
        faceEncodingLabel.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: {lableColor};')
        faceEncodingLayout.addWidget(faceEncodingLabel)
        self.faceEncoding = QLabel()
        self.faceEncoding.setMaximumWidth(200)
        self.faceEncoding.setStyleSheet('background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.faceEncoding.setAttribute(Qt.WA_MacShowFocusRect, 0);
        faceEncodingLayout.addWidget(self.faceEncoding)
        uleftLayoutRow4.addLayout(faceEncodingLayout)
        faceEncodingLayout.addSpacing(25)
        faceEncodingLayout.setContentsMargins(10, 10, 10, 10)







        urightLayout = QVBoxLayout()
        u_main_layout.addLayout(urightLayout)

        urightLayout.addSpacing(50)
        self.webcam_label = QLabel(self)
        self.webcam_label.setStyleSheet("background-color: transparent;")
        self.webcam_label.setFixedSize(700, 500)
        self.webcam_label.setContentsMargins(10, 10, 10, 10)

        urightLayout.addWidget(self.webcam_label)
        self.cap = cv2.VideoCapture(0)
        self.webcam_timer = QTimer(self)
        self.webcam_timer.timeout.connect(self.update_webcam_feed)
        self.webcam_timer.start(50)

        self.captured_photo_label = QLabel(self)
        self.captured_photo_label.setFixedSize(700, 500)
        urightLayout.addWidget(self.captured_photo_label)
        self.captured_photo_label.setVisible(False)

        self.photo_button = QPushButton("Take Photo")
        self.photo_button.setFixedWidth(150)
        self.photo_button.setFixedHeight(40)
        self.photo_button.setStyleSheet("background-color: black; color: black; border-radius: 20px; color:white")
        self.photo_button.clicked.connect(self.togglePhotoCapture)
        #rightLayout.addWidget(self.photo_button)
        takePhotoButtonLayout = QVBoxLayout()
        takePhotoButtonLayout.addWidget(self.photo_button)
        takePhotoButtonLayout.setAlignment(Qt.AlignCenter)
        urightLayout.addLayout(takePhotoButtonLayout)
        urightLayout.addSpacing(50)
        urightLayout.addStretch()

        uleftLayoutRow5 = QHBoxLayout()
        u_leftLayout.addLayout(uleftLayoutRow5)

        addButton = QPushButton("Add")
        addButton.setFixedWidth(150)
        addButton.setFixedHeight(40)
        addButton.setStyleSheet("background-color: black; color: black; border-radius: 20px; color:white;")
        addButton.clicked.connect(self.addUser)
        uleftLayoutRow5.addWidget(addButton)
        uleftLayoutRow5.addSpacing(75)


        cancelButton = QPushButton("Cancel")
        cancelButton.setFixedWidth(150)
        cancelButton.setFixedHeight(40)
        cancelButton.setStyleSheet("background-color: black; color: black; border-radius: 20px; color:white;")
        cancelButton.clicked.connect(self.cancel)
        uleftLayoutRow5.addWidget(cancelButton)
        uleftLayoutRow5.setAlignment(Qt.AlignLeft)
        uleftLayoutRow5.setContentsMargins(10,10,10,10)



        u_leftLayout.addStretch()

        central_widget.setLayout(u_central_layout)


        self.capturing_photo = False

    def update_webcam_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.resize(frame, (700, 500))
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = rgb_frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.webcam_label.setPixmap(pixmap)

    def togglePhotoCapture(self):
        if self.capturing_photo:
            self.capturing_photo = False
            self.captured_photo_label.setVisible(False)
            self.webcam_label.setVisible(True)
            self.photo_button.setText("Take Photo")

            #Clear text
            self.photo.setText("")
            self.faceEncoding.setText("")
            #Remove Files
            self.removeFiles()

        else:
            self.capturing_photo = True
            self.takePhoto()

    def takePhoto(self):
        file_path = f"../Database/AddLocal/{self.idLineEdit.text()}_0.jpg"
        ret, frame = self.cap.read()
        cv2.imwrite(file_path, frame)


        pixmap = QPixmap(file_path)
        self.captured_photo_label.setPixmap(pixmap.scaled(700, 500))
        self.captured_photo_label.setContentsMargins(10, 10, 10, 10)
        self.captured_photo_label.setVisible(True)
        self.webcam_label.setVisible(False)
        self.photo_button.setText("Retake Photo")

        self.photo.setText(f"{self.idLineEdit.text()}_0.jpg")

        # Save plk
        face_detector = dlib.get_frontal_face_detector()
        shape_predictor = dlib.shape_predictor("../Database/datFiles/shape_predictor_68_face_landmarks.dat")
        face_recognizer = dlib.face_recognition_model_v1("../Database/datFiles/dlib_face_recognition_resnet_model_v1.dat")
        # Load the image
        image = dlib.load_rgb_image(file_path)
        faces = face_detector(image) # Detect faces in the image
        # Create a dictionary to store the face descriptors and image path
        known_face_data = {
            "name": f"{self.idLineEdit.text()}_0",
            "face_descriptors": [],
            "image_path": file_path,
        }
        # Compute face descriptors for each face
        for face in faces:
            shape = shape_predictor(image, face)
            face_descriptor = face_recognizer.compute_face_descriptor(image, shape)
            known_face_data["face_descriptors"].append(face_descriptor)
        # Save the known_face_data to a pickle file
        pickle_file_path = f"../Database/AddLocal/{self.idLineEdit.text()}_0.pkl"  # Choose a filename for your pickle file
        with open(pickle_file_path, "wb") as f:
            pickle.dump(known_face_data, f)

        self.faceEncoding.setText(f"{self.idLineEdit.text()}_0.pkl")



    def addUser(self):
        # id, firstName, lastName, gender, company, title, photos, faceEncoding
        newUser = user(id=self.idLineEdit.text(), firstName=self.firstNameLineEdit.text(), lastName=self.lastNameLineEdit.text(),
             gender=self.genderLineEdit.text(), company=self.companyLineEdit.text(), title=self.titleLineEdit.text(),
             photos=self.photo.text(), faceEncoding=self.faceEncoding.text())


        db.add_user(newUser)

        #Move Photo
        self.moveFile(f"../Database/AddLocal/{self.photo.text()}",
                      f"../Database/IndirectUsers/photos/{self.photo.text()}")
        # Move face Encoding
        self.moveFile(f"../Database/AddLocal/{self.faceEncoding.text()}",
                      f"../Database/IndirectUsers/face_encodings/{self.faceEncoding.text()}")






        #self.removeFiles()
        self.close()


    def cancel(self):
        self.removeFiles()
        self.close()

    def removeFiles(self):
        # Delete all files in the temp folder
        folder_path = '../Database/AddLocal'
        if os.path.exists(folder_path):
            files = os.listdir(folder_path)
            for file in files:
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def moveFile(self, source, destination):
        shutil.move(source, destination)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())