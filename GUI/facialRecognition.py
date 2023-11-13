import csv
import inspect
import json
import os
import pickle
import shutil
import sys
import traceback
from datetime import datetime, timedelta

import cv2
import dlib
import numpy as np
from IPython.external.qt_for_kernel import QtCore, QtGui
from PyQt5.QtCore import QCoreApplication, QMetaObject, QSize, Qt, QTimer, QDate, QTime, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QFrame, QSizePolicy, QVBoxLayout, QLabel, \
    QPushButton, QLineEdit, QGraphicsOpacityEffect, QSpacerItem, QTabWidget, QTableView, QCalendarWidget, QTextEdit, \
    QFormLayout, QCheckBox, QTimeEdit, QComboBox, QDateTimeEdit, QGridLayout, QHeaderView, QToolButton
from PyQt5.QtCore import QCoreApplication, QMetaObject
from PyQt5.QtWidgets import QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem, QImage, QPalette, QColor, QBrush, QPainter
from PyQt5.uic.properties import QtWidgets
from holoviews.examples.reference.apps.bokeh.player import layout
from matplotlib.figure import Figure
from matplotlib_inline.backend_inline import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from Database.firebaseDatabase import database
import Entities.entitiesMain


from GUI.MainWindow import db
import dashboard
from Entities.Employee import Employee
# Link to data base
dbu = Entities.IndirectUser.User.UserDatabase("../Database/IndirectUsers/jsonFile/users.json")
# Users
User = Entities.IndirectUser.User.User
# Link to data base
dbe = Employee.EmployeeDatabase("../Database/Employees/jsonFile/employee.json")

employee = Employee.Employee

userColumnLength = len(dbu.users)
userRowLength = inspect.getsource(User.__init__).count("self.")

employeeColumnLength = len(dbe.employees)
employeeRowLength = inspect.getsource(employee.__init__).count("self.")
font = "Garamond"
#font = "Copperplate"
tittleFontSize = "36px"
subheaderFontSize = "24px"
bodyFontSize = "18px"
bodySecondaryFontSize = "16px"
buttonFontSize = "16px"
buttonLabelSize = "14px"
captionsFontSize = "12px"
dataTablesFontSize = "14px"
toolTipsFontSize = "16px"

backgroundColorTransparent = "background-color: transparent;"
sidebarColor = "#333940"
iconColor = "white"
sideBarTextColor = "#E0E0E0"

mainBackgroundColor = "#FAFAFA"
contentCardBackgroundColor = "#FEFEFE"

secondaryFontColor = "#4A4A4A"
opacity_effect = QGraphicsOpacityEffect()
opacity_effect.setOpacity(0.5)

buttonColor = "#B0BEC5"

textColor = "#4A4A4A"

bordersLines = "#E0E0E0"





primaryColor = "#333940"
secondaryColor = "rgb(250, 250, 232)"

backgroundColor = "#F5F5F5"
backgroundColor2 = "#ECECEC"





textColorSecondary = "rgb(100, 100, 100)"
accentColor1 = "rgb(200, 200, 200)"
accentColor2 = "rgb(100, 100, 100)"
interactiveElements1 = "rgb(220, 220, 220)"
interactiveElements2 = "rgb(190, 190, 190)"

dataVisualizations = ""

shadowsHighlights = "rgba(0, 0, 0, 0.5)"
fieldBackgroundColor = "rgb(255, 255, 255)"
placeholderColor = "rgb(200, 200, 200)"
buttonBackgroundColor = "rgb(255, 255, 255)"



graph_background_color = (250, 245, 232)
graph_font_color = (74, 74, 74)
graph_bar_color = (176, 190, 197)

search_bar_style = f"""
            QLineEdit {{
                border: 1px solid {bordersLines}; /* Light grey border */
                border-radius: 20px; /* Rounded corners */
                padding: 0 8px; /* Text padding */
                background: {fieldBackgroundColor}; /* White background */
                selection-background-color: {interactiveElements1}; /* Color when text is selected */
                font-size: {bodySecondaryFontSize}; /* Adjust the font size as needed */
                opacity: 0.5;
                color:{textColor}
            }}
            QLineEdit::placeholder {{
                color: {placeholderColor}; /* Replace with your placeholder text color */
                font-style: italic;
                opacity: 0.5;
            }}
            QLineEdit:focus {{
                border: 2px solid {bordersLines}; /* Highlighted border color when focused */

            }}
        """

