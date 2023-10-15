import csv
import sys
import cv2
import os
import numpy as np
import face_recognition
from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTableWidgetItem, QTableWidget, QDesktopWidget, QFrame
from PyQt5.QtGui import QPixmap, QImage, QColor, QFont
from PyQt5.QtCore import Qt, QTimer
import Entities.IndirectUser.User
import LoginWindow

# Link to data base
db = Entities.IndirectUser.User.UserDatabase("../Entities/IndirectUser/jsonFile/users.json")
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
        # desktop = QDesktopWidget()
        # screen_width = desktop.screenGeometry().width() - 100
        # self.setMaximumWidth(screen_width)
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
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding,tolerance=0.7)
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
        table_widget.setColumnCount(7)
        table_widget.setHorizontalHeaderLabels(["Timestamp", "TechID", "UserID", "FirstName", "LastName", "Company", "Title"])
        table_widget.setStyleSheet("background-color: rgb(60,60,60);")

        # Read data from CSV file
        data = []
        try:
            with open('../Entities/Logs/log.csv', 'r') as csvfile:
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
        self.setWindowTitle("Main Application Window")
        self.showMaximized()
        self.showFullScreen()

        desktop = QDesktopWidget()
        screen_width = desktop.screenGeometry().width()


        central_widget = QWidget()

        central_widget.setStyleSheet("background-color: rgb(36, 36, 36);")
        main_layout = QHBoxLayout(central_widget)

        layout_left = QVBoxLayout()

        colored_widget = QWidget()
        colored_widget.setStyleSheet("background-color: rgb(60, 60, 60);")
        colored_layout = QVBoxLayout(colored_widget)
        colored_widget.setFixedWidth(300)

        # pictureFrame = QFrame(window)
        # pictureFrame.setLayout(layout_left)
        self.picture = QLabel(self)
        self.picturePixmap = QPixmap("Picture/file.jpg")
        self.picture.setPixmap(self.picturePixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.picture.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.picture.setMaximumHeight(200)
        colored_layout.addWidget(self.picture)


        labelFont = QFont()
        labelFont.setPointSize(24)
        labelFont.setBold(True)

        feildFont = QFont()
        feildFont.setPointSize(18)

        colored_layout.setSpacing(0)




        colored_layout.setSpacing(10)
        self.name = QLabel("Name:")
        self.name.setAlignment(Qt.AlignTop)
        self.name.setFont(labelFont)
        self.name.setFixedHeight(25)
        colored_layout.addWidget(self.name)
        colored_layout.addSpacing(5)
        self.nameLabel = QLabel()
        self.nameLabel.setAlignment(Qt.AlignTop)
        self.nameLabel.setFont(feildFont)
        self.nameLabel.setStyleSheet('background-color: darkgray; padding: 5px; border: 1px solid black;')
        self.nameLabel.setFixedHeight(40)
        colored_layout.addWidget(self.nameLabel)
        colored_layout.addSpacing(20)


        self.gender = QLabel("Gender:")
        self.gender.setMargin(0)
        self.gender.setFont(labelFont)
        self.gender.setFixedHeight(25)
        colored_layout.addWidget(self.gender)
        self.genderLabel = QLabel()
        self.genderLabel.setFont(feildFont)
        self.genderLabel.setStyleSheet('background-color: darkgray; padding: 5px; border: 1px solid black;')
        self.genderLabel.setFixedHeight(40)
        colored_layout.addWidget(self.genderLabel)
        colored_layout.addSpacing(20)


        self.id = QLabel("ID:")
        self.id.setMargin(0)
        self.id.setFont(labelFont)
        self.id.setFixedHeight(25)
        colored_layout.addWidget(self.id)
        self.idLabel = QLabel()
        self.idLabel.setFont(feildFont)
        self.idLabel.setStyleSheet('background-color: darkgray; padding: 5px; border: 1px solid black;')
        self.idLabel.setFixedHeight(40)
        colored_layout.addWidget(self.idLabel)
        colored_layout.addSpacing(20)

        self.company = QLabel("Company:")
        self.company.setMargin(0)
        self.company.setFont(labelFont)
        self.company.setFixedHeight(25)
        colored_layout.addWidget(self.company)
        self.companyLabel = QLabel()
        self.companyLabel.setFont(feildFont)
        self.companyLabel.setStyleSheet('background-color: darkgray; padding: 5px; border: 1px solid black;')
        self.companyLabel.setFixedHeight(40)
        colored_layout.addWidget(self.companyLabel)
        colored_layout.addSpacing(20)

        self.title = QLabel("Title:")
        self.title.setMargin(0)
        self.title.setFont(labelFont)
        self.title.setFixedHeight(25)
        colored_layout.addWidget(self.title)
        self.tittleLabel = QLabel()
        self.tittleLabel.setFont(feildFont)
        self.tittleLabel.setStyleSheet('background-color: darkgray; padding: 5px; border: 1px solid black;')
        self.tittleLabel.setFixedHeight(40)
        colored_layout.addWidget(self.tittleLabel)
        colored_layout.addStretch()

        buttonBox = QHBoxLayout()
        colored_layout.addLayout(buttonBox)


        acceptButton = QPushButton("Accept")
        acceptButton.setFixedWidth(75)
        acceptButton.setFixedHeight(30)
        acceptButton.setStyleSheet("background-color: darkgray;")
        acceptButton.clicked.connect(self.acceptHandle)
        buttonBox.addWidget(acceptButton)

        rejectButton = QPushButton("Reject")
        rejectButton.setFixedWidth(75)
        rejectButton.setFixedHeight(30)
        rejectButton.setStyleSheet("background-color: darkgray;")
        rejectButton.clicked.connect(self.rejectHandle)
        buttonBox.addWidget(rejectButton)

        layout_left.addWidget(colored_widget, alignment=Qt.AlignLeft)
        main_layout.addLayout(layout_left)

        layout_right = QVBoxLayout()
        main_layout.addLayout(layout_right)

        self.webcam_handler = WebcamHandler()
        self.webcam_handler.setFixedHeight(600)
        self.webcam_handler.setFixedWidth(screen_width-340)




        # self.webcam_handler.setFixedWidth(500)
        layout_right.addWidget(self.webcam_handler, alignment=Qt.AlignLeft)


        table_view = TableView()
        table_view.setFixedHeight(250)
        table_view.setFixedWidth(screen_width - 340)

        layout_right.addStretch()
        layout_right.addWidget(table_view, alignment=Qt.AlignLeft)


        # self.space = QLabel("Title")
        # main_layout.addWidget(self.space)


        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateUser)
        self.timer.start(1000)  # every 10,000 milliseconds




    def updateUser(self):

        try:
            global indirectUser
            new_pixmap = QPixmap("../Entities/IndirectUser/photos/" + indirectUser.photos[0])  # Load the new image
            self.picture.setPixmap(new_pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
