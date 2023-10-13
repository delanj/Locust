import sys

import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QFrame, QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QTimer

from Entities.Employee import Employee
import sys
import cv2
import os
import numpy as np
import face_recognition
from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import Entities.IndirectUser.User



class BackgroundWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image_path)
        painter.drawPixmap(self.rect(), pixmap)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(0, 0, 1920, 1080)  # Set your desired screen resolution

        # Create a central widget to hold everything
        central_widget = BackgroundWidget("../Icons/Untitled design (3).png")
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        parent_layout = QVBoxLayout(central_widget)
        parent_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Create a transparent frame to hold the login elements
        frame = QFrame()
        # frame.setStyleSheet("background-color: rgba(0, 0, 0, 150);")  # Adjust transparency as needed
        parent_layout.addWidget(frame)

        # Inside the frame, add your login elements (labels, buttons, etc.)
        inner_layout = QVBoxLayout(frame)
        inner_layout.addSpacing(200)

        label = QLabel("LocUST")
        label.setStyleSheet('font-size: 56pt; '
                            'font-family: Copperplate;'
                            'color: white; '
                            'padding: 6px;'
                            'min-width: 10;')

        label.setFixedHeight(75)
        label.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(label)
        inner_layout.addSpacing(15)

        # Add an image at the top (existing image)
        image_label = QLabel(self)
        pixmap = QPixmap("Icons/Untitled (1) copy.png")  # Replace with your image path
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedHeight(225)

        inner_layout.addWidget(image_label)
        inner_layout.addSpacing(50)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.username_edit.setFixedWidth(300)
        inner_layout.addWidget(self.username_edit)

        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedWidth(300)
        inner_layout.addWidget(self.password_edit)

        inner_layout.addSpacing(25)

        layout2 = QHBoxLayout()  # Create layout2

        login_button = QPushButton("Login")
        login_button.setFixedWidth(150)
        login_button.setStyleSheet("background-color: rgb(105, 105, 105);")

        login_button.clicked.connect(self.login)

        layout2.addWidget(login_button)  # Add the button to layout2

        inner_layout.addLayout(layout2)  # Add layout2 to the parent layout

        inner_layout.setAlignment(Qt.AlignCenter)

        inner_layout.addStretch()

        self.main_window = MainWindow()



    def login(self):
        dbe = Employee.EmployeeDatabase("../../Entities/Employee/jsonFile/employee.json")
        employee = Employee.Employee
        for i in dbe.load_employees():
            username = self.username_edit.text()
            password = self.password_edit.text()
            if username == i.employeeID and password == i.passcode:  # Replace with your actual login logic
                print("Login Successful")
                # global e
                # e = i.getEmployee()
                self.main_window.showFullScreen()
                self.close()  # Close the login window
            else:
                print("Login Failed")


# Link to data base
db = Entities.IndirectUser.User.UserDatabase("../../Entities/IndirectUser/jsonFile/users.json")
# Entities
user = Entities.IndirectUser.User.User

class WebcamHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.webcam_label = QLabel(self)
        self.init_webcam()
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.webcam_label)
        self.setLayout(layout)
        # Initialize variables for facial recognition
        self.known_face_encodings = []
        self.known_face_names = []
        self.process_this_frame = True
        # Load known face encodings and their corresponding names
        self.load_known_face_encodings()
    def init_webcam(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Unable to access the webcam.")
            return
        self.webcam_timer = QTimer(self)
        self.webcam_timer.timeout.connect(self.update_webcam_feed)
        self.webcam_timer.start(50)  # Update every 50 milliseconds
    def load_known_face_encodings(self):
        encodings_directory = "../Entities/IndirectUser/face_encodings"
        for filename in os.listdir(encodings_directory):
            if filename.endswith(".npy"):
                name = os.path.splitext(filename)[0]  # Extract the name from the filename
                face_encoding = np.load(os.path.join(encodings_directory, filename))
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(name)

    def recognize_faces(self, frame):
        # Initialize face_locations and face_names
        face_locations = []
        face_names = []

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        if self.process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    id = name[:4]

                    for i in db.load_users():

                        if i.id == id:
                            global indirectUser
                            indirectUser = i.getUser()
                            face_names.append(i.firstName +" "+i.lastName)


                        # if u.id == id:
                        #     print(u.firstName)
                        #     face_names.append(u.firstName + " " + u.lastName)
                        #     global indirectUser
                        #     indirectUser = u.getUser()



                face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame

    def update_webcam_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_with_faces = self.recognize_faces(frame)  # Perform facial recognition
            height, width, channel = frame_with_faces.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame_with_faces.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.webcam_label.setPixmap(pixmap)


class TableView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        table_widget = QTableWidget(self)
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["Name", "Age", "City"])
        table_widget.setStyleSheet("background-color: rgb(255,255,255);")

        data = [("John", "30", "New York"),
                ("Alice", "25", "Los Angeles"),
                ("Bob", "35", "Chicago"),
                ("Eve", "28", "San Francisco"),
                ("Charlie", "32", "Miami")]

        for i, (name, age, city) in enumerate(data):
            table_widget.insertRow(i)
            table_widget.setItem(i, 0, QTableWidgetItem(name))
            table_widget.setItem(i, 1, QTableWidgetItem(age))
            table_widget.setItem(i, 2, QTableWidgetItem(city))

        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(table_widget)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application Window")
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: rgb(36, 36, 36);")
        main_layout = QHBoxLayout(central_widget)

        layout_left = QVBoxLayout()

        colored_widget = QWidget()
        colored_widget.setStyleSheet("background-color: rgb(105, 105, 105);")
        colored_layout = QVBoxLayout(colored_widget)

        picture = QLabel(self)
        picturePixmap = QPixmap("Picture/file.jpg")
        picture.setPixmap(picturePixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        picture.setAlignment(Qt.AlignCenter)
        colored_layout.addWidget(picture)

        self.nameLabel = QLabel("Name")
        colored_layout.addWidget(self.nameLabel)

        self.genderLabel = QLabel("Gender")
        colored_layout.addWidget(self.genderLabel)

        self.idLabel = QLabel("ID")
        colored_layout.addWidget(self.idLabel)

        self.companyLabel = QLabel("Company")
        colored_layout.addWidget(self.companyLabel)

        self.tittleLabel = QLabel("Title")
        colored_layout.addWidget(self.tittleLabel)

        buttonBox = QHBoxLayout()
        colored_layout.addLayout(buttonBox)

        acceptButton = QPushButton("Accept")
        acceptButton.setFixedWidth(50)
        acceptButton.setStyleSheet("background-color: rgb(105, 105, 105);")
        acceptButton.clicked.connect(self.acceptHandle)
        buttonBox.addWidget(acceptButton)

        rejectButton = QPushButton("Reject")
        rejectButton.setFixedWidth(50)
        rejectButton.setStyleSheet("background-color: rgb(105, 105, 105);")
        rejectButton.clicked.connect(self.rejectHandle)
        buttonBox.addWidget(rejectButton)

        layout_left.addWidget(colored_widget, alignment=Qt.AlignLeft)
        main_layout.addLayout(layout_left)

        layout_right = QVBoxLayout()
        main_layout.addLayout(layout_right)

        self.webcam_handler = WebcamHandler()
        layout_right.addWidget(self.webcam_handler)


        table_view = TableView()
        layout_right.addStretch()
        layout_right.addWidget(table_view, alignment=Qt.AlignBottom)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateUser)
        self.timer.start(1000)  # every 10,000 milliseconds




    def updateUser(self):
        try:
            global indirectUser
            self.nameLabel.setText(indirectUser.firstName + " " + indirectUser.lastName)
            self.genderLabel.setText(indirectUser.gender)
            self.idLabel.setText(indirectUser.id)
            self.companyLabel.setText(indirectUser.company)
            self.tittleLabel.setText(indirectUser.title)
        except:
            pass

    def rejectHandle(self):
        self.close()

    def acceptHandle(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showFullScreen()  # Show the window in full screen
    sys.exit(app.exec_())