class Ui_centralWindow(object):
    def setupUi(self, centralWindow, employee=None):

        self.webcam_handler = WebcamHandler()
        # Ensure the central window has an object name
        if not centralWindow.objectName():
            centralWindow.setObjectName("centralWindow")

        # Set the window title and display it in full screen
        centralWindow.setWindowTitle(QCoreApplication.translate("centralWindow", "MainWindow", None))
        centralWindow.showFullScreen()

        # Create the central widget and set its layout
        self.centralwidget = QWidget(centralWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralLayout = QHBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        # Set up the sidebar frame
        self.sideBar = QFrame(self.centralwidget)
        self.sideBar.setObjectName("sideBar")
        self.sideBar.setStyleSheet(f"background-color: {sidebarColor};")
        self.sideBar.setFrameShape(QFrame.StyledPanel)
        self.sideBar.setFrameShadow(QFrame.Raised)
        self.sidebarLayout = QVBoxLayout(self.sideBar)
        self.sidebarLayout.setSpacing(0)
        self.sidebarLayout.setContentsMargins(0, 0, 0, 0)

        # Add logo and navigation widgets to the sidebar
        self.logoWidgetContainer = QWidget(self.sideBar)
        self.logoWidgetContainer.setObjectName("logoWidgetContainer")
        self.logoWidgetUi = Ui_logoWidget()
        self.logoWidgetUi.setupUi(self.logoWidgetContainer)
        self.sidebarLayout.addWidget(self.logoWidgetContainer, stretch=2)

        self.scanInfoContainer = QWidget(self.sideBar)
        self.scanInfoContainer.setObjectName("navigationWidgetContainer")
        self.scanInfoWidgetUi = Ui_scanInfo()
        self.scanInfoWidgetUi.setupUi(self.scanInfoContainer)
        self.sidebarLayout.addWidget(self.scanInfoContainer, stretch=10)
        self.scanInfoWidgetUi.logoutButton.clicked.connect(self.closeCam)



        # Set up the main window frame
        self.mainWindow = QFrame(self.centralwidget)
        self.mainWindow.setObjectName("mainWindow")
        self.mainWindow.setStyleSheet(f"background-color: {mainBackgroundColor};")
        self.mainWindow.setFrameShape(QFrame.StyledPanel)
        self.mainWindow.setFrameShadow(QFrame.Raised)

        # Add user header and display container to the main window
        self.userHeaderContainer = QWidget(self.mainWindow)
        self.userHeaderContainer.setObjectName("userHeaderContainer")
        self.userHeaderUi = Ui_userHeaderWidget()
        self.userHeaderUi.setupUi(self.userHeaderContainer)

        self.displayContainer = QWidget(self.mainWindow)
        self.displayContainer.setObjectName("displayContainer")
        self.displayContainer.setStyleSheet(backgroundColorTransparent)
        self.displayLayout = QVBoxLayout(self.displayContainer)



        # Arrange the main layout with header and display container
        self.mainLayout = QVBoxLayout(self.mainWindow)
        self.mainLayout.addWidget(self.userHeaderContainer, stretch=1)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.displayContainer, stretch=10)

        # Connecting the signals and slots
        self.webcam_handler.setUser.connect(self.setUser)
        self.webcam_handler.user_updated.connect(self.updateUser)

        # Adjusting the size policy of the webcam_label
        self.webcam_handler.webcam_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # Ensuring minimum width for webcam_label (optional but recommended)
        self.webcam_handler.webcam_label.setMinimumWidth(640)

        self.spacer1 = QLabel()
        self.displayLayout.addWidget(self.spacer1, stretch=2)

        # Adding the webcam_handler widget with a stretch factor
        self.displayLayout.addWidget(self.webcam_handler, stretch=20)  # 2/3 of the height

        self.spacer2 = QLabel()
        self.displayLayout.addWidget(self.spacer2, stretch=3)

        # Add sidebar and main window to the central layout
        self.centralLayout.addWidget(self.sideBar, stretch=2)
        self.centralLayout.addWidget(self.mainWindow, stretch=10)


        # Set the central widget of the main window
        centralWindow.setCentralWidget(self.centralwidget)

    def clearDisplayContainer(self):
        # This will remove all widgets from displayLayout
        for i in reversed(range(self.displayLayout.count())):
            widget = self.displayLayout.itemAt(i).widget()
            if widget is not None:
                self.displayLayout.removeWidget(widget)
                widget.deleteLater()

    def setUser(self, user):
        self.current_user = user

    def closeCam(self):
        e = employee
        if hasattr(self, 'webcam_handler'):
            self.webcam_handler.close_webcam()

        self.close()
        # Open the dashboard main window
        self.dashboard_main = dashboard.MainWindow(emp=e)
        self.dashboard_main.show()




    def updateUser(self, user):
        picture = self.scanInfoWidgetUi.picture
        name = self.scanInfoWidgetUi.name
        gender = self.scanInfoWidgetUi.gender
        id = self.scanInfoWidgetUi.id
        company = self.scanInfoWidgetUi.company
        title = self.scanInfoWidgetUi.title


        if user:
            new_pixmap = QPixmap("../Database/IndirectUsers/photos/" + user.photos)  # Load the new image
            picture.setPixmap(new_pixmap.scaled(150, 150))
            name.setText(f"{user.firstName} {user.lastName}")
            gender.setText(user.gender)
            id.setText(user.id)
            company.setText(user.company)
            title.setText(user.title)
        if not user:
            new_pixmap = QPixmap("Picture/file.jpg")  # Load the new image
            picture.setPixmap(new_pixmap.scaled(150, 150))
            name.setText("")
            gender.setText("")
            id.setText("")
            company.setText("")
            title.setText("")
        if user == None:
            new_pixmap = QPixmap("Picture/file.jpg")  # Load the new image
            picture.setPixmap(new_pixmap.scaled(150, 150))
            name.setText("Unknown")
            gender.setText("Unknown")
            id.setText("Unknown")
            company.setText("Unknown")
            title.setText("Unknown")

