import sys
import cv2
from IPython.external.qt_for_kernel import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QFrame, QTableWidgetItem, QTableWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QPainter, QImage, QBitmap, QColor, QPalette, QLinearGradient, QBrush
from PyQt5.QtCore import Qt, QTimer
from Entities.Employee import Employee
import MainWindow
import ManagerWindow
import dashboard
from dashboard import MainWindow



class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.showFullScreen()
        #self.setGeometry(0, 0, 1920, 1080)  # Set your desired screen resolution
        centralWidget = QWidget()

        layout = QVBoxLayout()


        innerWidget = QWidget()
        innerWidget.setStyleSheet("background-color: white; border-radius: 30px;")
        innerLayout = QVBoxLayout(innerWidget)
        innerLayout.setAlignment(Qt.AlignCenter)

        innerWidget.setFixedWidth(350)
        innerWidget.setFixedHeight(600)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(3,3)

        shadowColor = QColor(0, 0, 0)
        #shadow.setColor(shadowColor)
        # adding shadow to the label
        innerWidget.setGraphicsEffect(shadow)

        label = QLabel("LocUST")
        label.setStyleSheet('font-size: 56pt; '
                            'font-family: Copperplate;'
                            'color: black; '
                            'padding: 6px;'
                            'min-width: 10;'
                            'color: black;')

        label.setFixedHeight(75)
        label.setAlignment(Qt.AlignCenter)
        innerLayout.addWidget(label)


        image_label = QLabel(self)
        pixmap = QPixmap("Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")  # Replace with your image path
        image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedHeight(225)
        innerLayout.addWidget(image_label)

        self.invalid = QLabel("")
        self.invalid.setAlignment(Qt.AlignCenter)
        self.invalid.setStyleSheet("color: black;")
        innerLayout.addWidget(self.invalid)
        innerLayout.addSpacing(15)

        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Username")
        self.username_edit.setStyleSheet("background: transparent; border: 1px solid transparent; border-bottom: 1px solid black; "
                                         "selection-background-color: transparent; outline: none; color: black;")
        self.username_edit.setAttribute(Qt.WA_MacShowFocusRect, 0);

        self.username_edit.setFixedWidth(250)
        self.username_edit.setFixedHeight(30)
        innerLayout.addWidget(self.username_edit)
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("Password")
        self.password_edit.setStyleSheet("background: transparent; border: none; border-bottom: 1px solid black; "
                                         "selection-background-color: transparent; color: black; ")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setFixedWidth(250)
        self.password_edit.setFixedHeight(30)
        self.password_edit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        innerLayout.addWidget(self.password_edit)

        layout2 = QHBoxLayout()

        login_button = QPushButton("Login")
        login_button.setFixedWidth(150)
        login_button.setFixedHeight(40)
        login_button.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        login_button.clicked.connect(self.login)

        innerLayout.addSpacing(30)

        layout2.addWidget(login_button)  # Add the button to layout2
        innerLayout.addLayout(layout2)  # Add layout2 to the parent layout
        innerLayout.addSpacing(30)

        copright = QLabel("©2023 LocUST.inc ")
        copright.setStyleSheet("color: black;")
        copright.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        innerLayout.addWidget(copright)



        layout.addWidget(innerWidget, alignment=Qt.AlignCenter)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def login(self):
        dbe = Employee.EmployeeDatabase("../Database/Employees/jsonFile/employee.json")

        username = self.username_edit.text()
        password = self.password_edit.text()

        for i in dbe.load_employees():
            if username == i.employeeID and password == i.passcode:
                employee = i.getEmployee()
                print("Login Successful")
                self.close()
                try:
                    self.dashboard_main = dashboard.MainWindow(emp=employee)
                    self.dashboard_main.show()
                except Exception as e:
                    print("Error opening MainWindow:", e)
            else:
                print("Login Failed")
                self.invalid.setText("Login failed. Please check your credentials.")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showFullScreen()  # Show the window in full screen
    sys.exit(app.exec_())
