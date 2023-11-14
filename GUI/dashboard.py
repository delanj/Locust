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
from Entities.Employee import Employee
from Entities import entitiesMain

from GUI import facialRecognition
import LoginWindow
# Link to data base
dbu = Entities.IndirectUser.User.UserDatabase("../Database/IndirectUsers/jsonFile/users.json")
# Users
User = Entities.IndirectUser.User.User
# Link to data base
dbe = Employee.EmployeeDatabase("../Database/Employees/jsonFile/employee.json")

e = Employee.Employee


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

interactiveElements1 = "rgb(220, 220, 220)"
interactiveElements2 = "rgb(190, 190, 190)"

dataVisualizations = ""

shadowsHighlights = "rgba(0, 0, 0, 0.5)"
fieldBackgroundColor = "rgb(255, 255, 255)"
placeholderColor = "rgb(200, 200, 200)"




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

        self.employee = employee

        # Ensure the central window has an object name
        if not centralWindow.objectName():
            centralWindow.setObjectName("centralWindow")

        print(self.employee.employeeID)

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

        self.navigationWidgetContainer = QWidget(self.sideBar)
        self.navigationWidgetContainer.setObjectName("navigationWidgetContainer")
        self.navigationWidgetUi = Ui_navigationWidget()
        self.navigationWidgetUi.setupUi(self.navigationWidgetContainer)
        self.sidebarLayout.addWidget(self.navigationWidgetContainer, stretch=10)

        # Connect navigation buttons to their respective slot functions
        self.navigationWidgetUi.logsButton.clicked.connect(self.showLogsWidget)
        self.navigationWidgetUi.dashboardButton.clicked.connect(self.showDashBoardWidget)
        self.navigationWidgetUi.scheduleButton.clicked.connect(self.showScheduleWidget)
        self.navigationWidgetUi.ticketsButton.clicked.connect(self.showTicketWidget)
        self.navigationWidgetUi.addUserButton.clicked.connect(self.showAddUserWidget)
        self.navigationWidgetUi.logoutButton.clicked.connect(self.logout)
        self.navigationWidgetUi.faceRecButton.clicked.connect(self.faceRec)

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
        if employee:
            self.userHeaderUi.employeeName.setText(f"{employee.firstName} {employee.lastName}")

        self.displayContainer = QWidget(self.mainWindow)
        self.displayContainer.setObjectName("displayContainer")
        self.displayContainer.setStyleSheet(backgroundColorTransparent)
        self.displayLayout = QVBoxLayout(self.displayContainer)

        # Set up the dashboard widget within the display container
        self.dashboardWidgetContainer = QWidget(self.displayContainer)
        self.dashboardWidgetContainer.setObjectName("dashboardWidgetContainer")
        self.dashboardUi = Ui_dashboardWidget()
        self.dashboardUi.setupUi(self.dashboardWidgetContainer)
        self.displayLayout.addWidget(self.dashboardWidgetContainer)

        # Arrange the main layout with header and display container
        self.mainLayout = QVBoxLayout(self.mainWindow)
        self.mainLayout.addWidget(self.userHeaderContainer, stretch=1)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.displayContainer, stretch=10)

        # Add sidebar and main window to the central layout
        self.centralLayout.addWidget(self.sideBar, stretch=2)
        self.centralLayout.addWidget(self.mainWindow, stretch=10)

        # Set the central widget of the main window
        centralWindow.setCentralWidget(self.centralwidget)
        self.employeeView()

    def employeeView(self):
        if self.employee:
            if self.employee.title == "Security Manager":
                self.navigationWidgetUi.logsButton.setEnabled(True)
                self.navigationWidgetUi.scheduleButton.setEnabled(True)
                self.navigationWidgetUi.ticketsButton.setEnabled(True)
                self.navigationWidgetUi.addUserButton.setEnabled(True)

                self.navigationWidgetUi.logoutButton.setEnabled(True)
                self.navigationWidgetUi.faceRecButton.setEnabled(True)
                self.navigationWidgetUi.dashboardButton.setEnabled(True)

            if self.employee.title == "Desk Technician":
                self.navigationWidgetUi.logsButton.setEnabled(False)
                self.navigationWidgetUi.scheduleButton.setEnabled(True)
                self.navigationWidgetUi.ticketsButton.setEnabled(False)
                self.navigationWidgetUi.addUserButton.setEnabled(False)

                self.navigationWidgetUi.logoutButton.setEnabled(True)
                self.navigationWidgetUi.faceRecButton.setEnabled(True)
                self.navigationWidgetUi.dashboardButton.setEnabled(True)


    def clearDisplayContainer(self):
        # This will remove all widgets from displayLayout
        for i in reversed(range(self.displayLayout.count())):
            widget = self.displayLayout.itemAt(i).widget()
            if widget is not None:
                self.displayLayout.removeWidget(widget)
                widget.deleteLater()

    def showDashBoardWidget(self):
        try:
            # Clear any widgets that might be in the displayContainer
            self.clearDisplayContainer()

            # Create and set up the logs widget
            self.dashboardWidgetContainer = QWidget(self.displayContainer)
            self.dashboardWidgetContainer.setObjectName("dashboardWidgetContainer")
            self.dashboardUi = Ui_dashboardWidget()  # Instantiate your Dashboard UI class
            self.dashboardUi.setupUi(self.dashboardWidgetContainer)  # Set up the dashboard UI
            self.displayLayout.addWidget(self.dashboardWidgetContainer)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  # This will print the stack trace.

    def showLogsWidget(self):
        try:
            # Clear any widgets that might be in the displayContainer
            self.clearDisplayContainer()

            # Create and set up the logs widget
            self.logsWidgetContainer = QWidget(self.displayContainer)
            self.logsWidgetContainer.setObjectName("logsWidgetContainer")
            self.logsUi = Ui_logs()
            self.logsUi.setupUi(self.logsWidgetContainer)
            self.displayLayout.addWidget(self.logsWidgetContainer)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  # This will print the stack trace.

    def showScheduleWidget(self):
        try:
            # Clear any widgets that might be in the displayContainer
            self.clearDisplayContainer()

            # Create and set up the logs widget
            self.scheduleWidgetContainer = QWidget(self.displayContainer)
            self.scheduleWidgetContainer.setObjectName("scheduleWidgetContainer")
            self.scheduleUi = Ui_scheduleWidget()
            self.scheduleUi.setupUi(self.scheduleWidgetContainer)
            self.displayLayout.addWidget(self.scheduleWidgetContainer)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  # This will print the stack trace.

    def showTicketWidget(self):
        try:
            # Clear any widgets that might be in the displayContainer
            self.clearDisplayContainer()

            # Create and set up the logs widget
            self.ticketWidgetContainer = QWidget(self.displayContainer)
            self.ticketWidgetContainer.setObjectName("ticketWidgetContainer")
            self.ticketUi = Ui_ticketsWidget()
            self.ticketUi.setupUi(self.ticketWidgetContainer)
            self.displayLayout.addWidget(self.ticketWidgetContainer)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  # This will print the stack trace.

    def showAddUserWidget(self):

        try:
            # Clear any widgets that might be in the displayContainer
            self.clearDisplayContainer()

            # Create and set up the logs widget
            self.addUserWidgetContainer = QWidget(self.displayContainer)
            self.addUserWidgetContainer.setObjectName("addUserWidgetContainer")
            self.addUserUi = Ui_addUserWidget()
            self.addUserUi.setupUi(self.addUserWidgetContainer)
            self.displayLayout.addWidget(self.addUserWidgetContainer)
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()  # This will print the stack trace.

    def logout(self):
        self.close()
        # Open the dashboard main window
        self.login_main = LoginWindow.LoginWindow()
        self.login_main.show()
    def faceRec(self):

        self.close()
        # Open the dashboard main window
        self.dashboard_main = facialRecognition.MainWindow(emp=self.employee)
        self.dashboard_main.show()

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