class Ui_scanInfo(object):
    def setupUi(self, scanInfo):
        if not scanInfo.objectName():
            scanInfo.setObjectName(u"sidebar")
        self.labelStyle = f"color: {sideBarTextColor}; font: 75 {buttonLabelSize} '{font}'; padding-left: 10px;"
        self.fieldStyle = f'background-color: white; padding: 5px; border: 1px solid black; color:black'
        scanInfo.setStyleSheet(u"background-color:transparent;")
        self.mainLayout = QVBoxLayout(scanInfo)
        self.mainLayout.setSpacing(5)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.pictureContainer = QFrame(scanInfo)
        self.pictureContainer.setObjectName(u"pictureContainer")
        self.pictureContainer.setFrameShape(QFrame.StyledPanel)
        self.pictureContainer.setFrameShadow(QFrame.Raised)
        self.pictureLayout = QVBoxLayout(self.pictureContainer)
        self.pictureLayout.setSpacing(5)
        self.pictureLayout.setObjectName(u"pictureLayout")
        self.pictureLayout.setContentsMargins(5, 5, 5, 5)
        self.picture = QLabel()
        self.picturePixmap = QPixmap("Picture/file.jpg")
        self.picture.setPixmap(self.picturePixmap.scaled(150, 150))
        self.picture.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.picture.setMaximumHeight(150)

        self.pictureLayout.addWidget(self.picture, 0, Qt.AlignHCenter)


        self.mainLayout.addWidget(self.pictureContainer, 0, Qt.AlignVCenter)

        self.infoContainer = QFrame(scanInfo)
        self.infoContainer.setObjectName(u"infoContainer")
        self.infoContainer.setFrameShape(QFrame.StyledPanel)
        self.infoContainer.setFrameShadow(QFrame.Raised)
        self.infoLayout = QFormLayout(self.infoContainer)
        self.infoLayout.setObjectName(u"infoLayout")
        self.infoLayout.setHorizontalSpacing(10)
        self.infoLayout.setVerticalSpacing(5)
        self.infoLayout.setContentsMargins(5, 5, 5, 5)



        self.nameLabel = QLabel("Name: ")
        self.nameLabel.setObjectName(u"nameLabel")
        self.nameLabel.setStyleSheet(self.labelStyle)

        self.infoLayout.setWidget(0, QFormLayout.LabelRole, self.nameLabel)

        self.genderLabel = QLabel("Gender: ")
        self.genderLabel.setObjectName(u"genderLabel")
        self.genderLabel.setStyleSheet(self.labelStyle)

        self.infoLayout.setWidget(1, QFormLayout.LabelRole, self.genderLabel)

        self.idLabel = QLabel("ID: ")
        self.idLabel.setObjectName(u"idLabel")
        self.idLabel.setStyleSheet(self.labelStyle)

        self.infoLayout.setWidget(2, QFormLayout.LabelRole, self.idLabel)

        self.companyLabel = QLabel("Company: ")
        self.companyLabel.setObjectName(u"companyLabel")
        self.companyLabel.setStyleSheet(self.labelStyle)

        self.infoLayout.setWidget(3, QFormLayout.LabelRole, self.companyLabel)

        self.titleLabel = QLabel("Title: ")
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setStyleSheet(self.labelStyle)

        self.infoLayout.setWidget(4, QFormLayout.LabelRole, self.titleLabel)

        self.title = QLabel(self.infoContainer)
        self.title.setStyleSheet(self.fieldStyle)

        self.infoLayout.setWidget(4, QFormLayout.FieldRole, self.title)

        self.company = QLabel(self.infoContainer)
        self.company.setStyleSheet(self.fieldStyle)

        self.infoLayout.setWidget(3, QFormLayout.FieldRole, self.company)

        self.id = QLabel(self.infoContainer)
        self.id.setStyleSheet(self.fieldStyle)

        self.infoLayout.setWidget(2, QFormLayout.FieldRole, self.id)

        self.gender = QLabel(self.infoContainer)
        self.gender.setStyleSheet(self.fieldStyle)

        self.infoLayout.setWidget(1, QFormLayout.FieldRole, self.gender)

        self.name = QLabel(self.infoContainer)
        self.name.setStyleSheet(self.fieldStyle)

        self.infoLayout.setWidget(0, QFormLayout.FieldRole, self.name)


        self.mainLayout.addWidget(self.infoContainer)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.mainLayout.addItem(self.verticalSpacer_2)

        self.buttonContainer = QFrame(scanInfo)
        self.buttonContainer.setObjectName(u"buttonContainer")
        self.buttonContainer.setFrameShape(QFrame.StyledPanel)
        self.buttonContainer.setFrameShadow(QFrame.Raised)
        self.buttonLayout = QHBoxLayout(self.buttonContainer)
        self.buttonLayout.setSpacing(5)
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonLayout.setContentsMargins(5, 5, 5, 5)

        self.acceptButton = QPushButton("Accept")
        self.acceptButton = self.create_button("Accept", "acceptButton", "accept-circular-button-outline.png", "green")
        self.buttonLayout.addWidget(self.acceptButton)


        self.rejectButton = self.create_button("Reject", "rejectButton", "cross-button.png", "red")
        self.buttonLayout.addWidget(self.rejectButton)

        self.mainLayout.addWidget(self.buttonContainer)

        self.mainLayout.addSpacing(20)

        self.frame_3 = QFrame(scanInfo)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.frame_3Layout = QVBoxLayout(self.frame_3)
        self.frame_3Layout.setSpacing(5)
        self.frame_3Layout.setObjectName(u"buttonLayout")
        self.frame_3Layout.setContentsMargins(5, 5, 5, 5)

        self.logoutButton = self.create_button("Exit", "logoutButton", "sign-out-alt.png", "white")
        #self.logoutButton.clicked.connect(self.exitButtonHandle)
        self.frame_3Layout.addWidget(self.logoutButton)

        self.mainLayout.addWidget(self.frame_3)

    def create_button(self, text, objectName, iconPath, setColor):
        button = QPushButton()
        button.setObjectName(objectName)
        button.setText(f"{text}")

        # Load the icon
        pixmap = QPixmap(f"buttonIcons/{iconPath}")
        # Create a new pixmap with the same size to apply the color change
        white_pixmap = QPixmap(pixmap.size())
        white_pixmap.fill(QColor('transparent'))  # Start with a transparent pixmap

        # Create a QPainter to draw on the pixmap
        painter = QPainter(white_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, pixmap)  # Draw the original pixmap onto the transparent one
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        # Set the color to white
        painter.fillRect(white_pixmap.rect(), QColor(setColor))
        painter.end()

        # Create the icon with the white pixmap and set it on the button
        button.setIcon(QIcon(white_pixmap))
        button.setIconSize(QSize(20, 20))
        button.setStyleSheet(
            self.button_style('textColor', 'buttonFontSize', 'font', 'interactiveElements1', 'interactiveElements2'))
        button.setMinimumHeight(40)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return button
    def button_style(self, textColor, buttonFontSize, font, interactiveElements1, interactiveElements2):
        return (f"""
            QPushButton {{
                color: {sideBarTextColor}; 
                font: 75 {buttonFontSize} '{font}';
                padding-left: 30px;
                text-align: left;
                border: none;
                background-color: transparent;
            }}
            QPushButton:hover {{
                background-color: {interactiveElements1};
            }}
            QPushButton:pressed {{
                background-color: {interactiveElements2};
            }}
            QPushButton::icon {{
                margin-left: -25px;
                padding-left: 10px;
            }}
        """)

