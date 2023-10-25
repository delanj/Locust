import csv
import pickle
import sys
import cv2
import os

import dlib
import numpy as np

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTableWidgetItem, QTableWidget, QDesktopWidget, QFrame
from PyQt5.QtGui import QPixmap, QImage, QColor, QFont, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
import Entities.IndirectUser.User
import LoginWindow

class CustomWidgetGradient(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(250, 250, 250))
        gradient.setColorAt(1, QColor(230, 230, 230))
        painter.setBrush(gradient)
        painter.drawRect(self.rect())

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
# Link to data base
db = Entities.IndirectUser.User.UserDatabase("../Database/IndirectUsers/jsonFile/users.json")
# Entities
user = Entities.IndirectUser.User.User
class WebcamHandler(QWidget):
    user_updated = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.webcam_label = QLabel(self)
        self.init_webcam()
        layout = QVBoxLayout()
        layout.addWidget(self.webcam_label)
        self.setLayout(layout)
        self.face_detector = dlib.get_frontal_face_detector()
        self.shape_predictor = dlib.shape_predictor("../Database/datFiles/shape_predictor_68_face_landmarks.dat")
        self.face_recognizer = dlib.face_recognition_model_v1(
            "../Database/datFiles/dlib_face_recognition_resnet_model_v1.dat")
        self.known_face_descriptors = self.load_known_face_descriptors()

    def init_webcam(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Unable to access the webcam.")
            return
        self.webcam_timer = QTimer(self)
        self.webcam_timer.timeout.connect(self.update_webcam_feed)
        self.webcam_timer.start(250)  # Update every 50 milliseconds

    def load_known_face_descriptors(self):
        pickle_directory = "../Database/IndirectUsers/face_encodings"
        known_face_descriptors = {}
        for filename in os.listdir(pickle_directory):
            if filename.endswith(".pkl"):
                name = os.path.splitext(filename)[0]
                pickle_path = os.path.join(pickle_directory, filename)

                with open(pickle_path, "rb") as f:
                    known_face_data = pickle.load(f)
                    known_face_descriptors[name] = known_face_data["face_descriptors"]
        return known_face_descriptors

    def recognize_faces(self, frame):
        face_locations = self.face_detector(frame)
        face_names = []

        for face_location in face_locations:
            shape = self.shape_predictor(frame, face_location)
            face_descriptor = self.face_recognizer.compute_face_descriptor(frame, shape)
            match_found = False


            for name, known_descriptors in self.known_face_descriptors.items():
                for known_descriptor in known_descriptors:
                    distance = np.linalg.norm(np.array(known_descriptor) - np.array(face_descriptor))
                    if distance < 0.6:  # Adjust the threshold as needed
                        face_names.append(name)
                        match_found = True
                        break
                if match_found:
                    id = name[:4]
                    for i in db.load_users():
                        if i.id == id:
                            face_names[-1] = f"{i.firstName} {i.lastName}"
                            name = face_names[-1]
                            user = i
                            self.user_updated.emit(user)

                    break

            if not match_found:
                face_names.append("Unknown")
                self.user_updated.emit(None)

            # Draw rectangles and labels on the frame
            left, top, right, bottom = face_location.left(), face_location.top(), face_location.right(), face_location.bottom()
            #cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            if match_found:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 128, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 128, 0), 2)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
                cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        return frame, face_names

    def update_webcam_feed(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_with_faces, face_names = self.recognize_faces(rgb_frame)
            height, width, channel = frame_with_faces.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame_with_faces.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.webcam_label.setPixmap(pixmap)
            if not face_names:
                self.user_updated.emit(False)
class TableView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        table_widget = QTableWidget(self)
        table_widget.setColumnCount(7)
        table_widget.setHorizontalHeaderLabels(
            ["Timestamp", "TechID", "UserID", "FirstName", "LastName", "Company", "Title"])
        table_widget.setStyleSheet("background-color: black;")

        # Read data from CSV file
        data = []
        try:
            with open('../Database/Logs/log.csv', 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                data = list(csvreader)
        except FileNotFoundError:
            print("CSV file not found or path is incorrect.")
            sys.exit(1)

        # Set the number of rows in the table
        table_widget.setRowCount(len(data))

        # Set the column widths to spread them out
        column_widths = [150, 150, 150, 150, 150, 150, 150]  # Adjust these values as needed
        for i in range(len(column_widths)):
            table_widget.setColumnWidth(i, column_widths[i])

        # Populate the table with data
        for i, row in enumerate(data):
            for j, value in enumerate(row):
                item = QTableWidgetItem(value)
                table_widget.setItem(i, j, item)

        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(table_widget)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self, employee=None):
        super().__init__()
        self.employee = employee
        self.showMaximized()
        self.showFullScreen()
        central_widget = CustomWidgetGradient()
        self.setCentralWidget(central_widget)

        fadingLine = FadingLine()

        desktop = QDesktopWidget()
        screen_geometry = QApplication.desktop().screenGeometry()
        screen_width = desktop.screenGeometry().width()
        window_width = screen_geometry.width()

        headerWidget = QWidget()
        headerWidget.setStyleSheet("background-color: white")
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(headerWidget)
        central_layout.setAlignment(Qt.AlignTop)

        mainHeaderLayout = QVBoxLayout(headerWidget)
        headerWidget.setFixedHeight(150)
        headerLayout = QHBoxLayout()
        mainHeaderLayout.addLayout(headerLayout)

        labels_container_size = 200 + 30 + 50
        middleLabels = labels_container_size / 2
        middleWindow = window_width / 2

        # Create a container for the labels
        labels_container = QWidget()
        labels_layout = QHBoxLayout(labels_container)
        labels_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("L")
        label.setStyleSheet(f'font-size: 72pt; font-family: Copperplate; color:black;')
        label.setFixedSize(42, 50)
        image_label = QLabel(self)
        pixmap = QPixmap("Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")  # Replace with your image path
        image_label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setFixedSize(60, 60)
        label2 = QLabel("cUST")
        label2.setStyleSheet(f'font-size: 72pt; font-family: Copperplate; color: black;')
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



        main_layout = QHBoxLayout()

        central_layout.addLayout(main_layout)


        leftLayout = QVBoxLayout()
        leftLayout.setAlignment(Qt.AlignLeft)
        leftLayout.setContentsMargins(0,0,0,0)
        main_layout.addLayout(leftLayout)

        leftWidget = QWidget()
        leftWidget.setStyleSheet("background-color: white;")
        leftLayout.addWidget(leftWidget)

        infoBox = QVBoxLayout(leftWidget)


        #colored_layout = QVBoxLayout(leftWidget)
        leftWidget.setFixedWidth(300)



        self.picture = QLabel(self)
        self.picturePixmap = QPixmap("Picture/file.jpg")
        self.picture.setPixmap(self.picturePixmap.scaled(150, 150))
        self.picture.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.picture.setMaximumHeight(150)
        infoBox.addWidget(self.picture)
        infoBox.addSpacing(10)





        self.name = QLabel("Name:")
        self.name.setAlignment(Qt.AlignTop)
        self.name.setFixedHeight(20)
        self.name.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color:black;')
        infoBox.addWidget(self.name)
        infoBox.addSpacing(5)
        self.nameLabel = QLabel()
        self.nameLabel.setAlignment(Qt.AlignTop)
        self.nameLabel.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black')
        self.nameLabel.setFixedHeight(35)
        infoBox.addWidget(self.nameLabel)
        infoBox.addSpacing(20)

        infoBox.setSpacing(0)

        infoBox.setSpacing(10)


        self.gender = QLabel("Gender:")
        self.gender.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color:black;')
        self.gender.setFixedHeight(20)
        infoBox.addWidget(self.gender)
        self.genderLabel = QLabel()
        self.genderLabel.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black')
        self.genderLabel.setFixedHeight(35)
        infoBox.addWidget(self.genderLabel)
        infoBox.addSpacing(20)

        self.id = QLabel("ID:")
        self.id.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color:black;')
        self.id.setFixedHeight(20)
        infoBox.addWidget(self.id)
        self.idLabel = QLabel()
        self.idLabel.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black')
        self.idLabel.setFixedHeight(35)
        infoBox.addWidget(self.idLabel)
        infoBox.addSpacing(20)

        self.company = QLabel("Company:")
        self.company.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color:black;')
        self.company.setFixedHeight(20)
        infoBox.addWidget(self.company)
        self.companyLabel = QLabel()
        self.companyLabel.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black')
        self.companyLabel.setFixedHeight(35)
        infoBox.addWidget(self.companyLabel)
        infoBox.addSpacing(20)

        self.title = QLabel("Title:")
        self.title.setStyleSheet(f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color:black;')
        self.title.setFixedHeight(20)
        infoBox.addWidget(self.title)
        self.tittleLabel = QLabel()
        self.tittleLabel.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black')
        self.tittleLabel.setFixedHeight(35)
        infoBox.addWidget(self.tittleLabel)
        infoBox.addStretch()

        buttonBox = QHBoxLayout()
        infoBox.addLayout(buttonBox)

        acceptButton = QPushButton("Accept")
        acceptButton.setFixedWidth(100)
        acceptButton.setFixedHeight(40)
        acceptButton.setStyleSheet("background-color: black; color: black; border-radius: 20px; color:white")
        acceptButton.clicked.connect(self.acceptHandle)
        buttonBox.addWidget(acceptButton)

        rejectButton = QPushButton("Reject")
        rejectButton.setFixedWidth(100)
        rejectButton.setFixedHeight(40)
        rejectButton.setStyleSheet("background-color: black; color: black; border-radius: 20px; color:white")
        rejectButton.clicked.connect(self.rejectHandle)
        buttonBox.addWidget(rejectButton)

        #leftLayout.addWidget(leftWidget, alignment=Qt.AlignLeft)


        rightLayout = QVBoxLayout()

        main_layout.addLayout(rightLayout)
        main_layout.addStretch()

        self.webcam_handler = WebcamHandler()
        self.webcam_handler.user_updated.connect(self.updateUser)
        camWidth = window_width - 315
        self.webcam_handler.setFixedSize(int(camWidth), 550)



        rightLayout.addWidget(self.webcam_handler, alignment=Qt.AlignLeft | Qt.AlignTop)


        table_view = TableView()
        table_view.setFixedHeight(175)
        table_view.setFixedWidth(screen_width - 315)

        rightLayout.addStretch()
        rightLayout.addWidget(table_view, alignment=Qt.AlignLeft)

        self.space = QLabel("Title")
        main_layout.addWidget(self.space)



    def updateUser(self, user):
        if user:
            new_pixmap = QPixmap("../Database/IndirectUsers/photos/" + user.photos)  # Load the new image
            self.picture.setPixmap(new_pixmap.scaled(150, 150))
            self.nameLabel.setText(f"{user.firstName} {user.lastName}")
            self.genderLabel.setText(user.gender)
            self.idLabel.setText(user.id)
            self.companyLabel.setText(user.company)
            self.tittleLabel.setText(user.title)
        if not user:
            new_pixmap = QPixmap("Picture/file.jpg")  # Load the new image
            self.picture.setPixmap(new_pixmap.scaled(150, 150))
            self.nameLabel.setText("")
            self.genderLabel.setText("")
            self.idLabel.setText("")
            self.companyLabel.setText("")
            self.tittleLabel.setText("")
        if user == None:
            new_pixmap = QPixmap("Picture/file.jpg")  # Load the new image
            self.picture.setPixmap(new_pixmap.scaled(150, 150))
            self.nameLabel.setText("Unknown")
            self.genderLabel.setText("Unknown")
            self.idLabel.setText("Unknown")
            self.companyLabel.setText("Unknown")
            self.tittleLabel.setText("Unknown")

    def rejectHandle(self):
        self.close()

    def acceptHandle(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