class Ui_navigationWidget(object):

    def setupUi(self, navigationWidget):
        if not navigationWidget.objectName():
            navigationWidget.setObjectName("navigationWidget")
        navigationWidget.setStyleSheet(backgroundColorTransparent)

        self.navigationLayout = QVBoxLayout(navigationWidget)
        self.navigationLayout.setSpacing(0)
        self.navigationLayout.setContentsMargins(0, 5, 0, 5)

        # Create navigation buttons and labels
        self.mainMenuLabel = self.create_label("Main Menu", "mainMenuLabel")
        self.dashboardButton = self.create_button("Dashboard", "dashboardButton", "home.png")
        self.inboxButton = self.create_button("Inbox", "inboxButton", "paper-plane.png")
        self.workspaceLabel = self.create_label("Workspace", "workspaceLabel")
        self.ticketsButton = self.create_button("Tickets", "ticketsButton", "receipt.png")
        self.scheduleButton = self.create_button("Schedule", "scheduleButton", "calendar.png")
        self.logsButton = self.create_button("Logs", "logsButton", "document.png")
        self.addUserButton = self.create_button("Add User", "addUserButton", "user-add.png")
        self.generalLabel = self.create_label("General", "generalLabel")
        self.faceRecButton = self.create_button("Facial Recognition", "faceRecButton", "face-viewfinder.png")
        self.logoutButton = self.create_button("Logout", "logoutButton", "sign-out-alt.png")

        self.navigationLayout.addWidget(self.mainMenuLabel)
        self.navigationLayout.addWidget(self.dashboardButton)
        self.navigationLayout.addWidget(self.inboxButton)
        self.navigationLayout.addWidget(self.workspaceLabel)
        self.navigationLayout.addWidget(self.ticketsButton)
        self.navigationLayout.addWidget(self.scheduleButton)
        self.navigationLayout.addWidget(self.logsButton)
        self.navigationLayout.addWidget(self.addUserButton)
        self.navigationLayout.addWidget(self.generalLabel)
        self.navigationLayout.addWidget(self.faceRecButton)
        self.navigationLayout.addWidget(self.logoutButton)

    def create_button(self, text, objectName, iconPath):
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
        painter.fillRect(white_pixmap.rect(), QColor(f'{iconColor}'))
        painter.end()

        # Create the icon with the white pixmap and set it on the button
        button.setIcon(QIcon(white_pixmap))
        button.setIconSize(QSize(20, 20))
        button.setStyleSheet(
            self.button_style('textColor', 'buttonFontSize', 'font', 'interactiveElements1', 'interactiveElements2'))
        button.setMinimumHeight(40)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return button

    def create_label(self, text, objectName):
        label = QLabel()
        label.setObjectName(objectName)
        label.setText(text)
        label.setStyleSheet(f"color: {sideBarTextColor}; font: 75 {buttonLabelSize} '{font}'; padding-left: 10px;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return label

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
        self.employeeName.setText("None")
        self.employeeName.setStyleSheet(f"font: 75 {bodyFontSize} '{font}'; color:{secondaryFontColor};")
        self.userHeaderLayout.addWidget(self.employeeName)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        self.employeeName.setGraphicsEffect(opacity_effect)

class Ui_dashboardWidget(object):
    def setupUi(self, dashboardWidget):
        self.containerStylesheet = f"""
            QFrame {{
                background-color: {contentCardBackgroundColor};
                border: 2px solid {bordersLines};
                border-radius: 20px;
            }}
        """
        self.font1 = f"""
            QLabel {{
            font: 75 {subheaderFontSize} "{font}";
            color: {textColor};
            background-color: transparent;
            border: none;
            border-radius: 20px;
        }}"""
        self.font2 = f"""
            QLabel {{
            color: {textColor};
            font: 75 {bodyFontSize} "{font}";
            background-color: transparent;
            border: none;
            border-radius: 20px;
        }}"""
        self.noneStyle = "background-color: transparent; border: none; border-radius: 20px;"

        # Dashboard widget
        dashboardWidget.setObjectName(u"dashboardWidget")
        dashboardWidget.setStyleSheet(backgroundColorTransparent)
        self.dashboardLayout = QHBoxLayout(dashboardWidget)
        self.dashboardLayout.setSpacing(10)
        self.dashboardLayout.setContentsMargins(10, 10, 10, 10)

        # Left Frame
        self.leftFrame = QFrame(dashboardWidget)
        self.leftFrame.setObjectName(u"leftFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftFrame.sizePolicy().hasHeightForWidth())
        self.leftFrame.setSizePolicy(sizePolicy)
        self.leftLayout = QVBoxLayout(self.leftFrame)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)

        # Row 1 Container
        self.row1Container = QFrame(self.leftFrame)
        self.row1Layout = QHBoxLayout(self.row1Container)

        # Date Time widget
        self.dateTimeWidget = QFrame()
        self.dateTimeWidget.setObjectName(u"dateTimeWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.dateTimeWidget.sizePolicy().hasHeightForWidth())
        self.dateTimeWidget.setSizePolicy(sizePolicy4)
        self.dateTimeWidget.setStyleSheet(self.containerStylesheet)
        self.dateTimeWidget.setFrameShape(QFrame.StyledPanel)
        self.dateTimeWidget.setFrameShadow(QFrame.Raised)
        self.dateTimeLayout = QVBoxLayout(self.dateTimeWidget)
        self.dateTimeLayout.setSpacing(0)
        self.dateTimeLayout.setContentsMargins(10, 10, 10, 10)

        # Date Label
        self.dateLabel = QLabel(self.dateTimeWidget)
        self.dateLabel.setObjectName(u"dateLabel")
        self.dateLabel.setStyleSheet(self.font2)
        self.dateLabel.setTextFormat(Qt.PlainText)
        self.update_date_label()
        self.dateTimeLayout.addWidget(self.dateLabel)

        # Time Label
        self.timeLabel = QLabel(self.dateTimeWidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setStyleSheet(self.font1)
        self.timeLabel.setTextFormat(Qt.PlainText)
        self.update_time_label()
        self.dateTimeLayout.addWidget(self.timeLabel)

        # Ticket Container
        self.ticketContainer = QFrame()
        self.ticketContainer.setObjectName(u"ticketsNumContainer")
        sizePolicy4.setHeightForWidth(self.ticketContainer.sizePolicy().hasHeightForWidth())
        self.ticketContainer.setSizePolicy(sizePolicy4)
        self.ticketContainer.setStyleSheet(self.containerStylesheet)
        self.ticketContainer.setFrameShape(QFrame.StyledPanel)
        self.ticketContainer.setFrameShadow(QFrame.Raised)
        self.ticketLayout = QVBoxLayout(self.ticketContainer)
        self.ticketLayout.setSpacing(10)
        self.ticketLayout.setContentsMargins(10, 10, 10, 10)

        # Ticket Label
        self.currentTicketLabel = QLabel(self.ticketContainer)
        self.currentTicketLabel.setObjectName(u"currentTicketLabel")
        self.currentTicketLabel.setStyleSheet(self.font1)
        self.currentTicketLabel.setTextFormat(Qt.PlainText)
        self.currentTicketLabel.setText("Current Tickets")
        self.ticketLayout.addWidget(self.currentTicketLabel, 0, Qt.AlignHCenter)

        # Number of Tickets Label
        self.currentNumOfTickets = QLabel(self.ticketContainer)
        self.currentNumOfTickets.setObjectName(u"currentNumOfTickets")
        self.currentNumOfTickets.setStyleSheet(self.font2)
        self.currentNumOfTickets.setFrameShadow(QFrame.Raised)
        self.currentNumOfTickets.setTextFormat(Qt.PlainText)
        self.currentNumOfTickets.setText("0")
        self.ticketLayout.addWidget(self.currentNumOfTickets, 0, Qt.AlignHCenter)

        # Row 1 Add Widgets
        self.row1Layout.addWidget(self.dateTimeWidget)
        self.row1Layout.addWidget(self.ticketContainer)

        self.leftLayout.addWidget(self.row1Container)


        # Scan Info Widget
        self.scanInfoWidget = QFrame(self.leftFrame)
        self.scanInfoWidget.setObjectName(u"scanInfoWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setHeightForWidth(self.scanInfoWidget.sizePolicy().hasHeightForWidth())
        self.scanInfoWidget.setSizePolicy(sizePolicy1)
        self.scanInfoWidget.setFrameShape(QFrame.StyledPanel)
        self.scanInfoWidget.setFrameShadow(QFrame.Raised)
        self.scanInfoLayout = QHBoxLayout(self.scanInfoWidget)

        # User Widget
        self.userContainer = QFrame()
        self.userContainer.setObjectName(u"iunContainer")
        self.userContainer.setStyleSheet(self.containerStylesheet)
        self.userContainer.setFrameShape(QFrame.StyledPanel)
        self.userContainer.setFrameShadow(QFrame.Raised)
        self.userLayout = QVBoxLayout(self.userContainer)
        self.userLayout.setSpacing(10)
        self.userLayout.setContentsMargins(10, 10, 10, 10)
        # User Label
        self.userLabel = QLabel("Users")
        self.userLabel.setObjectName(u"iULabel")
        self.userLabel.setStyleSheet(self.font1)
        self.userLabel.setTextFormat(Qt.PlainText)
        self.userLayout.addWidget(self.userLabel, 0, Qt.AlignHCenter)
        # User Number Label
        self.userNumberLabel = QLabel("0")
        self.userNumberLabel.setObjectName(u"iUNumber")
        self.userNumberLabel.setStyleSheet(self.font2)
        self.userNumberLabel.setTextFormat(Qt.PlainText)
        self.userLayout.addWidget(self.userNumberLabel, 0, Qt.AlignHCenter)
        self.scanInfoLayout.addWidget(self.userContainer)

        # User Scheduled For Today Container
        self.usersScheduledTodayContainer = QFrame(self.scanInfoWidget)
        self.usersScheduledTodayContainer.setObjectName(u"canScanTodayContainer")
        self.usersScheduledTodayContainer.setStyleSheet(self.containerStylesheet)
        self.usersScheduledTodayContainer.setFrameShape(QFrame.StyledPanel)
        self.usersScheduledTodayContainer.setFrameShadow(QFrame.Raised)
        self.usersScheduledTodayLayout = QVBoxLayout(self.usersScheduledTodayContainer)
        self.usersScheduledTodayLayout.setSpacing(10)
        self.usersScheduledTodayLayout.setObjectName(u"canScanTodayLayout")
        self.usersScheduledTodayLayout.setContentsMargins(10, 10, 10, 10)
        # User Scheduled Today Label
        self.usersScheduledTodayLabel = QLabel("Scheduled For Today")
        self.usersScheduledTodayLabel.setObjectName(u"userScheduleTodayLabel")
        self.usersScheduledTodayLabel.setStyleSheet(self.font1)
        self.usersScheduledTodayLabel.setTextFormat(Qt.PlainText)
        self.usersScheduledTodayLayout.addWidget(self.usersScheduledTodayLabel, 0, Qt.AlignHCenter)
        # User Scheduled Today Number Label
        self.usersScheduledTodayNumberLabel = QLabel("0")
        self.usersScheduledTodayNumberLabel.setObjectName(u"userScheduleTodayNumber")
        self.usersScheduledTodayNumberLabel.setStyleSheet(self.font2)
        self.usersScheduledTodayNumberLabel.setTextFormat(Qt.PlainText)
        self.usersScheduledTodayLayout.addWidget(self.usersScheduledTodayNumberLabel, 0, Qt.AlignHCenter)

        self.scanInfoLayout.addWidget(self.usersScheduledTodayContainer)

        # Scanned Today Container
        self.scannedTodayContainer = QFrame(self.scanInfoWidget)
        self.scannedTodayContainer.setObjectName(u"scansTodayWidget")
        self.scannedTodayContainer.setStyleSheet(self.containerStylesheet)
        self.scannedTodayContainer.setFrameShape(QFrame.StyledPanel)
        self.scannedTodayContainer.setFrameShadow(QFrame.Raised)
        self.scannedTodayLayout = QVBoxLayout(self.scannedTodayContainer)
        self.scannedTodayLayout.setSpacing(10)
        self.scannedTodayLayout.setContentsMargins(10, 10, 10, 10)
        # Scanned Today Label
        self.scannedTodayLabel = QLabel("Scans Today")
        self.scannedTodayLabel.setObjectName(u"scansTodayLabel")
        self.scannedTodayLabel.setStyleSheet(self.font1)
        self.scannedTodayLabel.setTextFormat(Qt.PlainText)
        self.scannedTodayLayout.addWidget(self.scannedTodayLabel, 0, Qt.AlignHCenter)
        # Scanned Today Number Label
        self.scannedTodayNumberLabel = QLabel("0")
        self.scannedTodayNumberLabel.setObjectName(u"scansTodayNumber")
        self.scannedTodayNumberLabel.setStyleSheet(self.font2)
        self.scannedTodayLayout.addWidget(self.scannedTodayNumberLabel, 0, Qt.AlignHCenter)

        self.scanInfoLayout.addWidget(self.scannedTodayContainer)
        self.leftLayout.addWidget(self.scanInfoWidget)

        # Set up Graph Widget
        self.setupGraphWidget()
        self.leftLayout.addWidget(self.graphWidget)
        self.dashboardLayout.addWidget(self.leftFrame)

        # Right Frame
        self.rightFrame = QFrame(dashboardWidget)
        self.rightFrame.setObjectName(u"rightFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy3.setHorizontalStretch(3)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.rightFrame.sizePolicy().hasHeightForWidth())
        self.rightFrame.setSizePolicy(sizePolicy3)
        self.rightFrame.setFrameShape(QFrame.StyledPanel)
        self.rightFrame.setFrameShadow(QFrame.Raised)
        self.rightLayout = QVBoxLayout(self.rightFrame)
        self.rightLayout.setSpacing(10)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)

        # Recent Scanned Frame
        self.recentScansframe = QFrame(self.rightFrame)
        self.recentScansframe.setStyleSheet(self.containerStylesheet)
        self.recentScansframeLayout = QVBoxLayout(self.recentScansframe)
        self.rightLayout.addWidget(self.recentScansframe)

        self.recentScansHeader = QFrame(self.rightFrame)
        self.recentScansHeader.setStyleSheet(self.noneStyle)
        self.recentScansHeader.setObjectName(u"recentScansHeader")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHeightForWidth(self.recentScansHeader.sizePolicy().hasHeightForWidth())
        self.recentScansHeader.setSizePolicy(sizePolicy2)
        self.recentScansHeader.setFrameShape(QFrame.StyledPanel)
        self.recentScansHeader.setFrameShadow(QFrame.Raised)
        recentScansHeaderLayout = QVBoxLayout(self.recentScansHeader)
        recentScansHeaderLayout.setSpacing(10)
        recentScansHeaderLayout.setObjectName(u"recentScansHeaderLayout")
        recentScansHeaderLayout.setContentsMargins(0, 0, 0, 0)

        # Label for the Recent Scans Section
        self.recentscansLabel = QLabel("Recent Scans")
        self.recentscansLabel.setObjectName(u"recentscansLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHeightForWidth(self.recentscansLabel.sizePolicy().hasHeightForWidth())
        self.recentscansLabel.setSizePolicy(sizePolicy4)
        self.recentscansLabel.setStyleSheet(f"font: 75 {subheaderFontSize} {font}; color:{textColor}")
        recentScansHeaderLayout.addWidget(self.recentscansLabel)
        self.recentScansframeLayout.addWidget(self.recentScansHeader)

        for i in self.last5Scanned():
            user = dbu.get_user_by_id(i[0])
            photo_path = f"../Database/IndirectUsers/photos/{user.photos}"
            name = f"{user.firstName} {user.lastName}"
            id = user.id
            date_time = i[1]
            recentScan = self.create_recent_scan_widget(photo_path, name, id, date_time)
            self.recentScansframeLayout.addWidget(recentScan)


        self.rightLayout.addStretch()
        self.dashboardLayout.addWidget(self.rightFrame)
        self.getData()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_date_label)
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(60000)  # Update every 60000 milliseconds (1 minute)

    def update_date_label(self):
        # Update the QLabel with the current date
        current_date = QDate.currentDate().toString("dddd, MMMM dd, yyyy")
        self.dateLabel.setText(current_date)

    def update_time_label(self):
        # Update the QLabel with the current time
        current_time = QTime.currentTime().toString("hh:mm AP")
        self.timeLabel.setText(current_time)

    def create_recent_scan_widget(self, user_image_path, user_name_text, user_id_text, scan_date_time_text):
        recentScansWidget = QFrame()
        recentScansWidget.setStyleSheet("background-color: transparent;"
                                   "border: none;"
                                   "border-radius: 20px;")
        recentScansWidget.setObjectName("recentScansWidget")
        recentScansWidget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        recentScansWidget.setFrameShape(QFrame.StyledPanel)
        recentScansWidget.setFrameShadow(QFrame.Raised)
        recentScansLayout = QVBoxLayout(recentScansWidget)
        recentScansLayout.setSpacing(10)
        recentScansLayout.setContentsMargins(0, 0, 0, 0)

        # Container for Recent Scan Information
        recentScans = QFrame()
        recentScans.setObjectName("recentScans")
        recentScans.setStyleSheet(self.noneStyle)
        recentScans.setFrameShape(QFrame.StyledPanel)
        recentScans.setFrameShadow(QFrame.Raised)
        recentScansLayout = QHBoxLayout(recentScans)
        recentScansLayout.setSpacing(5)
        recentScansLayout.setContentsMargins(10, 10, 10, 10)

        # Image Container within Recent Scan Information
        imgContainer = QFrame(recentScans)
        imgContainer.setObjectName("imgContainer")
        imgContainer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        imgContainer.setStyleSheet(self.noneStyle)
        imgLayout = QVBoxLayout(imgContainer)
        imgLayout.setSpacing(0)
        imgLayout.setContentsMargins(0, 0, 0, 0)
        userImg = QLabel(imgContainer)
        userImg.setObjectName("userImg")
        pixmap = QPixmap(user_image_path)
        userImg.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio))
        userImg.setScaledContents(True)
        userImg.setMaximumSize(50, 50)
        imgLayout.addWidget(userImg, 0, Qt.AlignHCenter | Qt.AlignVCenter)

        recentScansLayout.addWidget(imgContainer, stretch=1)

        # User Info Container
        userInfo = QFrame(recentScans)
        userInfo.setObjectName("userInfo")
        userInfo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        userInfo.setStyleSheet(self.noneStyle)
        userInfoLayout = QVBoxLayout(userInfo)
        userInfoLayout.setSpacing(5)
        userInfoLayout.setContentsMargins(0, 0, 0, 0)

        # User ID Label
        userID = QLabel(userInfo)
        userID.setObjectName("userID")
        userID.setStyleSheet(f"font: 75 {bodySecondaryFontSize} '{font}'; color:{textColor};")
        userID.setText(user_id_text)
        userInfoLayout.addWidget(userID)

        # User Name Label
        userName = QLabel(userInfo)
        userName.setObjectName("userName")
        userName.setStyleSheet(f"font: 75 {bodyFontSize} '{font}'; color:{textColor};")
        userName.setText(user_name_text)
        userInfoLayout.addWidget(userName)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        # Scan Date Time Label
        scanDateTime = QLabel(userInfo)
        scanDateTime.setObjectName("scanDateTime")
        scanDateTime.setStyleSheet(f"font: 75 {bodySecondaryFontSize} '{font}'; color:{secondaryFontColor};")
        scanDateTime.setGraphicsEffect(opacity_effect)
        scanDateTime.setText(scan_date_time_text)
        userInfoLayout.addWidget(scanDateTime)

        recentScansLayout.addWidget(userInfo, stretch=2)

        # Add the recent scans frame to the widget's layout
        recentScansWidget.layout().addWidget(recentScans)

        return recentScansWidget

    def setupGraphWidget(self):
        self.graphWidget = QFrame(self.leftFrame)
        self.graphWidget.setObjectName("graphWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setVerticalStretch(12)
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setStyleSheet(self.containerStylesheet)
        self.graphWidget.setFrameShape(QFrame.StyledPanel)
        self.graphWidget.setFrameShadow(QFrame.Raised)

        # Set the layout for the graphWidget
        layout = QVBoxLayout(self.graphWidget)

        # Create a Figure and a Canvas
        self.figure = Figure()
        self.figure = Figure(facecolor='none')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        # Call the method to plot the graph
        self.plotBarGraph()

    def plotBarGraph(self):
        # Simulated data for user scans
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        users_scanned = [20, 35, 30, 15, 40, 60, 45]  # Random user counts for each day

        # Convert RGB to Matplotlib color format
        def convert_rgb_to_mpl(color):
            return tuple(c / 255 for c in color)

        # Define your colors


        bg_color = convert_rgb_to_mpl(graph_background_color)
        font_color = convert_rgb_to_mpl(graph_font_color)
        bar_color = convert_rgb_to_mpl(graph_bar_color)

        ax = self.figure.add_subplot(111)

        # Set the background color for the Axes (plot area)
        ax.set_facecolor(bg_color)

        # Set the graph title, labels, and font properties
        ax.set_title('Scans per Day', fontsize=14, fontname=f'{font}', color=font_color)
        ax.set_xlabel('Days of the Week', fontsize=14, fontname=f'{font}', color=font_color)
        ax.set_ylabel('Users Scanned', fontsize=14, fontname=f'{font}', color=font_color)

        # Plot the bar chart with the specified bar color
        bars = ax.bar(days_of_week, users_scanned, color=[bar_color] * len(days_of_week))

        # Change the font of the ticks on x and y axis
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname(f'{font}')
            label.set_fontsize(14)  # Adjust the size as needed

        ax.patch.set_visible(False)

        # Redraw the canvas to reflect the changes
        self.canvas.draw()

    def getData(self):
        # Indirect User number set text
        self.userNumberLabel.setText(str(len(dbu.users)))

        now = datetime.now()
        current_day_of_week = now.strftime("%A")
        self.usersScheduledTodayNumberLabel.setText(str(len(entitiesMain.getSchedule(current_day_of_week))))

        # number of current tickets
        directory = '../Database/Tickets'
        files = os.listdir(directory)
        file_count = len([entry for entry in files if os.path.isfile(os.path.join(directory, entry))])
        self.currentNumOfTickets.setText(str(file_count))


        logsDirectory = "../Database/Logs/log.csv"
        with open(logsDirectory, mode='r') as file:
            reader = csv.DictReader(file)
            logs = list(reader)

        # get users scanned today
        users_scanned_today = \
            [log for log in logs if datetime.strptime(log['Timestamp'], '%Y-%m-%d %H:%M:%S').date() == now.date()]

        self.scannedTodayNumberLabel.setText(str(len(users_scanned_today)))

        # get users scanned this week
        start_of_week = now - timedelta(days=now.weekday())
        users_scanned_this_week = [log for log in logs if start_of_week.date() <= datetime.strptime(log['Timestamp'],
                                                                                                    '%Y-%m-%d %H:%M:%S').date() <= now.date()]

    def last5Scanned(self):
        logs_directory = "../Database/Logs/log.csv"
        with open(logs_directory, mode='r') as file:
            reader = csv.DictReader(file)
            logs = list(reader)

            # get last 5 users scanned
            last_5_users_scanned = logs[-5:] if len(logs) >= 5 else logs

            # Extract user IDs and timestamps from the last 5 scanned entries
            user_ids_and_times = [(log['UserID'], log['Timestamp']) for log in last_5_users_scanned]

            return user_ids_and_times

class Ui_logs(object):
    def setupUi(self, logs):
        if not logs.objectName():
            logs.setObjectName("logs")

        self.table_stylesheet = f"""
            QTableView {{
                border: 1px solid {bordersLines};
                gridline-color: {bordersLines};
                selection-background-color: {interactiveElements1};
                selection-color: black;
                background-color: {contentCardBackgroundColor};
                color: {textColor};
                font: 75 {dataTablesFontSize} "{font}";
            }}

            QTableView::item {{
                padding: 5px;
                border-color: transparent;
                gridline-color: #d4d4d4;
            }}

            QTableView::item:selected {{
                background: #e7e7e7;
                color: black;
            }}
            QTableView QLineEdit {{
        color: black; /* Color of the text while editing */
        }}
    

            QTableView::item:hover {{
                background-color: #f5f5f5;
            }}

            QTableView QTableCornerButton::section {{
                background: #e6e6e6;
                border: 1px solid #d4d4d4;
            }}

            QHeaderView::section {{
                font: 75 {bodyFontSize} "{font}";
                background-color: #f4f4f4;
                padding: 4px;
                border: 1px solid {bordersLines};
                font-weight: bold;
                color: {textColor};
            }}

            QHeaderView::section:checked {{
                background-color: #d0d0d0;
            }}

            QHeaderView::section:horizontal {{
                border-top: none;
            }}

            QHeaderView::section:vertical {{
                border-left: none;
            }}
        """
        self.tabStyleSheet = f"""
            QTabWidget::tab-bar {{
                alignment: left;
                background-color: {contentCardBackgroundColor};
                
            }}

            QTabWidget::pane {{
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                background: {contentCardBackgroundColor};
                color:{textColor};
            }}

            QTabBar::tab {{
                background: {buttonColor};
                font: 75 {bodyFontSize} "{font}";
                color: {textColor};
                border: 0px;
                margin: 5px;
                padding: 5px;
                min-width: 250px;
                border-top-right-radius: 10px; 
                border-bottom-right-radius: 10px;
                border-bottom-left-radius: 10px;
                border-top-left-radius: 10px;
            }}



            QTabBar::tab:selected {{
                background: {sidebarColor};
                color: {sideBarTextColor};
            }}

            QTabBar::tab:hover {{
                background: {interactiveElements1};
            }}
        """



        self.buttonStyleSheet = f"""
                    QPushButton {{
                        background-color: {buttonColor};
                        color: {textColor};
                        border-style: outset;
                        border-width: 2px;
                        border-radius: 10px;
                        border-color: {bordersLines};
                        font: bold {bodyFontSize} "{font}";
                        padding: 5px;
                    }}
                    QPushButton:pressed {{
                        background-color: {interactiveElements1};
                        border-style: inset;
                    }}
                    QPushButton:hover:!pressed {{
                        background-color: {interactiveElements2};
                    }}

                """
        self.containerStylesheet = f"""
                                    QFrame {{
                                        background-color: {contentCardBackgroundColor};
                                        border: 2px solid {bordersLines};
                                        border-radius: 20px;
                                        color: {textColor}

                                    }}
                                """
        self.noneStyle = f"""
                                    QFrame {{
                                        background-color: transparent;
                                        border: none;
                                        border-radius: 0px;
                                    }}
                                """

        self.fileMap = {}
        logs.setStyleSheet("background-color: transparent;")

        self.logLayout = QHBoxLayout(logs)
        self.logLayout.setSpacing(0)
        self.logLayout.setObjectName("logLayout")
        self.logLayout.setContentsMargins(0, 0, 0, 0)

        self.setupLeftWindow(logs)
        self.setupRightFrame(logs)
        self.logsTabWidget.setCurrentIndex(0)

    def setupLeftWindow(self, parent):
        self.leftwindow = QFrame(parent)
        self.leftwindow.setObjectName("leftwindow")
        self.configureSizePolicy(self.leftwindow, horizontal_stretch=10)

        self.leftLayout = QVBoxLayout(self.leftwindow)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setObjectName("leftLayout")
        self.leftLayout.setContentsMargins(10, 10, 10, 10)

        self.logsTabWidget = QTabWidget(self.leftwindow)
        self.logsTabWidget.setStyleSheet(self.tabStyleSheet)
        self.logsTabWidget.setObjectName("logsTabWidget")

        self.setupTab("faceRecLogs", "Face Recognition Logs", self.leftwindow)
        self.setupTab("employeesLogs", "Employee Logs", self.leftwindow)
        self.setupTab("indirectUserLogs", "Indirect User Logs", self.leftwindow)

        self.leftLayout.addWidget(self.logsTabWidget)
        self.logLayout.addWidget(self.leftwindow)

    def setupTab(self, object_name, label, parent):
        tab = QWidget()
        tab.setObjectName(object_name)


        tab_layout = QVBoxLayout(tab)
        tab_layout.setObjectName(object_name + "Layout")

        tab_table_view = QTableView(tab)
        tab_table_view.setStyleSheet(self.table_stylesheet)
        tab_table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        tab_table_view.setObjectName(object_name + "TableView")
        tab_layout.addWidget(tab_table_view)

        self.setupSearchWidget(object_name, tab, tab_layout)

        self.logsTabWidget.addTab(tab, label)

        if object_name == "faceRecLogs":
            self.fileMap[object_name + "TableView"] = '../Database/Logs/log.csv'
            self.loadCsvData(self.fileMap[object_name + "TableView"], tab_table_view)
        elif object_name == "indirectUserLogs":
            self.fileMap[object_name + "TableView"] = '../Database/IndirectUsers/jsonFile/users.json'
            self.loadJsonData(self.fileMap[object_name + "TableView"], tab_table_view)
        elif object_name == "employeesLogs":
            self.fileMap[object_name + "TableView"] = '../Database/Employees/jsonFile/employee.json'
            self.loadJsonData(self.fileMap[object_name + "TableView"], tab_table_view)

    def setupSearchWidget(self, object_name, parent, layout):
        # Search widget frame
        search_widget = QFrame(parent)
        search_widget.setObjectName(object_name + "SearchWidget")
        search_widget.setFrameShape(QFrame.StyledPanel)
        search_widget.setFrameShadow(QFrame.Raised)

        # Search layout
        search_layout = QHBoxLayout(search_widget)
        search_layout.setObjectName(object_name + "SearchLayout")

        # Label for the pixmap
        label = QLabel(search_widget)
        label.setObjectName(object_name + "Label")
        label.setFixedSize(24, 24)

        # Set the constant pixmap here
        pixmap = QPixmap('buttonIcons/search.png')
        label.setPixmap(pixmap)

        # Maintain aspect ratio and scale pixmap to fit label size
        label.setScaledContents(True)

        # Add label to the search layout
        search_layout.addWidget(label)

        # Search input field
        search_input = QLineEdit(search_widget)
        search_input.setObjectName(object_name + "SearchInput")

        search_input.setStyleSheet(search_bar_style)

        # Setup the search functionality
        search_input.textChanged.connect(lambda: self.searchTable(object_name + "TableView", search_input.text()))

        # Add search input to the search layout
        search_layout.addWidget(search_input)

        # Save button setup
        save_button = QPushButton(search_widget)
        save_button.setStyleSheet(self.buttonStyleSheet)
        save_button.setObjectName(object_name + "SaveButton")
        save_button.setIcon(QIcon('buttonIcons/save.png'))  # Assuming you have an icon for the save button
        save_button.setText("Save")  # Set text if you want text on the button too

        # Connect the button to the save method (you need to define this method)
        save_button.clicked.connect(self.saveData)

        # Add save button to the search layout
        search_layout.addWidget(save_button)

        # Add search widget to the parent layout
        layout.addWidget(search_widget)

    def setupRightFrame(self, parent):
        # Right frame setup
        self.frame = QFrame(parent)
        self.frame.setObjectName("frame")
        self.configureSizePolicy(self.frame, horizontal_stretch=1)

    @staticmethod
    def configureSizePolicy(widget, horizontal_stretch=0):
        # Configuring size policy for a widget
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(horizontal_stretch)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(size_policy)
        widget.setFrameShape(QFrame.StyledPanel)
        widget.setFrameShadow(QFrame.Raised)

    def loadCsvData(self, filepath, table_view):
        # Create an instance of QStandardItemModel
        model = QStandardItemModel()
        table_view.setModel(model)

        # Read the CSV file
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            # Use the first row of the CSV file for setting the header labels
            headers = next(reader)
            model.setHorizontalHeaderLabels(headers)

            for row in reader:
                items = [QStandardItem(field) for field in row]
                model.appendRow(items)

        # Resize columns to fit content
        table_view.resizeColumnsToContents()

    def searchTable(self, table_view_name, search_text):
        table_view = self.logsTabWidget.findChild(QTableView, table_view_name)
        model = table_view.model()

        for row in range(model.rowCount()):
            match = False
            for column in range(model.columnCount()):
                item = model.item(row, column)
                if search_text.lower() in item.text().lower():
                    match = True
                    break
            table_view.setRowHidden(row, not match)

    def loadJsonData(self, filepath, table_view):
        # Create an instance of QStandardItemModel
        model = QStandardItemModel()
        table_view.setModel(model)

        # Open and read the JSON file
        with open(filepath, 'r') as file:
            data = json.load(file)

        # Assuming all dictionaries in the list have the same keys.
        headers = list(data[0].keys())
        model.setHorizontalHeaderLabels(headers)

        for entry in data:
            row_data = []
            for header in headers:
                item = QStandardItem(str(entry.get(header, "")))
                row_data.append(item)
            model.appendRow(row_data)

        # Resize columns to fit content
        table_view.resizeColumnsToContents()

    def saveData(self):
        currentTabIndex = self.logsTabWidget.currentIndex()
        currentTabName = self.logsTabWidget.tabText(currentTabIndex).replace(" ", "")
        tableViewName = self.name_mapping(currentTabName) + "TableView"
        tableView = self.logsTabWidget.findChild(QTableView, tableViewName)

        if tableView is None:
            print(f"Error: Table view {tableViewName} not found.")
            return

        model = tableView.model()

        # Determine whether we are saving to a CSV or JSON file based on the extension
        filePath = self.fileMap.get(tableViewName)
        if not filePath:
            print(f"Error: No file path found for table view {tableViewName}.")
            return

        if filePath.endswith('.csv'):
            self.saveDataToCsv(filePath, model)
        elif filePath.endswith('.json'):
            self.saveDataToJson(filePath, model)
        else:
            print(f"Unsupported file format for {filePath}")

    def saveDataToJson(self, filepath, model):
        try:
            # Prepare the data list
            data = []
            headers = [model.headerData(i, QtCore.Qt.Horizontal) for i in range(model.columnCount())]
            for row in range(model.rowCount()):
                row_data = {}
                for column, header in enumerate(headers):
                    item = model.item(row, column)
                    # Check if the item is not None before calling item.text()
                    row_data[header] = item.text() if item is not None else ""
                data.append(row_data)

            # Open the file in write mode
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            print(f"An error occurred while saving to JSON: {e}")

    def saveDataToCsv(self, filepath, model):
        try:
            with open(filepath, 'w', newline='') as file:
                writer = csv.writer(file)
                headers = [model.headerData(i, QtCore.Qt.Horizontal) for i in range(model.columnCount())]
                writer.writerow(headers)
                for row in range(model.rowCount()):
                    row_data = []
                    for column in range(model.columnCount()):
                        item = model.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append("")  # Append an empty string if the item is None
                    writer.writerow(row_data)
        except Exception as e:
            print(f"An error occurred while saving to CSV: {e}")

    def name_mapping(self, tabName):
        mapping = {
            "FaceRecognitionLogs": "faceRecLogs",
            "EmployeeLogs": "employeesLogs",
            "IndirectUserLogs": "indirectUserLogs"
        }
        return mapping.get(tabName, "")

class Ui_scheduleWidget(object):
    def setupUi(self, scheduleWidget):
        if not scheduleWidget.objectName():
            scheduleWidget.setObjectName(u"scheduleWidget")

        self.calendar_stylesheet = f"""
                                        QCalendarWidget {{
                                background-color: {contentCardBackgroundColor};  /* Background color of the entire calendar */
                                border: 3px solid {bordersLines};  /* Border color of the entire calendar */
                                border-radius: 4px;         /* Rounded corners for the calendar */
                            }}

                            QCalendarWidget QWidget {{ 
                                color: {textColor};             /* change day numbers */
                            }}

                            QCalendarWidget QTableView {{ 
                                border: 2px solid {bordersLines};  /* Border around the table view (contains the days) */
                                gridline-color: {bordersLines};   /* Color of the grid separating the days */
                                background-color: white; /* Background color of the entire table view */
                            }}

                            QCalendarWidget QTableView QHeaderView::section {{ 
                                background-color: {contentCardBackgroundColor};  /* Background color of the headers (Mon, Tue, ...) */
                                padding: 6px;               /* Padding for the headers */
                                border: 1px solid {bordersLines};  /* Border color for the headers */
                                font-size: 12pt;            /* Font size of the headers */
                                font-weight: bold;          /* Font weight of the headers */
                                color: {textColor};                /* Text color of the headers */
                            }}

                            QCalendarWidget QToolButton {{ 
                                icon-size: 24px;            /* Size of the navigation icons (previous and next month) */
                                border: none;               /* Remove the border from tool buttons */
                                background-color: transparent;  /* Make tool buttons' background transparent */
                                color: {textColor};             /* Color of the navigation icons */
                            }}

                            QCalendarWidget QToolButton:hover {{ 
                                background-color: {interactiveElements1};  /* Background color when hovering over navigation buttons */
                            }}

                            QCalendarWidget QMenu {{ 
                                border: 1px solid {bordersLines};  /* Border around the drop-down menu (from the small arrow button) */
                            }}

                            QCalendarWidget QMenu::item {{ 
                                padding: 4px 24px 4px 24px; /* Padding around the items inside the drop-down menu */
                                background-color: {contentCardBackgroundColor}; /* Background color of the menu items */
                                color: {textColor};            /* Text color of the menu items */
                            }}

                            QCalendarWidget QMenu::item:selected {{ 
                                background-color: {contentCardBackgroundColor};  /* Background color when an item inside the menu is selected */
                                color: {interactiveElements1};                /* Text color of the selected item inside the menu */
                            }}

                            QCalendarWidget QAbstractItemView {{
                                selection-background-color: {contentCardBackgroundColor}; /* Background color of the selected date */
                                selection-color: {interactiveElements1};              /* Text color of the selected date */
                            }}

                            QCalendarWidget QLabel {{ 
                                font-size: 28pt;            /* Font size of the large month and year label */
                                color: {textColor};             /* Color of the large month and year label */
                                font-weight: bold;          /* Font weight of the large month and year label */
                            }}

                            QCalendarWidget #qt_calendar_navigationbar {{ 
                                background-color: {contentCardBackgroundColor};  /* Background color of the navigation bar (contains the month, year, and navigation buttons) */
                                border: 2px solid {bordersLines};  /* Border at the bottom of the navigation bar */
                                font: bold {bodyFontSize} "{font}";         /* Font size of the navigation bar */
                                min-height: 30;
                                color:{textColor}
                            }}
                """



        self.table_stylesheet = f"""
                    QTableView {{
                        border: 1px solid {bordersLines};
                        gridline-color: {bordersLines};
                        selection-background-color: {interactiveElements1};
                        selection-color: black;
                        background-color: {contentCardBackgroundColor};
                        color: {textColor};
                        font: 75 {dataTablesFontSize} "{font}";
                    }}

                    QTableView::item {{
                        padding: 5px;
                        border-color: transparent;
                        gridline-color: #d4d4d4;
                    }}

                    QTableView::item:selected {{
                        background: #e7e7e7;
                        color: black;
                    }}
                    QTableView QLineEdit {{
                color: black; /* Color of the text while editing */
                }}


                    QTableView::item:hover {{
                        background-color: #f5f5f5;
                    }}

                    QTableView QTableCornerButton::section {{
                        background: #e6e6e6;
                        border: 1px solid #d4d4d4;
                    }}

                    QHeaderView::section {{
                        font: 75 {bodyFontSize} "{font}";
                        background-color: #f4f4f4;
                        padding: 4px;
                        border: 1px solid {bordersLines};
                        font-weight: bold;
                        color: {textColor};
                    }}

                    QHeaderView::section:checked {{
                        background-color: #d0d0d0;
                    }}

                    QHeaderView::section:horizontal {{
                        border-top: none;
                    }}

                    QHeaderView::section:vertical {{
                        border-left: none;
                    }}
                """


        self.buttonStyleSheet = f"""
                            QPushButton {{
                                background-color: {buttonColor};
                                color: {textColor};
                                border-style: outset;
                                border-width: 2px;
                                border-radius: 10px;
                                border-color: {bordersLines};
                                font: bold {bodyFontSize} "{font}";
                                padding: 5px;
                            }}
                            QPushButton:pressed {{
                                background-color: {interactiveElements1};
                                border-style: inset;
                            }}
                            QPushButton:hover:!pressed {{
                                background-color: {interactiveElements2};
                            }}

                        """
        self.containerStylesheet = f"""
                                            QFrame {{
                                                background-color: {contentCardBackgroundColor};
                                                border: 2px solid {bordersLines};
                                                border-radius: 20px;
                                                color: {textColor}

                                            }}
                                        """
        self.noneStyle = f"""
                                            QFrame {{
                                                background-color: transparent;
                                                border: none;
                                                border-radius: 0px;
                                            }}
                                        """


        self.scheduleLayout = QHBoxLayout(scheduleWidget)
        self.scheduleLayout.setSpacing(0)
        self.scheduleLayout.setObjectName(u"scheduleLayout")
        self.scheduleLayout.setContentsMargins(0, 0, 0, 0)
        self.leftWidget = QFrame(scheduleWidget)
        self.leftWidget.setObjectName(u"leftWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftWidget.sizePolicy().hasHeightForWidth())
        self.leftWidget.setSizePolicy(sizePolicy)
        self.leftWidget.setFrameShape(QFrame.StyledPanel)
        self.leftWidget.setFrameShadow(QFrame.Raised)
        self.leftLayout = QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(10, 10, 10, 10)
        self.calendarWidget = QCalendarWidget(self.leftWidget)
        self.calendarWidget.setStyleSheet(self.calendar_stylesheet)
        self.calendarWidget.setGridVisible(True)
        format = self.calendarWidget.weekdayTextFormat(Qt.Saturday)
        format.setForeground(QBrush(QColor(f"{buttonColor}"), Qt.SolidPattern))
        self.calendarWidget.setWeekdayTextFormat(Qt.Saturday, format)
        self.calendarWidget.setWeekdayTextFormat(Qt.Sunday, format)

        # Set header format
        self.calendarWidget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # Hide navigation buttons
        self.calendarWidget.findChild(QToolButton, "qt_calendar_prevmonth").hide()
        self.calendarWidget.findChild(QToolButton, "qt_calendar_nextmonth").hide()
        self.calendarWidget.setObjectName(u"calendarWidget")

        self.leftLayout.addWidget(self.calendarWidget)


        self.scheduleLayout.addWidget(self.leftWidget)

        self.rightWidget = QFrame(scheduleWidget)
        self.rightWidget.setObjectName(u"rightWidget")
        sizePolicy.setHeightForWidth(self.rightWidget.sizePolicy().hasHeightForWidth())
        self.rightWidget.setSizePolicy(sizePolicy)
        self.rightWidget.setFrameShape(QFrame.StyledPanel)
        self.rightWidget.setFrameShadow(QFrame.Raised)
        self.rightLayout = QVBoxLayout(self.rightWidget)
        self.rightLayout.setSpacing(10)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(10, 10, 10, 10)
        self.tableView = QTableView(self.rightWidget)
        self.tableView.setStyleSheet(self.table_stylesheet)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setObjectName(u"tableView")

        self.tableView.model = QStandardItemModel()

        # Set the headers (optional)
        self.tableView.model.setHorizontalHeaderLabels(['Name', 'Start Time', 'End Time'])
        self.model = QStandardItemModel()

        # Set the headers
        self.model.setHorizontalHeaderLabels(['Name', 'Start Time', 'End Time'])

        # Populate the model with data
        self.populateModelWithData(self.model)

        # Assign the model to the tableView
        self.tableView.setModel(self.model)



        self.calendarWidget.clicked[QDate].connect(self.on_day_clicked)

        self.on_day_clicked(QDate.currentDate())

        self.rightLayout.addWidget(self.tableView)


        self.scheduleLayout.addWidget(self.rightWidget)

    def on_day_clicked(self, date):
        day_of_the_week = date.toString('dddd')
        getSchedules = Entities.entitiesMain.getSchedule(day_of_the_week)

        # Clear the existing model data
        self.tableView.model.clear()

        # Re-apply the header labels after clearing the data
        self.tableView.model.setHorizontalHeaderLabels(['Name', 'Start Time', 'End Time'])

        # Add new schedules to the model
        for schedule_str in getSchedules:


            # Split each schedule string into name and times
            if ': ' in schedule_str:
                name, times = schedule_str.split(': ', 1)
                # Look for a hyphen with optional whitespace around it
                if ' - ' in times or '-' in times:
                    # Remove any potential whitespace around the hyphen before splitting
                    times = times.replace(' - ', '-').replace('–', '-')  # Also replace en-dash if present
                    start_time, end_time = times.split('-')
                else:

                    start_time = 'N/A'
                    end_time = 'N/A'
            else:

                name = schedule_str  # Assume entire string is the name if no times are provided
                start_time = 'N/A'
                end_time = 'N/A'

            # Create QStandardItems for each piece of the schedule
            items = [
                QStandardItem(name),
                QStandardItem(start_time),
                QStandardItem(end_time)
            ]

            # Append the items as a new row to the model
            self.tableView.model.appendRow(items)

        # Set the model to the tableView and update it
        self.tableView.setModel(self.tableView.model)
        self.tableView.update()

    def populateModelWithData(self, model):
        # Assuming you have some data to add to the table, let's just add a few rows for example
        for i in range(5):  # 5 rows of data
            # Create a list of items
            items = [
                QStandardItem(f'Name {i}'),
                QStandardItem(f'Start {i}'),
                QStandardItem(f'End {i}')
            ]
            # Append the items as a new row to the model
            model.appendRow(items)

class Ui_ticketsWidget(object):
    def setupUi(self, ticketsWidget):
        self.button_stylesheet = f"""
            QPushButton {{
                background-color: {buttonColor};
                color: {textColor};
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: {bordersLines};
                font: bold {bodyFontSize} "{font}";
                padding: 5px;
            }}
            QPushButton:pressed {{
                background-color: {interactiveElements1};
                border-style: inset;
            }}
            QPushButton:hover:!pressed {{
                background-color: {interactiveElements2};
            }}

        """
        self.containerStylesheet = f"""
                            QFrame {{
                                background-color: {contentCardBackgroundColor};
                                border: 2px solid {bordersLines};
                                border-radius: 20px;
                                color: {textColor}
                                
                            }}
                        """
        self.noneStyle = f"""
                            QFrame {{
                                background-color: transparent;
                                border: none;
                                border-radius: 0px;
                            }}
                        """

        if not ticketsWidget.objectName():
            ticketsWidget.setObjectName(u"ticketsWidget")

        self.ticketsLayout = QHBoxLayout(ticketsWidget)
        self.ticketsLayout.setSpacing(10)
        self.ticketsLayout.setObjectName(u"ticketsLayout")
        self.ticketsLayout.setContentsMargins(10, 10, 10, 10)
        self.leftWidget = QFrame(ticketsWidget)
        self.leftWidget.setObjectName(u"leftWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftWidget.sizePolicy().hasHeightForWidth())
        self.leftWidget.setSizePolicy(sizePolicy)
        self.leftWidget.setStyleSheet(self.containerStylesheet)
        self.leftWidget.setFrameShape(QFrame.StyledPanel)
        self.leftWidget.setFrameShadow(QFrame.Raised)
        self.leftLayout = QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(10, 10, 10, 10)
        self.ticketNameLabel = QLabel(self.leftWidget)
        self.ticketNameLabel.setObjectName(u"ticketNameLabel")
        self.ticketNameLabel.setStyleSheet(f"font: 75 {subheaderFontSize} {font};"
                                           "background-color: transparent;"
                                           "border: none;"
                                           "border-radius: 20px;"
                                           f"color:{textColor}")
        self.leftLayout.addWidget(self.ticketNameLabel, 0, Qt.AlignHCenter)
        self.ticketTextEdit = QTextEdit(self.leftWidget)
        self.ticketTextEdit.setObjectName(u"ticketTextEdit")
        self.ticketTextEdit.setStyleSheet(f"background-color: {contentCardBackgroundColor};"
                                          "border: none;"
                                          "border-radius: 20px;"
                                          f"font: 75 {bodyFontSize} {font};"
                                          f"color:{textColor}")
        self.leftLayout.addWidget(self.ticketTextEdit)
        self.resolvedButton = QPushButton("Resolved")
        self.resolvedButton.setStyleSheet(self.button_stylesheet)
        self.resolvedButton.clicked.connect(self.deleteCurrentFile)
        self.resolvedButton.setObjectName(u"resolvedButton")
        self.leftLayout.addWidget(self.resolvedButton)
        self.ticketsLayout.addWidget(self.leftWidget)
        self.rightWidget = QFrame(ticketsWidget)
        self.rightWidget.setObjectName(u"rightWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rightWidget.sizePolicy().hasHeightForWidth())
        self.rightWidget.setSizePolicy(sizePolicy1)
        self.rightWidget.setStyleSheet(self.containerStylesheet)
        self.rightWidget.setFrameShape(QFrame.StyledPanel)
        self.rightWidget.setFrameShadow(QFrame.Raised)
        self.rightLayout = QVBoxLayout(self.rightWidget)
        self.rightLayout.setSpacing(10)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(10, 10, 10, 10)
        self.ticketLabel = QLabel("Tickets")
        self.ticketLabel.setObjectName(u"ticketLabel")
        self.ticketLabel.setStyleSheet(f"font: 75 {subheaderFontSize} {font};"
                                           "background-color: transparent;"
                                           "border: none;"
                                           "border-radius: 20px;"
                                           f"color:{textColor}")
        self.rightLayout.addWidget(self.ticketLabel)
        self.ticketFrame = QFrame(self.rightWidget)
        self.ticketFrame.setObjectName(u"ticketFrame")
        self.ticketFrame.setStyleSheet(u"background-color: transparent;"
                                       "border: none;"
                                       "border-radius: 20px;")
        self.ticketFrame.setFrameShape(QFrame.StyledPanel)
        self.ticketFrame.setFrameShadow(QFrame.Raised)
        self.ticketLayout = QVBoxLayout(self.ticketFrame)
        self.ticketLayout.setSpacing(10)
        self.ticketLayout.setObjectName(u"ticketLayout")
        self.ticketLayout.setContentsMargins(10, 10, 10, 10)
        self.rightLayout.addWidget(self.ticketFrame)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.rightLayout.addItem(self.verticalSpacer)

        self.ticketsLayout.addWidget(self.rightWidget)

        # Create buttons for each ticket file
        self.create_ticket_buttons()


    def create_ticket_button(self, text, font_family=f"{font}", font_size=16, font_weight=75):
        ticket_button = QPushButton()
        ticket_button.setObjectName(u"ticketButton")
        ticket_button.setText(text)
        ticket_button.setStyleSheet(self.button_stylesheet)
        return ticket_button
    def create_ticket_buttons(self):
        directory = "../Database/Tickets"
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                button = self.create_ticket_button(filename)
                button.clicked.connect(lambda checked, name=filename, filepath=os.path.join(directory, filename): self.display_file_content(filepath, name))
                self.ticketLayout.addWidget(button)

    def loadTextFile(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
                self.ticketTextEdit.setText(text)
        except Exception as e:
            print(f"An error occurred while trying to read the file: {e}")

    def display_file_content(self, filepath, filename):
        # Set the ticket name label to the file name (without extension)
        self.ticketNameLabel.setText(os.path.splitext(filename)[0])
        # Keep track of the current file path
        self.currentFilePath = filepath
        self.loadTextFile(filepath)

    def deleteCurrentFile(self):
        # Check if there is a file to delete
        if hasattr(self, 'currentFilePath') and os.path.exists(self.currentFilePath):
            try:
                os.remove(self.currentFilePath)
                # Clear the text edit and label because the file is deleted
                self.ticketTextEdit.clear()
                self.ticketNameLabel.clear()
                # Optionally, refresh the list of tickets
                self.refresh_ticket_list()
                print(f"File {self.currentFilePath} deleted successfully.")
            except Exception as e:
                print(f"An error occurred while trying to delete the file: {e}")
        else:
            print("No file is currently selected or file does not exist.")

    def refresh_ticket_list(self):
        # Clear the current list of tickets (buttons)
        for i in reversed(range(self.ticketLayout.count())):
            widget_to_remove = self.ticketLayout.itemAt(i).widget()
            # Remove it from the layout list
            self.ticketLayout.removeWidget(widget_to_remove)
            # Remove it from the gui
            widget_to_remove.setParent(None)

        # Create new buttons for all remaining ticket files
        self.create_ticket_buttons()

class Ui_addUserWidget(object):

    def setupUi(self, addUserWidget):
        #self.fieldLabelStyle = f"font: 75 {bodyFontSize} {font}; color:{textColor};"
        #self.subHeaderLabelStyle = f"font: 75 {subheaderFontSize} {font}; color:{textColor};"

        self.containerStylesheet = f"""
                    QFrame {{
                        background-color: {contentCardBackgroundColor};
                        border: 2px solid {bordersLines};
                        border-radius: 20px;
                    }}
                """
        self.noneStyle = f"""
                    QFrame {{
                        background-color: transparent;
                        border: none;
                        border-radius: 0px;
                    }}
                """
        self.subHeaderLabelStyle = f"""
                    QLabel {{
                    font: 75 {subheaderFontSize} "{font}";
                    color: {textColor};
                    background-color: transparent;
                    border: none;
                    border-radius: 20px;
                }}"""
        self.fieldLabelStyle = f"""
                    QLabel {{
                    color: {textColor};
                    font: 75 {bodyFontSize} "{font}";
                    background-color: transparent;
                    border: none;
                    border-radius: 20px;
                }}"""
        self.textFieldStyle = f"""
            QLineEdit {{
                border: 1px solid {bordersLines}; /* Replace with your border color */
                border-radius: 4px;
                padding: 5px;
                background-color: {fieldBackgroundColor}; /* Replace with your background color */
                color: {textColor}; /* Replace with your text color */
                font-size: {bodySecondaryFontSize}px; /* Replace with the size of your font */
                font-family: {font}; /* Replace with your font family */
            }}
            QLineEdit:focus {{
                border: 2px solid {interactiveElements1}; /* Replace with your focus border color */
                background-color: {interactiveElements2}; /* Replace with your focus background color */
            }}
            QLineEdit::placeholder {{
                color: {placeholderColor}; /* Replace with your placeholder text color */
                font-style: italic;
                opacity: 0.5;
            }}
        """
        self.comboBoxStyle = f"""QComboBox {{
        border: 1px solid {bordersLines};
        border-radius: 4px;
        padding: 5px;
        background-color: {fieldBackgroundColor};
        color: {textColor};
        font-size: {bodySecondaryFontSize}px;
        font-family: {font};
    }}
    QComboBox::drop-down {{
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;
        border-left-width: 1px;
        border-left-color: {bordersLines};
        border-left-style: solid; /* just a single line for the drop-down arrow */
        border-top-right-radius: 3px; /* same radius as the QComboBox */
        border-bottom-right-radius: 3px;
    }}
    QComboBox QAbstractItemView {{
    background-color: {contentCardBackgroundColor}; /* Set your desired color here */
    color: {textColor}; /* Optional: set text color in dropdown */
    selection-background-color: {interactiveElements1}; /* Optional: background color for selected item */
    selection-color: {interactiveElements2}; /* Optional: text color for selected item */
    min-width: 200px;  /* Adjust to desired width */
    max-width: 200px;  /* Adjust to desired width */
    border: none; /* Removes border around the dropdown */
    
}}

        QComboBox QAbstractItemView::item {{
            /* Style for the individual items in the dropdown */
            border: none;  /* Removes borders around the items */
            outline: none; /* Removes focus outline which could also appear as a line */
            background-color: {contentCardBackgroundColor}
        }}
        
        """
        self.time_edit_style = f"""
            QTimeEdit {{
                background-color: {backgroundColor}; /* Replace with your desired background color */
                color: {textColor}; /* Replace with your desired text color */
                border: 1px solid {bordersLines}; /* Replace with your desired border color */
                border-radius: 5px;
                padding: 5px;
                margin: 2px;
                font-size: {bodySecondaryFontSize}px; /* Replace with your desired font size */
                font-family: {font}; /* Replace with your desired font family */
            }}
            QTimeEdit::up-button {{
                subcontrol-origin: border;
                subcontrol-position: top right; /* Position can be changed if needed */
                border-left-width: 1px;
                border-left-color: {bordersLines}; /* Replace with your desired border color */
                border-left-style: solid; /* Can be changed if needed */
                width: {bodyFontSize}px; /* Replace with your desired button width */
            }}
            QTimeEdit::down-button {{
                subcontrol-origin: border;
                subcontrol-position: bottom right; /* Position can be changed if needed */
                border-left-width: 1px;
                border-left-color: {bordersLines}; /* Replace with your desired border color */
                border-left-style: solid; /* Can be changed if needed */
                width: {bodyFontSize}px; /* Replace with your desired button width */
            }}
            QTimeEdit::up-arrow {{
                image: url(:/icons/up-arrow.png); /* Replace with your desired icon */
                width: {bodyFontSize}px; /* Replace with your desired width */
                height: {bodyFontSize}px; /* Replace with your desired height */
            }}
            QTimeEdit::down-arrow {{
                image: url(:/icons/down-arrow.png); /* Replace with your desired icon */
                width: {bodyFontSize}px; /* Replace with your desired width */
                height: {bodyFontSize}px; /* Replace with your desired height */
            }}
            QTimeEdit::up-arrow:hover, QTimeEdit::down-arrow:hover {{
                image: url(:/icons/hover-arrow.png); /* Replace with an icon for hover state */
            }}
            QTimeEdit:focus {{
                border: 2px solid {interactiveElements1}; /* Replace with your desired focus border color */
            }}
        """
        self.checkbox_style = f"""
            QCheckBox {{
                font-family: {font};  /* Change to your preferred font family */
                font-size: {bodyFontSize};       /* Change to the desired font size */
                color: {textColor};    /* Set your preferred text color, replace {textColor} with a color variable or value */
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 1px solid {bordersLines};  /* Replace {bordersLines} with your color variable */
                background-color: {backgroundColor}; /* Replace {backgroundColor} with your color variable */
            }}
            QCheckBox::indicator:unchecked:hover {{
                border-color: #a0a0a0;
            }}
            QCheckBox::indicator:checked {{
                background-color: #5ca941;
                border: 1px solid #5ca941;
            }}
            QCheckBox::indicator:checked:hover {{
                background-color: {interactiveElements1}; /* Replace {interactiveElements1} with your color variable */
            }}
            /* Disabled states */
            QCheckBox::indicator:disabled {{
                background-color: #e6e6e6;
                border-color: #aaaaaa;
            }}
            /* Font styles for when the checkbox is disabled */
            QCheckBox:disabled {{
                color: #aaaaaa; /* Color for the text when the checkbox is disabled */
            }}
        """
        self.button_stylesheet = f"""
    QPushButton {{
        background-color: {buttonColor};
        color: {textColor};
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: {bordersLines};
        font: bold {bodyFontSize} "{font}";
        padding: 5px;
    }}
    QPushButton:pressed {{
        background-color: {interactiveElements1};
        border-style: inset;
    }}
    QPushButton:hover:!pressed {{
        background-color: {interactiveElements2};
    }}
    
"""


        addUserWidget.setStyleSheet(backgroundColorTransparent)
        self.addUserLayout = QVBoxLayout(addUserWidget)
        self.addUserLayout.setSpacing(10)
        self.addUserLayout.setContentsMargins(0, 0, 0, 0)


        self.accountOrganizationFrame = QFrame(addUserWidget)
        self.accountOrganizationFrame.setStyleSheet(self.containerStylesheet)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.accountOrganizationFrame.sizePolicy().hasHeightForWidth())
        self.accountOrganizationFrame.setSizePolicy(sizePolicy)
        self.accountOrganizationLayout = QHBoxLayout(self.accountOrganizationFrame)
        self.accountOrganizationLayout.setAlignment(Qt.AlignLeft)
        self.accountOrganizationLayout.setSpacing(5)
        self.accountOrganizationLayout.setContentsMargins(5, 5, 5, 5)


        self.accountFrame = QFrame(self.accountOrganizationFrame)
        self.accountFrame.setStyleSheet(self.noneStyle)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.accountFrame.sizePolicy().hasHeightForWidth())
        self.accountFrame.setSizePolicy(sizePolicy1)
        self.accountLayout = QVBoxLayout(self.accountFrame)
        self.accountLayout.setAlignment(Qt.AlignLeft)
        self.accountLayout.setSpacing(0)
        self.accountLayout.setContentsMargins(0, 0, 0, 0)
        self.accountLabel = QLabel("Account")
        self.accountLabel.setStyleSheet(self.subHeaderLabelStyle)
        self.accountLayout.addWidget(self.accountLabel)



        self.accountForm = QFrame(self.accountFrame)
        self.accountForm.setStyleSheet(self.fieldLabelStyle + self.textFieldStyle + self.comboBoxStyle)
        self.accountFormLayout = QFormLayout(self.accountForm)
        self.accountFormLayout.setHorizontalSpacing(5)
        self.accountFormLayout.setVerticalSpacing(5)
        self.accountFormLayout.setContentsMargins(0, 0, 0, 0)
        self.userIDLabel = QLabel("User ID: ")
        self.accountFormLayout.setWidget(0, QFormLayout.LabelRole, self.userIDLabel)
        self.userIDLineEdit = QLineEdit(self.accountForm)


        self.accountFormLayout.setWidget(0, QFormLayout.FieldRole, self.userIDLineEdit)
        self.firstNameLabel = QLabel("First Name: ")
        self.accountFormLayout.setWidget(1, QFormLayout.LabelRole, self.firstNameLabel)
        self.firstNameLineEdit = QLineEdit(self.accountForm)
        self.accountFormLayout.setWidget(1, QFormLayout.FieldRole, self.firstNameLineEdit)
        self.lastNameLabel = QLabel("Last Name: ")
        self.accountFormLayout.setWidget(2, QFormLayout.LabelRole, self.lastNameLabel)
        self.lastNameLineEdit = QLineEdit(self.accountForm)
        self.accountFormLayout.setWidget(2, QFormLayout.FieldRole, self.lastNameLineEdit)
        self.genderLabel = QLabel("Gender: ")
        self.accountFormLayout.setWidget(3, QFormLayout.LabelRole, self.genderLabel)
        self.genderComboBox = QComboBox(self.accountForm)
        self.genderComboBox.addItem("Male")
        self.genderComboBox.addItem("Female")
        self.accountFormLayout.setWidget(3, QFormLayout.FieldRole, self.genderComboBox)
        self.accountVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.accountFormLayout.setItem(4, QFormLayout.LabelRole, self.accountVerticalSpacer)
        self.accountLayout.addWidget(self.accountForm)
        self.accountOrganizationLayout.addWidget(self.accountFrame)


        self.organizationFrame = QFrame(self.accountOrganizationFrame)
        self.organizationFrame.setStyleSheet(self.noneStyle)
        sizePolicy1.setHeightForWidth(self.organizationFrame.sizePolicy().hasHeightForWidth())
        self.organizationFrame.setSizePolicy(sizePolicy1)
        self.organizationLayout = QVBoxLayout(self.organizationFrame)
        self.organizationLayout.setSpacing(0)
        self.organizationLayout.setContentsMargins(0, 0, 0, 0)
        self.organizationLabel = QLabel("Organization")
        self.organizationLabel.setStyleSheet(self.subHeaderLabelStyle)
        self.organizationLayout.addWidget(self.organizationLabel)


        self.organizationForm = QFrame(self.organizationFrame)
        self.organizationForm.setStyleSheet(self.textFieldStyle + self.fieldLabelStyle)
        self.organizationFormLayout = QFormLayout(self.organizationForm)
        self.organizationFormLayout.setHorizontalSpacing(10)
        self.organizationFormLayout.setVerticalSpacing(10)
        self.organizationFormLayout.setContentsMargins(0, 0, 0, 0)
        self.companyNameLabel = QLabel("Company: ")
        self.organizationFormLayout.setWidget(0, QFormLayout.LabelRole, self.companyNameLabel)
        self.companyNameLineEdit = QLineEdit(self.organizationForm)
        self.organizationFormLayout.setWidget(0, QFormLayout.FieldRole, self.companyNameLineEdit)
        self.titleLabel = QLabel("Title: ")
        self.organizationFormLayout.setWidget(1, QFormLayout.LabelRole, self.titleLabel)
        self.titleLineEdit = QLineEdit(self.organizationForm)
        self.organizationFormLayout.setWidget(1, QFormLayout.FieldRole, self.titleLineEdit)
        self.organizationVerticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.organizationFormLayout.setItem(2, QFormLayout.LabelRole, self.organizationVerticalSpacer)
        self.organizationLayout.addWidget(self.organizationForm)
        self.accountOrganizationLayout.addWidget(self.organizationFrame)
        self.addUserLayout.addWidget(self.accountOrganizationFrame)




        self.scheduleFrame = QFrame(addUserWidget)
        self.scheduleFrame.setStyleSheet(self.containerStylesheet)
        sizePolicy.setHeightForWidth(self.scheduleFrame.sizePolicy().hasHeightForWidth())
        self.scheduleFrame.setSizePolicy(sizePolicy)
        self.scheduleLayout = QVBoxLayout(self.scheduleFrame)
        self.scheduleLayout.setSpacing(5)
        self.scheduleLayout.setContentsMargins(5, 5, 5, 5)
        self.scheduleLabel = QLabel("Schedule")
        self.scheduleLabel.setStyleSheet(self.subHeaderLabelStyle + self.noneStyle)
        self.scheduleLayout.addWidget(self.scheduleLabel)


        self.scheduleForm = QFrame(self.scheduleFrame)
        self.scheduleForm.setStyleSheet(self.noneStyle + self.fieldLabelStyle + self.time_edit_style + self.checkbox_style )
        self.scheduleFormLayout = QGridLayout(self.scheduleForm)
        self.scheduleFormLayout.setSpacing(5)
        self.scheduleFormLayout.setContentsMargins(0, 0, 0, 0)
        self.timeEditStartMonday = QTimeEdit(self.scheduleForm)
        self.timeEditStartMonday.setReadOnly(False)



        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.timeEditStartMonday.sizePolicy().hasHeightForWidth())
        self.timeEditStartMonday.setSizePolicy(sizePolicy2)
        self.timeEditStartMonday.setCurrentSection(QDateTimeEdit.HourSection)
        self.timeEditStartMonday.setCalendarPopup(False)
        self.timeEditStartMonday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartMonday, 2, 1, 1, 1)
        self.timeEditStartThursday = QTimeEdit(self.scheduleForm)
        self.timeEditStartThursday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditStartThursday.sizePolicy().hasHeightForWidth())
        self.timeEditStartThursday.setSizePolicy(sizePolicy2)
        self.timeEditStartThursday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartThursday, 5, 1, 1, 1)
        self.timeEditEndThursday = QTimeEdit(self.scheduleForm)
        self.timeEditEndThursday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditEndThursday.sizePolicy().hasHeightForWidth())
        self.timeEditEndThursday.setSizePolicy(sizePolicy2)
        self.timeEditEndThursday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndThursday, 5, 3, 1, 1)
        self.timeEditStartWednesday = QTimeEdit(self.scheduleForm)
        self.timeEditStartWednesday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditStartWednesday.sizePolicy().hasHeightForWidth())
        self.timeEditStartWednesday.setSizePolicy(sizePolicy2)
        self.timeEditStartWednesday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartWednesday, 4, 1, 1, 1)
        self.timeEditEndSaturday = QTimeEdit(self.scheduleForm)
        self.timeEditEndSaturday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditEndSaturday.sizePolicy().hasHeightForWidth())
        self.timeEditEndSaturday.setSizePolicy(sizePolicy2)
        self.timeEditEndSaturday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndSaturday, 7, 3, 1, 1)
        self.dayLabel = QLabel("Day")
        self.dayLabel.setStyleSheet(self.fieldLabelStyle)
        sizePolicy1.setHeightForWidth(self.dayLabel.sizePolicy().hasHeightForWidth())
        self.dayLabel.setSizePolicy(sizePolicy1)
        self.scheduleFormLayout.addWidget(self.dayLabel, 0, 0, 1, 1)
        self.checkBoxSunday = QCheckBox("Sunday: ")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(1)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.checkBoxSunday.sizePolicy().hasHeightForWidth())
        self.checkBoxSunday.setSizePolicy(sizePolicy3)
        self.scheduleFormLayout.addWidget(self.checkBoxSunday, 1, 0, 1, 1)
        self.checkBoxFriday = QCheckBox("Friday: ")
        sizePolicy3.setHeightForWidth(self.checkBoxFriday.sizePolicy().hasHeightForWidth())
        self.checkBoxFriday.setSizePolicy(sizePolicy3)
        self.scheduleFormLayout.addWidget(self.checkBoxFriday, 6, 0, 1, 1)
        self.timeEditEndWednesday = QTimeEdit(self.scheduleForm)
        self.timeEditEndWednesday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditEndWednesday.sizePolicy().hasHeightForWidth())
        self.timeEditEndWednesday.setSizePolicy(sizePolicy2)
        self.timeEditEndWednesday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndWednesday, 4, 3, 1, 1)
        self.timeEditEndSunday = QTimeEdit(self.scheduleForm)
        self.timeEditEndSunday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditEndSunday.sizePolicy().hasHeightForWidth())
        self.timeEditEndSunday.setSizePolicy(sizePolicy2)
        self.timeEditEndSunday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndSunday, 1, 3, 1, 1)
        self.timeEditStartSunday = QTimeEdit(self.scheduleForm)
        self.timeEditStartSunday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditStartSunday.sizePolicy().hasHeightForWidth())
        self.timeEditStartSunday.setSizePolicy(sizePolicy2)
        self.timeEditStartSunday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartSunday, 1, 1, 1, 1)
        self.checkBoxWednesday = QCheckBox("Wednesday: ")
        sizePolicy3.setHeightForWidth(self.checkBoxWednesday.sizePolicy().hasHeightForWidth())
        self.checkBoxWednesday.setSizePolicy(sizePolicy3)
        self.scheduleFormLayout.addWidget(self.checkBoxWednesday, 4, 0, 1, 1)
        self.timeEditEndTuesday = QTimeEdit(self.scheduleForm)
        self.timeEditEndTuesday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditEndTuesday.sizePolicy().hasHeightForWidth())
        self.timeEditEndTuesday.setSizePolicy(sizePolicy2)
        self.timeEditEndTuesday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndTuesday, 3, 3, 1, 1)
        self.checkBoxThursday = QCheckBox("Thursday: ")
        sizePolicy3.setHeightForWidth(self.checkBoxThursday.sizePolicy().hasHeightForWidth())
        self.checkBoxThursday.setSizePolicy(sizePolicy3)
        self.scheduleFormLayout.addWidget(self.checkBoxThursday, 5, 0, 1, 1)
        self.checkBoxSaturday = QCheckBox("Saturday: ")
        sizePolicy3.setHeightForWidth(self.checkBoxSaturday.sizePolicy().hasHeightForWidth())
        self.checkBoxSaturday.setSizePolicy(sizePolicy3)
        self.scheduleFormLayout.addWidget(self.checkBoxSaturday, 7, 0, 1, 1)
        self.timeEditEndMonday = QTimeEdit(self.scheduleForm)
        self.timeEditEndMonday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditEndMonday.sizePolicy().hasHeightForWidth())
        self.timeEditEndMonday.setSizePolicy(sizePolicy2)
        self.timeEditEndMonday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndMonday, 2, 3, 1, 1)
        self.checkBoxTuesday = QCheckBox("Thursday: ")
        sizePolicy3.setHeightForWidth(self.checkBoxTuesday.sizePolicy().hasHeightForWidth())
        self.checkBoxTuesday.setSizePolicy(sizePolicy3)
        self.scheduleFormLayout.addWidget(self.checkBoxTuesday, 3, 0, 1, 1)
        self.endTimeLabel = QLabel("End Time")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(4)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.endTimeLabel.sizePolicy().hasHeightForWidth())
        self.endTimeLabel.setSizePolicy(sizePolicy4)
        self.scheduleFormLayout.addWidget(self.endTimeLabel, 0, 3, 1, 1)
        self.timeEditStartTuesday = QTimeEdit(self.scheduleForm)
        self.timeEditStartTuesday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditStartTuesday.sizePolicy().hasHeightForWidth())
        self.timeEditStartTuesday.setSizePolicy(sizePolicy2)
        self.timeEditStartTuesday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartTuesday, 3, 1, 1, 1)
        self.startTimeLabel = QLabel("Start Time")
        sizePolicy4.setHeightForWidth(self.startTimeLabel.sizePolicy().hasHeightForWidth())
        self.startTimeLabel.setSizePolicy(sizePolicy4)
        self.scheduleFormLayout.addWidget(self.startTimeLabel, 0, 1, 1, 1)
        self.checkBoxMonday = QCheckBox("Monday: ")
        sizePolicy3.setHeightForWidth(self.checkBoxMonday.sizePolicy().hasHeightForWidth())
        self.checkBoxMonday.setSizePolicy(sizePolicy3)
        self.scheduleFormLayout.addWidget(self.checkBoxMonday, 2, 0, 1, 1)
        self.timeEditEndFriday = QTimeEdit(self.scheduleForm)
        self.timeEditEndFriday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditEndFriday.sizePolicy().hasHeightForWidth())
        self.timeEditEndFriday.setSizePolicy(sizePolicy2)
        self.timeEditEndFriday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndFriday, 6, 3, 1, 1)
        self.timeEditStartFriday = QTimeEdit(self.scheduleForm)
        sizePolicy2.setHeightForWidth(self.timeEditStartFriday.sizePolicy().hasHeightForWidth())
        self.timeEditStartFriday.setSizePolicy(sizePolicy2)
        self.timeEditStartFriday.setReadOnly(False)
        self.timeEditStartFriday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartFriday, 6, 1, 1, 1)
        self.timeEditStartSaturday = QTimeEdit(self.scheduleForm)
        self.timeEditStartSaturday.setReadOnly(False)
        sizePolicy2.setHeightForWidth(self.timeEditStartSaturday.sizePolicy().hasHeightForWidth())
        self.timeEditStartSaturday.setSizePolicy(sizePolicy2)
        self.timeEditStartSaturday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartSaturday, 7, 1, 1, 1)
        self.scheduleLayout.addWidget(self.scheduleForm)
        self.addUserLayout.addWidget(self.scheduleFrame)



        self.faceEncFrame = QFrame(addUserWidget)
        self.faceEncFrame.setStyleSheet(self.noneStyle)
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.faceEncFrame.sizePolicy().hasHeightForWidth())
        self.faceEncFrame.setSizePolicy(sizePolicy5)
        self.faceEncLayout = QHBoxLayout(self.faceEncFrame)
        self.faceEncLayout.setSpacing(5)
        self.faceEncLayout.setContentsMargins(5, 5, 5, 5)


        self.pictureframe = QFrame(self.faceEncFrame)
        self.pictureframe.setStyleSheet(self.noneStyle)
        sizePolicy1.setHeightForWidth(self.pictureframe.sizePolicy().hasHeightForWidth())
        self.pictureframe.setSizePolicy(sizePolicy1)
        self.pictureLayout = QHBoxLayout(self.pictureframe)
        self.picture = QLabel(self.pictureframe)
        self.picture.setScaledContents(True)
        self.picture.setMaximumSize(40, 40)
        pixmap = QPixmap("buttonIcons/user.png")
        self.picture.setPixmap(pixmap)
        self.pictureLayout.addWidget(self.picture, 0, Qt.AlignHCenter)
        self.faceEncLayout.addWidget(self.pictureframe, 0, Qt.AlignVCenter)


        self.photoFaceEncFrame = QFrame(self.faceEncFrame)
        self.photoFaceEncFrame.setStyleSheet(self.noneStyle)
        sizePolicy4.setHeightForWidth(self.photoFaceEncFrame.sizePolicy().hasHeightForWidth())
        self.photoFaceEncFrame.setSizePolicy(sizePolicy4)
        self.photoFaceEncLayout = QVBoxLayout(self.photoFaceEncFrame)
        self.photoFaceEncLayout.setContentsMargins(0, 0, 0, 0)
        self.faceEncFrameLabel = QLabel("Face Encoding: ")
        self.faceEncFrameLabel.setStyleSheet(self.noneStyle + self.subHeaderLabelStyle)
        self.photoFaceEncLayout.addWidget(self.faceEncFrameLabel)


        self.photoFaceEncForm = QFrame(self.photoFaceEncFrame)
        self.photoFaceEncForm.setStyleSheet(self.noneStyle + self.fieldLabelStyle + self.textFieldStyle)
        self.photoFaceEncFormLayout = QFormLayout(self.photoFaceEncForm)
        self.photoFaceEncFormLayout.setAlignment(Qt.AlignLeft)
        self.photoFaceEncFormLayout.setHorizontalSpacing(5)
        self.photoFaceEncFormLayout.setVerticalSpacing(5)
        self.photoFaceEncFormLayout.setContentsMargins(0, 0, 0, 0)
        self.photoLabel = QLabel("Photo: ")
        self.photoFaceEncFormLayout.setWidget(0, QFormLayout.LabelRole, self.photoLabel)
        self.photoLineEdit = QLineEdit(self.photoFaceEncForm)
        self.photoFaceEncFormLayout.setWidget(0, QFormLayout.FieldRole, self.photoLineEdit)
        self.faceEncLabel = QLabel("Face Encoding: ")
        self.photoFaceEncFormLayout.setWidget(1, QFormLayout.LabelRole, self.faceEncLabel)
        self.faceEncLineEdit = QLineEdit(self.photoFaceEncForm)
        self.photoFaceEncFormLayout.setWidget(1, QFormLayout.FieldRole, self.faceEncLineEdit)
        self.photoFaceEncLayout.addWidget(self.photoFaceEncForm)


        self.buttonFrame = QFrame(self.photoFaceEncFrame)
        self.buttonFrame.setStyleSheet(self.noneStyle + self.button_stylesheet)
        self.buttonLayout = QHBoxLayout(self.buttonFrame)
        self.openCameraButton = self.createButton("Open Camera", self.openCameraButtonHandle)
        #self.openCameraButton.hide()
        self.takePhotoButton = self.createButton("Take Photo", self.takePhotoButtonHandle)
        self.takePhotoButton.hide()
        self.acceptButton = self.createButton("Accept", self.buttonAcceptHandle)
        self.acceptButton.hide()
        self.cancelButton = self.createButton("Cancel", self.cancelButtonHandle)


        self.photoFaceEncLayout.addWidget(self.buttonFrame)
        self.faceEncLayout.addWidget(self.photoFaceEncFrame)
        self.addUserLayout.addWidget(self.faceEncFrame)


    def clear(self):
        if hasattr(self, 'image_label'):
            self.image_label.hide()
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()

        self.accountFrame.show()
        self.organizationFrame.show()
        self.scheduleFrame.show()

        self.takePhotoButton.hide()
        self.acceptButton.hide()
        self.openCameraButton.show()

        self.userIDLineEdit.clear()
        self.firstNameLineEdit.clear()
        self.lastNameLineEdit.clear()
        # self.genderComboBox.clear()
        self.companyNameLineEdit.clear()
        self.titleLineEdit.clear()
        self.photoLineEdit.clear()
        self.faceEncLineEdit.clear()

        defaultStartTime = QTime(8, 0)
        defaultEndTime = QTime(17, 0)

        # Loop for setting the default start time
        for timeEdit in [self.timeEditStartMonday, self.timeEditStartTuesday,
                         self.timeEditStartWednesday, self.timeEditStartThursday,
                         self.timeEditStartFriday, self.timeEditStartSaturday,
                         self.timeEditStartSunday]:
            timeEdit.setTime(defaultStartTime)

        # Loop for setting the default end time
        for timeEdit in [self.timeEditEndMonday, self.timeEditEndTuesday,
                         self.timeEditEndWednesday, self.timeEditEndThursday,
                         self.timeEditEndFriday, self.timeEditEndSaturday,
                         self.timeEditEndSunday]:
            timeEdit.setTime(defaultEndTime)

        # Uncheck all CheckBoxes
        for checkBox in [self.checkBoxSunday, self.checkBoxMonday,
                         self.checkBoxTuesday, self.checkBoxWednesday,
                        self.checkBoxThursday, self.checkBoxFriday,
                        self.checkBoxSaturday
                         ]:
            checkBox.setChecked(False)


        def removeFiles():
            folder_path = '../Database/AddLocal'
            if os.path.exists(folder_path):
                for file in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, file)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
        removeFiles()

    def createButton(self, name, connect):
        button = QPushButton(name)
        button.clicked.connect(connect)
        self.buttonLayout.addWidget(button)
        return button

    def buttonAcceptHandle(self):
        self.saveNewUser()
        self.update_schedule_json()
        self.clear()

    def openCameraButtonHandle(self):
        self.accountFrame.hide()
        self.organizationFrame.hide()
        self.scheduleFrame.hide()
        if not hasattr(self, 'capture'):  # Check if the camera has been initialized already
            self.init_Cam()

        self.openCameraButton.hide()
        self.takePhotoButton.show()

    def takePhotoButtonHandle(self):
        try:
            self.capturePhoto()
            self.capture.release()

            self.image_label.hide()
            self.accountFrame.show()
            self.organizationFrame.show()
            self.scheduleFrame.show()

            self.takePhotoButton.hide()
            self.acceptButton.show()
            self.savePKL()
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()

    def init_Cam(self):
        self.image_label = QLabel()
        self.accountOrganizationLayout.addWidget(self.image_label)
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            # Convert the image from BGR to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Convert the image to Qt format
            qt_image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pix)

    def capturePhoto(self):
        ret, frame = self.capture.read()
        if ret:
            save_directory = "../Database/AddLocal"
            os.makedirs(save_directory, exist_ok=True)
            photoDir = f"{self.userIDLineEdit.text()}_0.jpg"
            file_path = os.path.join(save_directory, photoDir)
            cv2.imwrite(file_path, frame)
            self.photoLineEdit.setText(photoDir)

    def savePKL(self):
        file_path = f"../Database/AddLocal/{self.userIDLineEdit.text()}_0.jpg"
        # Save plk
        face_detector = dlib.get_frontal_face_detector()
        shape_predictor = dlib.shape_predictor("../Database/datFiles/shape_predictor_68_face_landmarks.dat")
        face_recognizer = dlib.face_recognition_model_v1(
            "../Database/datFiles/dlib_face_recognition_resnet_model_v1.dat")
        # Load the image
        image = dlib.load_rgb_image(file_path)
        faces = face_detector(image)  # Detect faces in the image

        known_face_data = {
            "name": f"{self.userIDLineEdit.text()}_0",
            "face_descriptors": [],
            "image_path": file_path,
        }

        for face in faces:
            shape = shape_predictor(image, face)
            face_descriptor = face_recognizer.compute_face_descriptor(image, shape)
            known_face_data["face_descriptors"].append(face_descriptor)
        # Save the known_face_data to a pickle file
        pickle_file_path = f"../Database/AddLocal/{self.userIDLineEdit.text()}_0.pkl"
        with open(pickle_file_path, "wb") as f:
            pickle.dump(known_face_data, f)
        self.faceEncLineEdit.setText(f"{self.userIDLineEdit.text()}_0.pkl")

    def cancelButtonHandle(self):
        self.clear()

    def saveNewUser(self):
        newUser = User(
            id=self.userIDLineEdit.text(),
            firstName=self.firstNameLineEdit.text(),
            lastName=self.lastNameLineEdit.text(),
            gender=self.genderComboBox.currentText(),
            company=self.companyNameLineEdit.text(),
            title=self.titleLineEdit.text(),
            photos=self.photoLineEdit.text(),
            faceEncoding=self.faceEncLineEdit.text()
        )

        dbu.add_user(newUser)

        shutil.move(f"../Database/AddLocal/{self.photoLineEdit.text()}",
                    f"../Database/IndirectUsers/photos/{self.photoLineEdit.text()}")

        shutil.move(f"../Database/AddLocal/{self.faceEncLineEdit.text()}",
                    f"../Database/IndirectUsers/face_encodings/{self.faceEncLineEdit.text()}")

        # db_conn = database.db
        # coll_ref = db_conn.collection("indirectUser")
        # coll_ref.add({
        #     "id": self.userIDLineEdit.text(),
        #     "firstName": self.firstNameLineEdit.text(),
        #     "lastName": self.lastNameLineEdit.text(),
        #     "gender": self.genderComboBox.currentText(),
        #     "company": self.companyNameLineEdit.text(),
        #     "title": self.titleLineEdit.text()
        # })
        # print("data added successfully")

    def get_schedule_info(self):
        user_id = self.userIDLineEdit.text()
        schedule_info = {
            "user_id": user_id,
            "schedule": {}
        }
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for day in days:
            checkbox = getattr(self, f"checkBox{day}", None)
            if checkbox and checkbox.isChecked():
                start_time_edit = getattr(self, f"timeEditStart{day}")
                end_time_edit = getattr(self, f"timeEditEnd{day}")
                start_time = start_time_edit.time().toString('hh:mm a')  # Using 12-hour format with AM/PM
                end_time = end_time_edit.time().toString('hh:mm a')  # Using 12-hour format with AM/PM
                schedule_info["schedule"][day] = f"{start_time} - {end_time}"
        return schedule_info

    def update_schedule_json(self):
        # Get the current schedule information
        new_schedule = self.get_schedule_info()

        # Define the path to the JSON file
        json_path = '../Database/IndirectUsers/jsonFile/schedule.json'

        # Read the existing data
        try:
            with open(json_path, 'r') as file:
                schedule_data = json.load(file)
                # Ensure that we have a list of dicts
                if not isinstance(schedule_data, list):
                    raise ValueError("JSON file must contain a list of dictionaries.")
        except (FileNotFoundError, ValueError) as e:
            print(f"Error reading schedule file: {e}")
            schedule_data = []

        # Check if the user_id already exists
        existing_user = next((item for item in schedule_data if item.get("user_id") == new_schedule["user_id"]), None)
        if existing_user:
            # Update existing user's schedule
            existing_user["schedule"] = new_schedule["schedule"]
        else:
            # Append the new schedule information
            schedule_data.append(new_schedule)

        # Write the updated data back to the file
        with open(json_path, 'w') as file:
            json.dump(schedule_data, file, indent=4)


class MainWindow(QMainWindow, Ui_centralWindow):
    def __init__(self, emp=None, parent=None):
        super(MainWindow, self).__init__(parent)
        self.employee = emp

        if self.employee:
            print(f"Employee logged in: {self.employee.firstName} {self.employee.lastName}")
            print("dashboard Window")
            # Adjust all other employee attribute accesses similarly
        self.setupUi(self, self.employee)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