class Ui_logoWidget(object):
    def setupUi(self, logoWidget):
        # Ensure the logo widget has an object name
        if not logoWidget.objectName():
            logoWidget.setObjectName("logoWidget")

        # Set the style of the logo widget
        logoWidget.setStyleSheet(backgroundColorTransparent)

        # Create a horizontal layout for the logo
        self.logoLayout = QHBoxLayout(logoWidget)
        self.logoLayout.setSpacing(0)
        self.logoLayout.setObjectName("logoLayout")
        self.logoLayout.setContentsMargins(0, 0, 0, 0)

        # Initialize the label to hold the logo image
        self.logoImg = QLabel(logoWidget)
        self.logoImg.setObjectName("logoImg")
        self.logoImg.setScaledContents(True)
        self.logoImg.setMaximumSize(80, 80)  # Set the maximum size of the logo

        # Load the logo image and set it to the label
        pixmap = QPixmap("../GUI/Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")
        self.logoImg.setPixmap(pixmap)
        self.logoLayout.addWidget(self.logoImg)  # Add the logo image to the layout

        # Initialize the label for the logo text
        self.logoLabel = QLabel("LocUST")
        self.logoLabel.setObjectName("logoLabel")
        self.logoLabel.setStyleSheet(f"font: 75 {tittleFontSize} '{font}'; color:{sideBarTextColor};")
        self.logoLayout.addWidget(self.logoLabel)  # Add the logo text to the layout

