import sys

import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QFrame, QTableWidgetItem, QTableWidget
from PyQt5.QtGui import QPixmap, QPainter, QImage
from PyQt5.QtCore import Qt, QTimer

from Entities.Employee import Employee
import MainWindow



class BackgroundWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.opacity = 100

    def setOpacity(self, opacity):
        self.opacity = opacity
        self.update()  # Call update to trigger a repaint


    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.image_path)

        # Apply opacity
        #painter.setOpacity(self.opacity)

        painter.drawPixmap(self.rect(), pixmap)

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(0, 0, 1920, 1080)  # Set your desired screen resolution

        # Create a central widget to hold everything
        central_widget = BackgroundWidget("Icons/276b002d-a460-4fa9-96db-a69f4fee3b71.jpg")
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        parent_layout = QVBoxLayout(central_widget)
        parent_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins

        # Create a transparent frame to hold the login elements
        frame = QFrame()
        frame.setStyleSheet("background-color: rgba(0, 0, 0, 150);")  # Black box with transparency
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
        pixmap = QPixmap("Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.jpg")  # Replace with your image path
        image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
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
        login_button.setStyleSheet("background-color: rgb(0, 0, 0);")
        login_button.clicked.connect(self.login)

        layout2.addWidget(login_button)  # Add the button to layout2

        inner_layout.addLayout(layout2)  # Add layout2 to the parent layout

        inner_layout.setAlignment(Qt.AlignCenter)

        inner_layout.addStretch()









    def login(self):
        dbe = Employee.EmployeeDatabase("../Entities/Employee/jsonFile/employee.json")
        employee = Employee.Employee
        global e

        for i in dbe.load_employees():



            username = self.username_edit.text()
            password = self.password_edit.text()

            if username == i.employeeID and password == i.passcode:  # Replace with your actual login logic
                print("Login Successful")

                e = i.getEmployee()
                self.w = MainWindow.MainWindow(e)
                self.w.showFullScreen()
                self.close()  # Close the login window



            else:
                print("Login Failed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showFullScreen()  # Show the window in full screen

    sys.exit(app.exec_())
