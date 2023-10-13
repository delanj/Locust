import sys

import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QFrame, QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QTimer


class BackgroundWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image_path)
        painter.drawPixmap(self.rect(), pixmap)
class TableView(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QVBoxLayout for the main layout
        layout = QVBoxLayout()

        # Create a QTableWidget
        table_widget = QTableWidget(self)
        table_widget.setColumnCount(3)  # Set the number of columns
        table_widget.setHorizontalHeaderLabels(["Name", "Age", "City"])  # Set column headers

        # Add data to the table
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

        # Set the table to be non-editable
        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        # Add the table to the layout
        layout.addWidget(table_widget)

        # Set the layout for the main widget
        self.setLayout(layout)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application Window")
        self.setGeometry(0, 0, 1920, 1080)

        # Create the central widget
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: rgb(36, 36, 36);")  # Set the background color for the entire central widget

        # Create the main layout
        main_layout = QHBoxLayout(central_widget)

        # Create the left-side layout (VBox)
        layout_left = QVBoxLayout()

        # Create a QWidget for the colored part
        colored_widget = QWidget()
        colored_widget.setStyleSheet("background-color: rgb(105, 105, 105);")  # Set the background color for the colored part
        colored_widget.setMaximumWidth(500)
        colored_widget.setFixedWidth(500)

        # Picture
        picture = QLabel(self)
        picturePixmap = QPixmap("Picture/file.jpg")  # Replace with your image path

        # Resize the picture to 200x200 pixels
        picture.setPixmap(picturePixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        picture.setAlignment(Qt.AlignCenter)
        colored_layout = QVBoxLayout(colored_widget)
        colored_layout.addWidget(picture)

        # Add other labels and buttons here within the colored_widget...
        nameLabel = QLabel("Name")
        colored_layout.addWidget(nameLabel)

        genderLabel = QLabel("Gender")
        colored_layout.addWidget(genderLabel)

        idLabel = QLabel("ID")
        colored_layout.addWidget(idLabel)

        companyLabel = QLabel("Company")
        colored_layout.addWidget(companyLabel)

        tittleLabel = QLabel("Tittle")
        colored_layout.addWidget(tittleLabel)

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

        # Add the colored part (colored_widget) to the layout_left
        layout_left.addWidget(colored_widget, alignment=Qt.AlignLeft)

        main_layout.addLayout(layout_left)  # Add the QVBoxLayout to the QHBoxLayout


        layout_right = QVBoxLayout()
        main_layout.addLayout(layout_right)

        # Webcam Streaming Code
        self.webcam_label = QLabel()
        layout_right.addWidget(self.webcam_label)
        self.init_webcam()

        table_view = TableView()
        layout_right.addWidget(table_view)


        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def init_webcam(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Unable to access the webcam.")
            sys.exit()
        self.webcam_timer = QTimer(self)
        self.webcam_timer.timeout.connect(self.update_webcam_feed)
        self.webcam_timer.start(50)  # Update every 50 milliseconds

    def update_webcam_feed(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert OpenCV BGR image to Qt QImage
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.webcam_label.setPixmap(pixmap)

    def rejectHandle(self):
        self.close()  # Close the application

    def acceptHandle(self):
        self.close()  # Close the application
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
        inner_layout.addSpacing(450)

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

        self.main_window = MainWindow()  # Create an instance of MainWindow

    def login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()

        if username == "" and password == "":  # Replace with your actual login logic
            print("Login Successful")
            self.close()  # Close the login window
            self.main_window.showFullScreen()  # Show the main application window
        else:
            print("Login Failed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showFullScreen()  # Show the window in full screen

    sys.exit(app.exec_())
