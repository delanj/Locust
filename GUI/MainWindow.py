import csv
import pickle
import sys
from datetime import datetime

import cv2
import os

import dlib
import numpy as np

from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTableWidgetItem, QTableWidget, QDesktopWidget, QFrame, QTabWidget, QLineEdit, QTextEdit
from PyQt5.QtGui import QPixmap, QImage, QColor, QFont, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QDate, QTime
import Entities.IndirectUser.User
import LoginWindow


xLarge_font_size = '75px'
large_font_size = '60px'
medium_font_size = '30px'
small_font_size = '25px'
xSmall_font_size = '20px'
tiny_font_size = "18px"

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

class WebcamHandler(QWidget):
    user_updated = pyqtSignal(object)
    setUser = pyqtSignal(object)
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
                            self.setUser.emit(user)


                    break

            if not match_found:
                face_names.append("Unknown")
                self.user_updated.emit(None)
                self.setUser.emit(None)

            # Draw rectangles and labels on the frame
            left, top, right, bottom = face_location.left(), face_location.top(), face_location.right(), face_location.bottom()
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            if match_found:
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            else:
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

            # Resize the pixmap to fit the label while maintaining the aspect ratio
            pixmap = pixmap.scaled(self.webcam_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.webcam_label.setPixmap(pixmap)
            self.webcam_label.setAlignment(Qt.AlignCenter)  # Center the pixmap if it doesn't occupy the full space



            if not face_names:
                self.user_updated.emit(False)
                self.setUser.emit(None)

class CSVViewer(QWidget):
    def __init__(self, csv_path, enable_search=True, parent=None):
        super(CSVViewer, self).__init__(parent)
        self.csv_path = csv_path
        self.enable_search = enable_search
        self._setup_ui()

    def _styleTable(self):
        table_stylesheet = """
            QTableWidget {
                gridline-color: #d4d4d4; /* Light gray gridlines */
                border: none;
                color: black; /* Text color for table items */
                background-color:white;
            }
            QHeaderView::section {
                background-color: #e6e6e6; /* Light gray header */
                padding: 4px;
                border: 1px solid #d4d4d4;
                font-weight: bold;
                color: black; /* Text color for headers */
            }

        """
        searchbar_stylesheet = """
            QLineEdit {
                background-color: white;
                color: black; /* Text color */
                border: 1px solid #d4d4d4; /* Light gray border to match the table gridlines */
                padding: 4px; /* Padding similar to header sections */
            }
            QLineEdit:focus {
                border: 1px solid #a4a4a4; /* Slightly darker border for focus state */
            }
            QLineEdit::placeholder {
                color: #a4a4a4; /* Placeholder text color */
            }
        """
        self.search_line_edit.setStyleSheet(searchbar_stylesheet)
        self.table_widget.setStyleSheet(table_stylesheet)

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        if self.enable_search:
            self.search_line_edit = QLineEdit()
            self.search_line_edit.setPlaceholderText("Search...")
            layout.addWidget(self.search_line_edit)
            self.search_line_edit.textChanged.connect(self._on_search)

        self.table_widget = QTableWidget()
        self._styleTable()
        # Call your _styleTable function if available.
        # self._styleTable()
        self._populate_table_from_csv(self.csv_path)
        layout.addWidget(self.table_widget)

        # Assuming you have a _createButtonLayout function that returns a layout.
        # layout.addLayout(self._createButtonLayout())

        self.setLayout(layout)

    def _populate_table_from_csv(self, csv_path):
        data = []
        try:
            with open(csv_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                data = list(csvreader)
        except FileNotFoundError:
            print("CSV file not found or path is incorrect.")
            return

        if not data:
            print("CSV is empty.")
            return

        headers = data[0]
        self.table_widget.setColumnCount(len(headers))
        self.table_widget.setHorizontalHeaderLabels(headers)

        self.table_widget.setRowCount(len(data) - 1)
        for i, row in enumerate(data[1:]):
            for j, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.table_widget.setItem(i, j, item)

    def _on_search(self):
        # Implement your search logic here.
        # You might need to repopulate or filter the table based on search criteria.
        pass

class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: white")

        # Main layout
        mainLayout = QVBoxLayout(self)
        headerLayout = QHBoxLayout()
        mainLayout.addLayout(headerLayout)


        screen_geometry = QApplication.desktop().screenGeometry()
        window_width = screen_geometry.width()


        middleWindow = window_width / 2

        # Create a container for the labels
        labels_container = QWidget()
        labels_layout = QHBoxLayout(labels_container)
        labels_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("L")
        label.setStyleSheet(f'font-size: 72pt; font-family: Copperplate; color:black;')

        image_label = QLabel(self)
        pixmap = QPixmap("Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")  # Replace with your image path
        image_label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setFixedSize(60, 60)

        label2 = QLabel("cUST")
        label2.setStyleSheet(f'font-size: 72pt; font-family: Copperplate; color: black;')


        # Add the labels to the container layout
        labelsSize = (label.sizeHint().width() + image_label.sizeHint().width() + label2.sizeHint().width()) / 2
        # Set to middle of the window
        labels_layout.addSpacing(int(middleWindow) - int(labelsSize))
        labels_layout.addWidget(label)
        labels_layout.addWidget(image_label)
        labels_layout.addWidget(label2)
        labels_layout.addStretch()
        # Add the labels container to the header layout
        headerLayout.addWidget(labels_container)

        fadingLine = FadingLine()
        mainLayout.addWidget(fadingLine)
        mainLayout.setAlignment(Qt.AlignBottom | Qt.AlignCenter)

class MainWindow(QMainWindow):
    def __init__(self, employee=None):
        super().__init__()
        self.employee = employee
        screen_geometry = QApplication.desktop().screenGeometry()
        self.window_width = int(screen_geometry.width() - 40)
        self.headerWidget = HeaderWidget()
        self.setupUI()

    def setupUI(self):
        self.showMaximized()
        self.showFullScreen()

        central_widget = CustomWidgetGradient()

        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(self.headerWidget)
        central_layout.setAlignment(Qt.AlignTop)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)


        main_layout = QHBoxLayout()
        central_layout.addLayout(main_layout)

        self.webcam_handler = WebcamHandler()
        main_layout.addWidget(self.leftWidgetContainer())
        main_layout.addWidget(self.rightWidgetContainer())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_label)
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(60000)  # Update every 60000 milliseconds (1 minute)

    def leftWidgetContainer(self):
        leftWidget = QWidget()
        leftLayout = QVBoxLayout()
        leftWidget.setLayout(leftLayout)
        leftLayout.setAlignment(Qt.AlignLeft)
        leftLayout.setContentsMargins(0, 0, 0, 0)

        leftWidget.setStyleSheet("background:white;")

        leftWidgetWidth = int(self.window_width / 5)

        leftWidget.setFixedWidth(leftWidgetWidth)

        self.leftTabs = QTabWidget()

        self.leftTabs.setStyleSheet("""

            QTabWidget{
            background:white;
            }
            QTabWidget::pane {
                border-top: 0px solid #C2C7CB;
                background: white; /* Background for the tab content */
            }
            QTabBar::tab {
                background: #E1E1E1; /* Inactive tab color */
                border: 1px solid #C4C4C3;
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                min-width: 50px;
                padding: 5px;
                margin: 2px;
                background-color:black;
                color:white;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background: #F9F9F9; /* Active tab or hover color */
                color:black;

            }
            QTabBar::tab:selected {
                font: bold; /* Font of the active tab */
            }
            QTabBar::tab:only-one {
                margin: 0;
            }
        """)

        def createButton(text, connect):
            button = QPushButton(text)
            button.setFixedSize(100, 40)
            button.setStyleSheet("background-color: black; color: black; border-radius: 20px; color:white")
            button.clicked.connect(connect)
            return button

        def createLabel(text):
            label = QLabel(text)
            label.setStyleSheet(
                f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color:black;')
            label.setAlignment(Qt.AlignTop)
            label.setFixedHeight(30)
            return label  # Added return statement

        def createLabelField():
            label = QLabel()
            label.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black')
            label.setAlignment(Qt.AlignTop)
            label.setFixedHeight(30)
            return label  # Added return statement

        def FaceRecInfo():
            faceRecInfoWidget = QWidget()
            faceRecInfoWidget.setFixedWidth(leftWidgetWidth)


            infoBox = QVBoxLayout()
            faceRecInfoWidget.setLayout(infoBox)

            def dateTimeWidget():
                dateTimeW = QWidget()
                dateTimeL = QVBoxLayout(dateTimeW)
                dateTimeW.setFixedWidth(leftWidgetWidth)


                self.date_label = QLabel(self)
                self.date_label.setStyleSheet(f'font-size:{tiny_font_size}; font-family: Copperplate; color: black;')
                self.update_date_label()

                self.time_label = QLabel(self)
                self.time_label.setStyleSheet(f'font-size: {medium_font_size}; font-family: Copperplate; color: black;')
                self.update_time_label()

                dateTimeL.addWidget(self.date_label)
                dateTimeL.addWidget(self.time_label)
                return dateTimeW

            def infoContiner():

                layout = QVBoxLayout()

                layout.addWidget(dateTimeWidget())

                # Picture
                self.picture = QLabel(self)
                self.picturePixmap = QPixmap("Picture/file.jpg")
                self.picture.setPixmap(self.picturePixmap.scaled(150, 150))
                self.picture.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
                self.picture.setMaximumHeight(150)

                # Name
                self.nameLabel = createLabel("Name: ")
                self.name = createLabelField()

                # Gender
                self.genderLabel = createLabel("Gender: ")
                self.gender = createLabelField()

                # ID
                self.idLabel = createLabel("ID: ")
                self.id = createLabelField()

                # Company
                self.companyLabel = createLabel("Company: ")
                self.company = createLabelField()

                # Title
                self.titleLabel = createLabel("Title: ")
                self.title = createLabelField()

                # Button box
                buttonBox = QHBoxLayout()
                acceptButton = createButton("Accept", self.acceptHandle)
                rejectButton = createButton("Reject", self.rejectHandle)
                buttonBox.addWidget(acceptButton)
                buttonBox.addWidget(rejectButton)

                # Set Layout
                layout.addWidget(self.picture)

                layout.addWidget(self.nameLabel)
                layout.addWidget(self.name)

                layout.addWidget(self.genderLabel)
                layout.addWidget(self.gender)

                layout.addWidget(self.idLabel)
                layout.addWidget(self.id)

                layout.addWidget(self.companyLabel)
                layout.addWidget(self.company)

                layout.addWidget(self.titleLabel)
                layout.addWidget(self.title)
                layout.addStretch()
                layout.addLayout(buttonBox)



                return layout

            infoBox.addLayout(infoContiner())
            infoBox.addSpacing(10)

            return faceRecInfoWidget

        def Nav():
            navWidget = QWidget()

            navBox = QVBoxLayout()

            subject = createLabel("Subject")



            #Layout


            navWidget.setLayout(navBox)
            return navWidget

        def Tickets():
            ticketWidget = QWidget()
            ticketBox = QVBoxLayout()



            try:
                name = createLabel(f"Name: {self.employee.firstName} {self.employee.lastName}")
                id = createLabel(f"ID: {self.employee.employeeID}")
            except:
                name = createLabel("Name: None")
                id = createLabel("ID: None")


            subject = createLabel("Subject: ")
            self.subjectText = QLineEdit()
            self.subjectText.setStyleSheet('background-color: white; padding: 5px; border: 1px solid black; color:black; font-size: 24pt; font-family: Copperplate;')


            description = createLabel("Description: ")
            self.descriptionText = QTextEdit()
            self.descriptionText.setStyleSheet('background-color: white; padding: 5px; border: 1px solid black; color:black; font-size: 24pt; font-family: Copperplate;')

            acceptButton = createButton("Submit",self.submitTicket)


            # Layout
            ticketBox.addWidget(name)
            ticketBox.addWidget(id)
            ticketBox.addWidget(subject)
            ticketBox.addWidget(self.subjectText)
            ticketBox.addWidget(description)
            ticketBox.addWidget(self.descriptionText)
            ticketBox.addWidget(acceptButton)



            ticketWidget.setLayout(ticketBox)

            return ticketWidget

        self.leftTabs.addTab(FaceRecInfo(), "Face Rec")
        self.leftTabs.addTab(Nav(), "Nav")
        self.leftTabs.addTab(Tickets(), "Tickets")
        leftLayout.addWidget(self.leftTabs)

        return leftWidget

    def rightWidgetContainer(self):
        rightWidget = QWidget()
        rightLayout = QVBoxLayout()
        rightWidget.setLayout(rightLayout)
        rightLayout.setAlignment(Qt.AlignLeft)
        rightLayout.setContentsMargins(0, 0, 0, 0)

        self.webcam_handler.setUser.connect(self.setUser)
        self.webcam_handler.user_updated.connect(self.updateUser)
        self.webcam_handler.webcam_label.setFixedSize(640, 480)

        rightLayout.addWidget(self.webcam_handler, alignment=Qt.AlignLeft | Qt.AlignTop)

        self.csv_viewer = CSVViewer("../Database/Logs/log.csv", enable_search=True)

        rightLayout.addWidget(self.csv_viewer)
        return rightWidget

    def updateUser(self, user):
        if user:
            new_pixmap = QPixmap("../Database/IndirectUsers/photos/" + user.photos)  # Load the new image
            self.picture.setPixmap(new_pixmap.scaled(150, 150))
            self.name.setText(f"{user.firstName} {user.lastName}")
            self.gender.setText(user.gender)
            self.id.setText(user.id)
            self.company.setText(user.company)
            self.title.setText(user.title)
        if not user:
            new_pixmap = QPixmap("Picture/file.jpg")  # Load the new image
            self.picture.setPixmap(new_pixmap.scaled(150, 150))
            self.name.setText("")
            self.gender.setText("")
            self.id.setText("")
            self.company.setText("")
            self.title.setText("")
        if user == None:
            new_pixmap = QPixmap("Picture/file.jpg")  # Load the new image
            self.picture.setPixmap(new_pixmap.scaled(150, 150))
            self.name.setText("Unknown")
            self.gender.setText("Unknown")
            self.id.setText("Unknown")
            self.company.setText("Unknown")
            self.title.setText("Unknown")

    def update_date_label(self):
        # Update the QLabel with the current date
        current_date = QDate.currentDate().toString("dddd, MMMM dd, yyyy")
        self.date_label.setText(current_date)
    def update_time_label(self):
        # Update the QLabel with the current time
        current_time = QTime.currentTime().toString("hh:mm AP")
        self.time_label.setText(current_time)

    def rejectHandle(self):
        self.close()

    def setUser(self, user):
        self.current_user = user

    def acceptHandle(self):
        try:
            user = self.current_user

            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

            data_to_append = [formatted_time,
                              self.employee.employeeID,
                              user.id,
                              user.firstName,
                              user.lastName,
                              user.company,
                              user.title]

            with open('../Database/Logs/log.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data_to_append)

        except:
            print("error")

    def submitTicket(self):
        try:
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            print(formatted_time)
            empName = f"{self.employee.firstName} {self.employee.lastName}"
            empID = self.employee.employeeID
            subjectHeader = "Subject: "
            subject = self.subjectText.text()
            descriptionHeader = "Description: "
            description = self.descriptionText.toPlainText()
            print(description)

            fileName = f"../Database/Tickets/{subject}_{str(formatted_time)}.txt"

            with open(fileName, 'w') as file:  # 'a' mode is for appending to the file, use 'w' to overwrite the file
                file.write("Timestamp: " + formatted_time + '\n')
                file.write("Employee Name: " + empName + '\n')
                file.write("Employee ID: " + empID + '\n')
                file.write(subjectHeader + subject + '\n')
                file.write(descriptionHeader + description + '\n')
                file.write('-' * 40 + '\n')  # Add a separator line for clarity

            self.subjectText.clear()
            self.descriptionText.clear()


        except Exception as e:
            print(f"Error: {e}")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