class Ui_userHeaderWidget(object):
    def setupUi(self, userHeaderWidget):
        if not userHeaderWidget.objectName():
            userHeaderWidget.setObjectName(u"userHeaderWidget")

        userHeaderWidget.setStyleSheet(backgroundColorTransparent)
        self.userHeaderLayout = QHBoxLayout(userHeaderWidget)
        self.userHeaderLayout.setSpacing(20)
        self.userHeaderLayout.setObjectName(u"userHeaderLayout")
        self.userHeaderLayout.setContentsMargins(10, 10, 10, 10)

        buttonStyleSheet = f"""
            QPushButton {{
                border: none;
                border-radius: 20px;  /* Half of width and height to make it circular */
                background-color: {buttonColor};  /* Your desired background color for the normal state */
            }}
            QPushButton:hover {{
                background-color: {interactiveElements1};  /* Your desired background color when hovered */
            }}
            QPushButton:pressed {{
                background-color: {interactiveElements2};  /* Your desired background color when pressed */
            }}
        """

        self.searchIcon = QPushButton(userHeaderWidget)
        self.searchIcon.setObjectName(u"searchIcon")
        self.searchIcon.setIcon(QIcon("buttonIcons/search.png"))
        self.searchIcon.setIconSize(QSize(18, 18))
        self.searchIcon.setStyleSheet(buttonStyleSheet)
        self.searchIcon.setFixedSize(40, 40)
        self.userHeaderLayout.addWidget(self.searchIcon)

        self.searchBar = QLineEdit(userHeaderWidget)
        self.searchBar.setObjectName(u"searchBar")
        self.searchBar.setFixedHeight(24)
        search_bar_style = f"""
            QLineEdit {{
                border: 1px solid {bordersLines}; /* Light grey border */
                border-radius: 12px; /* Rounded corners */
                padding: 0 8px; /* Text padding */
                background: {fieldBackgroundColor}; /* White background */
                selection-background-color: {interactiveElements1}; /* Color when text is selected */
                font-size: {bodySecondaryFontSize}; /* Adjust the font size as needed */
                opacity: 0.5;
            }}
            QLineEdit::placeholder {{
                color: {placeholderColor}; /* Replace with your placeholder text color */
                font-style: italic;
                opacity: 0.5;
            }}
            QLineEdit:focus {{
                border: 2px solid {bordersLines}; /* Highlighted border color when focused */

            }}
        """
        palette = self.searchBar.palette()
        palette.setColor(QPalette.PlaceholderText, QColor(placeholderColor))
        self.searchBar.setPalette(palette)
        self.searchBar.setStyleSheet(search_bar_style)
        self.searchBar.setFocusPolicy(Qt.NoFocus)
        self.searchBar.setPlaceholderText("Search...")

        self.userHeaderLayout.addWidget(self.searchBar)

        self.settingsButton = QPushButton(userHeaderWidget)
        self.settingsButton.setObjectName("settingsButton")
        self.settingsButton.setIcon(QIcon("buttonIcons/settings.png"))
        self.settingsButton.setIconSize(QSize(18, 18))
        self.settingsButton.setStyleSheet(buttonStyleSheet)
        self.settingsButton.setFixedSize(40, 40)
        self.userHeaderLayout.addWidget(self.settingsButton)

        self.notificationButton = QPushButton(userHeaderWidget)
        self.notificationButton.setObjectName("notificationButton")
        self.notificationButton.setIcon(QIcon("buttonIcons/bell.png"))  # Replace with your icon's path
        self.notificationButton.setIconSize(QSize(18, 18))  # Icon size
        self.notificationButton.setStyleSheet(buttonStyleSheet)
        self.notificationButton.setFixedSize(40, 40)  # Adjust size as needed
        self.userHeaderLayout.addWidget(self.notificationButton)

        self.employeeProfile = QPushButton(userHeaderWidget)
        self.employeeProfile.setObjectName("employeeProfile")
        self.employeeProfile.setIcon(QIcon("buttonIcons/user.png"))  # Replace with your icon's path
        self.employeeProfile.setIconSize(QSize(18, 18))  # Icon size, adjust as needed
        self.employeeProfile.setStyleSheet(buttonStyleSheet)
        self.employeeProfile.setFixedSize(40, 40)
        self.userHeaderLayout.addWidget(self.employeeProfile)

        self.employeeName = QLabel(userHeaderWidget)
        self.employeeName.setObjectName(u"employeeName")
        self.employeeName.setText("Nickholas Delavallierre")
        self.employeeName.setStyleSheet(f"font: 75 {bodyFontSize} '{font}'; color:{secondaryFontColor};")
        self.userHeaderLayout.addWidget(self.employeeName)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        self.employeeName.setGraphicsEffect(opacity_effect)

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
                    if distance < 0.5:  # Adjust the threshold as needed
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

            # Resize the pixmap to fit the label while maintaining the aspect ratio
            pixmap = pixmap.scaled(self.webcam_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.webcam_label.setPixmap(pixmap)
            self.webcam_label.setAlignment(Qt.AlignCenter)  # Center the pixmap if it doesn't occupy the full space



            if not face_names:
                self.user_updated.emit(False)
                self.setUser.emit(None)

    def close_webcam(self):
        # Stop the timer
        if self.webcam_timer.isActive():
            self.webcam_timer.stop()

        # Release the webcam resource
        if self.cap.isOpened():
            self.cap.release()

        # Optionally, clear the label or display a closing message
        self.webcam_label.clear()
        self.webcam_label.setText("Webcam closed")

class MainWindow(QMainWindow, Ui_centralWindow):
    def __init__(self, emp=None, parent=None):
        super(MainWindow, self).__init__(parent)
        self.employee = emp

        if self.employee:
            print(f"Employee logged in: {self.employee.firstName} {self.employee.lastName}")

            print("face rec window")
            # Adjust all other employee attribute accesses similarly
        self.setupUi(self, self.employee)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
