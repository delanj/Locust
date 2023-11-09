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
    QFormLayout, QCheckBox, QTimeEdit, QComboBox, QDateTimeEdit, QGridLayout
from PyQt5.QtCore import QCoreApplication, QMetaObject
from PyQt5.QtWidgets import QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem, QImage
from holoviews.examples.reference.apps.bokeh.player import layout
from matplotlib.figure import Figure
from matplotlib_inline.backend_inline import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


from Database.firebaseDatabase import database
import Entities.entitiesMain

from Entities import entitiesMain


# Link to data base
dbu = Entities.IndirectUser.User.UserDatabase("../Database/IndirectUsers/jsonFile/users.json")
# Users
User = Entities.IndirectUser.User.User
# Link to data base
dbe = Entities.Employee.Employee.EmployeeDatabase("../Database/Employees/jsonFile/employee.json")
# Employees
Employee = Entities.Employee.Employee.Employee

userColumnLength = len(dbu.users)
userRowLength = inspect.getsource(User.__init__).count("self.")

employeeColumnLength = len(dbe.employees)
employeeRowLength = inspect.getsource(Employee.__init__).count("self.")

font = "Copperplate"
headerFontSize = "42pt"
menuItemFontSize = "22pt"
menuItemFontSizeSecondary = "14pt"


"""Smallest Text — 12px
Detail Text — 14px
Body Text — 16/18px
Subtitle — 18px
Title Text — 24/28px
Main Text — 32/38/42px
Display Text — 60/72/80px"""

textColor = "black"



class Ui_centralWindow(object):
    def setupUi(self, centralWindow):
        if not centralWindow.objectName():
            centralWindow.setObjectName("centralWindow")

        centralWindow.setWindowTitle(QCoreApplication.translate("centralWindow", "MainWindow", None))
        centralWindow.showFullScreen()

        self.centralwidget = QWidget(centralWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.centralLayout = QHBoxLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)

        self.sideBar = QFrame(self.centralwidget)
        self.sideBar.setObjectName("sideBar")
        self.sideBar.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.sideBar.setStyleSheet("background-color: rgb(129, 117, 102);")
        self.sideBar.setFrameShape(QFrame.StyledPanel)
        self.sideBar.setFrameShadow(QFrame.Raised)

        self.sidebarLayout = QVBoxLayout(self.sideBar)
        self.sidebarLayout.setSpacing(0)
        self.sidebarLayout.setContentsMargins(0, 0, 0, 0)

        self.logoWidgetContainer = QWidget(self.sideBar)
        self.logoWidgetContainer.setObjectName("logoWidgetContainer")
        self.logoWidgetUi = Ui_logoWidget()
        self.logoWidgetUi.setupUi(self.logoWidgetContainer)
        self.sidebarLayout.addWidget(self.logoWidgetContainer, stretch=2)

        self.navigationWidgetContainer = QWidget(self.sideBar)
        self.navigationWidgetContainer.setObjectName("logoWidgetContainer")
        self.navigationWidgetUi = Ui_navigationWidget()
        self.navigationWidgetUi.setupUi(self.navigationWidgetContainer)
        self.sidebarLayout.addWidget(self.navigationWidgetContainer, stretch=10)


        self.navigationWidgetUi.logsButton.clicked.connect(self.showLogsWidget)
        self.navigationWidgetUi.dashboardButton.clicked.connect(self.showDashBoardWidget)
        self.navigationWidgetUi.scheduleButton.clicked.connect(self.showScheduleWidget)
        self.navigationWidgetUi.ticketsButton.clicked.connect(self.showTicketWidget)
        self.navigationWidgetUi.addUserButton.clicked.connect(self.showAddUserWidget)





        self.mainWindow = QFrame(self.centralwidget)
        self.mainWindow.setObjectName("mainWindow")
        self.mainWindow.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.mainWindow.setStyleSheet("background-color: rgb(250, 245, 232);")
        self.mainWindow.setFrameShape(QFrame.StyledPanel)
        self.mainWindow.setFrameShadow(QFrame.Raised)



        self.userHeaderContainer = QWidget(self.mainWindow)
        self.userHeaderContainer.setObjectName("userHeaderContainer")
        self.userHeaderUi = Ui_userHeaderWidget()
        self.userHeaderUi.setupUi(self.userHeaderContainer)


        self.displayContainer = QWidget(self.mainWindow)
        self.displayContainer.setObjectName("displayContainer")
        self.displayContainer.setStyleSheet("background-color: transparent;")
        self.displayLayout = QVBoxLayout(self.displayContainer)


        self.dashboardWidgetContainer = QWidget(self.displayContainer)
        self.dashboardWidgetContainer.setObjectName("dashboardWidgetContainer")
        self.dashboardUi = Ui_dashboardWidget()  # Instantiate your Dashboard UI class
        self.dashboardUi.setupUi(self.dashboardWidgetContainer)  # Set up the dashboard UI
        self.displayLayout.addWidget(self.dashboardWidgetContainer)





        self.mainLayout = QVBoxLayout(self.mainWindow)
        self.mainLayout.addWidget(self.userHeaderContainer, stretch=1)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.displayContainer, stretch=10)





        self.centralLayout.addWidget(self.sideBar, stretch=2)
        self.centralLayout.addWidget(self.mainWindow, stretch=10)
        centralWindow.setCentralWidget(self.centralwidget)






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

class Ui_logoWidget(object):
    def setupUi(self, logoWidget):
        if not logoWidget.objectName():
            logoWidget.setObjectName("logoWidget")

        logoWidget.setStyleSheet("background-color: transparent;")

        self.logoLayout = QHBoxLayout(logoWidget)
        self.logoLayout.setSpacing(0)
        self.logoLayout.setObjectName("logoLayout")
        self.logoLayout.setContentsMargins(0, 0, 0, 0)

        self.logoImg = QLabel(logoWidget)
        self.logoImg.setObjectName("logoImg")
        self.logoImg.setScaledContents(True)
        self.logoImg.setMaximumSize(80, 80)


        pixmap = QPixmap("../GUI/Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")
        self.logoImg.setPixmap(pixmap)

        self.logoLayout.addWidget(self.logoImg)

        self.logoLabel = QLabel(logoWidget)
        self.logoLabel.setObjectName("logoLabel")
        self.logoLabel.setStyleSheet(f"font: 75 {headerFontSize} '{font}';")

        self.logoLayout.addWidget(self.logoLabel)

        self.retranslateUi(logoWidget)
        QMetaObject.connectSlotsByName(logoWidget)

    def retranslateUi(self, logoWidget):
        logoWidget.setWindowTitle(QCoreApplication.translate("logoWidget", "Form", None))
        self.logoLabel.setText(QCoreApplication.translate("logoWidget", "LocUST", None))

class Ui_navigationWidget(object):
    logsButtonClicked = pyqtSignal()
    def setupUi(self, navigationWidget):
        if not navigationWidget.objectName():
            navigationWidget.setObjectName("navigationWidget")
        navigationWidget.setStyleSheet("background-color: transparent;")

        self.navigationLayout = QVBoxLayout(navigationWidget)
        self.navigationLayout.setSpacing(0)
        self.navigationLayout.setContentsMargins(5, 5, 5, 5)



        self.mainMenuLabel = self.create_label("Main Menu", "mainMenuLabel")
        self.dashboardButton = self.create_button("Dashboard", "dashboardButton", "home.png")
        self.inboxdButton = self.create_button("Inbox", "inboxdButton", "paper-plane.png")

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
        self.navigationLayout.addWidget(self.inboxdButton)

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
        button.setText("  " + text)  # Adding spaces for padding before the text
        button.setIcon(QIcon(f"buttonIcons/{iconPath}"))
        button.setIconSize(QSize(20, 20))  # Set your desired icon size

        # Stylesheet with hover and pressed states
        button.setStyleSheet(f"""
                    QPushButton {{
                        color: {textColor}; 
                        font: 75 {menuItemFontSize}pt '{font}';
                        padding-left: 30px; /* Size of the icon plus desired spacing */
                        text-align: left;
                        border: none; /* Remove border */
                        background-color: transparent;
                    }}
                    QPushButton:hover {{
                        background-color: rgb(220, 220, 220); /* Lighter shade for hover */
                    }}
                    QPushButton:pressed {{
                        background-color: rgb(190, 190, 190); /* Even lighter for pressed */
                    }}
                    QPushButton::icon {{
                        margin-left: -25px; /* Negative margin to align the icon with the button edge */
                        padding-left: 10px;
                    }}
                """)

        button.setMinimumHeight(40)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return button

    def create_label(self, text, objectName):
        label = QLabel()
        label.setObjectName(objectName)
        label.setText(text)
        label.setStyleSheet(f"color: {textColor}; font: 75 {menuItemFontSizeSecondary} '{font}'; padding-left: 10px;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return label



class Ui_userHeaderWidget(object):
    def setupUi(self, userHeaderWidget):
        if not userHeaderWidget.objectName():
            userHeaderWidget.setObjectName(u"userHeaderWidget")

        userHeaderWidget.setStyleSheet(u"background-color: transparent; color:black;")
        self.userHeaderLayout = QHBoxLayout(userHeaderWidget)
        self.userHeaderLayout.setSpacing(10)
        self.userHeaderLayout.setObjectName(u"userHeaderLayout")
        self.userHeaderLayout.setContentsMargins(10, 10, 10, 10)

        font = "font: 75 16pt 'Copperplate';"
        buttonStyleSheet = """
            QPushButton {
                border: none;
                border-radius: 20px;  /* Half of width and height to make it circular */
                background-color: rgb(129, 117, 102);  /* Your desired background color for the normal state */
            }
            QPushButton:hover {
                background-color: lightgrey;  /* Your desired background color when hovered */
            }
            QPushButton:pressed {
                background-color: grey;  /* Your desired background color when pressed */
            }
        """

        self.searchIcon = QPushButton(userHeaderWidget)
        self.searchIcon.setObjectName(u"searchIcon")
        self.searchIcon.setIcon(QIcon("buttonIcons/search.png"))
        self.searchIcon.setIconSize(QSize(24, 24))
        self.searchIcon.setStyleSheet(buttonStyleSheet)
        self.searchIcon.setFixedSize(40, 40)
        self.userHeaderLayout.addWidget(self.searchIcon)


        self.searchBar = QLineEdit(userHeaderWidget)
        self.searchBar.setObjectName(u"searchBar")
        self.searchBar.setFixedHeight(24)
        self.userHeaderLayout.addWidget(self.searchBar)


        self.settingsButton = QPushButton(userHeaderWidget)
        self.settingsButton.setObjectName("settingsButton")
        self.settingsButton.setIcon(QIcon("buttonIcons/settings.png"))
        self.settingsButton.setIconSize(QSize(24, 24))
        self.settingsButton.setStyleSheet(buttonStyleSheet)
        self.settingsButton.setFixedSize(40, 40)
        self.userHeaderLayout.addWidget(self.settingsButton)

        self.notificationButton = QPushButton(userHeaderWidget)
        self.notificationButton.setObjectName("notificationButton")
        self.notificationButton.setIcon(QIcon("buttonIcons/bell.png"))  # Replace with your icon's path
        self.notificationButton.setIconSize(QSize(24, 24))  # Icon size
        self.notificationButton.setStyleSheet(buttonStyleSheet)
        self.notificationButton.setFixedSize(40, 40)  # Adjust size as needed
        self.userHeaderLayout.addWidget(self.notificationButton)

        self.employeeProfile = QPushButton(userHeaderWidget)
        self.employeeProfile.setObjectName("employeeProfile")
        self.employeeProfile.setIcon(QIcon("buttonIcons/user.png"))  # Replace with your icon's path
        self.employeeProfile.setIconSize(QSize(24, 24))  # Icon size, adjust as needed
        self.employeeProfile.setStyleSheet(buttonStyleSheet)
        self.employeeProfile.setFixedSize(40, 40)
        self.userHeaderLayout.addWidget(self.employeeProfile)

        self.employeeName = QLabel(userHeaderWidget)
        self.employeeName.setObjectName(u"employeeName")
        self.employeeName.setText("Nickholas Delavallierre")
        self.employeeName.setStyleSheet(font)
        self.userHeaderLayout.addWidget(self.employeeName)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        self.employeeName.setGraphicsEffect(opacity_effect)


        self.retranslateUi(userHeaderWidget)

        QMetaObject.connectSlotsByName(userHeaderWidget)
    # setupUi

    def retranslateUi(self, userHeaderWidget):
        userHeaderWidget.setWindowTitle(QCoreApplication.translate("userHeaderWidget", u"Form", None))
        self.searchIcon.setText("")
        self.notificationButton.setText("")
        self.employeeProfile.setText("")

class Ui_dashboardWidget(object):
    def setupUi(self, dashboardWidget):
        if not dashboardWidget.objectName():
            dashboardWidget.setObjectName(u"dashboardWidget")
        dashboardWidget.setStyleSheet(u"background-color: transparent; color:black;")
        self.dashboardLayout = QHBoxLayout(dashboardWidget)
        self.dashboardLayout.setSpacing(10)
        self.dashboardLayout.setObjectName(u"dashboardLayout")
        self.dashboardLayout.setContentsMargins(10, 10, 10, 10)
        self.leftFrame = QFrame(dashboardWidget)
        self.leftFrame.setObjectName(u"leftFrame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftFrame.sizePolicy().hasHeightForWidth())
        self.leftFrame.setSizePolicy(sizePolicy)
        self.leftFrame.setFrameShape(QFrame.StyledPanel)
        self.leftFrame.setFrameShadow(QFrame.Raised)
        self.leftLayout = QVBoxLayout(self.leftFrame)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(0, 0, 0, 0)
        self.entWidget = QFrame(self.leftFrame)
        self.entWidget.setObjectName(u"entWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(5)
        sizePolicy1.setHeightForWidth(self.entWidget.sizePolicy().hasHeightForWidth())
        self.entWidget.setSizePolicy(sizePolicy1)
        self.entWidget.setFrameShape(QFrame.StyledPanel)
        self.entWidget.setFrameShadow(QFrame.Raised)
        self.entLayout = QHBoxLayout(self.entWidget)
        self.entLayout.setObjectName(u"entLayout")
        self.iunContainer = QFrame(self.entWidget)
        self.iunContainer.setObjectName(u"iunContainer")
        self.iunContainer.setStyleSheet(u"background-color: rgb(250, 245, 232);\n"
"border: 2px solid rgb(129, 117, 102);\n"
"border-radius: 20px;")
        self.iunContainer.setFrameShape(QFrame.StyledPanel)
        self.iunContainer.setFrameShadow(QFrame.Raised)
        self.iunLayout = QVBoxLayout(self.iunContainer)
        self.iunLayout.setSpacing(10)
        self.iunLayout.setObjectName(u"iunLayout")
        self.iunLayout.setContentsMargins(10, 10, 10, 10)

        self.iULabel = QLabel("Users")
        self.iULabel.setObjectName(u"iULabel")
        self.iULabel.setStyleSheet(u"font: 75 24pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.iULabel.setTextFormat(Qt.PlainText)
        self.iunLayout.addWidget(self.iULabel, 0, Qt.AlignHCenter)


        self.iUNumber = QLabel("0")
        self.iUNumber.setObjectName(u"iUNumber")
        self.iUNumber.setStyleSheet(u"font: 75 36pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.iUNumber.setTextFormat(Qt.PlainText)
        self.iunLayout.addWidget(self.iUNumber, 0, Qt.AlignHCenter)
        self.entLayout.addWidget(self.iunContainer)


        self.techNumberContainer = QFrame(self.entWidget)
        self.techNumberContainer.setObjectName(u"techNumberContainer")
        self.techNumberContainer.setStyleSheet(u"background-color: rgb(250, 245, 232);\n"
"border: 2px solid rgb(129, 117, 102);\n"
"border-radius: 20px;")
        self.techNumberContainer.setFrameShape(QFrame.StyledPanel)
        self.techNumberContainer.setFrameShadow(QFrame.Raised)
        self.techNumberLayout = QVBoxLayout(self.techNumberContainer)
        self.techNumberLayout.setSpacing(10)
        self.techNumberLayout.setObjectName(u"techNumberLayout")
        self.techNumberLayout.setContentsMargins(10, 10, 10, 10)

        self.techLabel = QLabel("Desk Technicians")
        self.techLabel.setObjectName(u"techLabel")
        self.techLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.techLabel.setTextFormat(Qt.PlainText)

        self.techNumberLayout.addWidget(self.techLabel, 0, Qt.AlignHCenter)

        self.techNumber = QLabel("0")
        self.techNumber.setObjectName(u"techNumber")
        self.techNumber.setStyleSheet(u"font: 75 36pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.techNumber.setTextFormat(Qt.PlainText)

        self.techNumberLayout.addWidget(self.techNumber, 0, Qt.AlignHCenter)


        self.entLayout.addWidget(self.techNumberContainer)

        self.empNumberContainer = QFrame(self.entWidget)
        self.empNumberContainer.setObjectName(u"empNumberContainer")
        self.empNumberContainer.setStyleSheet(u"background-color: rgb(250, 245, 232);\n"
"border: 2px solid rgb(129, 117, 102);\n"
"border-radius: 20px;")
        self.empNumberContainer.setFrameShape(QFrame.StyledPanel)
        self.empNumberContainer.setFrameShadow(QFrame.Raised)
        self.empNumberLayout = QVBoxLayout(self.empNumberContainer)
        self.empNumberLayout.setSpacing(10)
        self.empNumberLayout.setObjectName(u"empNumberLayout")
        self.empNumberLayout.setContentsMargins(10, 10, 10, 10)
        self.mangerLabel = QLabel("Security Managers")
        self.mangerLabel.setObjectName(u"mangerLabel")
        self.mangerLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.mangerLabel.setTextFormat(Qt.PlainText)

        self.empNumberLayout.addWidget(self.mangerLabel, 0, Qt.AlignHCenter)

        self.managerNum = QLabel("0")
        self.managerNum.setObjectName(u"managerNum")
        self.managerNum.setStyleSheet(u"font: 75 36pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.managerNum.setTextFormat(Qt.PlainText)

        self.empNumberLayout.addWidget(self.managerNum, 0, Qt.AlignHCenter)


        self.entLayout.addWidget(self.empNumberContainer)


        self.leftLayout.addWidget(self.entWidget)

        self.scanInfoWidget = QFrame(self.leftFrame)
        self.scanInfoWidget.setObjectName(u"scanInfoWidget")
        sizePolicy1.setHeightForWidth(self.scanInfoWidget.sizePolicy().hasHeightForWidth())
        self.scanInfoWidget.setSizePolicy(sizePolicy1)
        self.scanInfoWidget.setFrameShape(QFrame.StyledPanel)
        self.scanInfoWidget.setFrameShadow(QFrame.Raised)
        self.scanInfoLayout = QHBoxLayout(self.scanInfoWidget)
        self.scanInfoLayout.setObjectName(u"scanInfoLayout")
        self.canScanTodayContainer = QFrame(self.scanInfoWidget)
        self.canScanTodayContainer.setObjectName(u"canScanTodayContainer")
        self.canScanTodayContainer.setStyleSheet(u"background-color: rgb(250, 245, 232);\n"
"border: 2px solid rgb(129, 117, 102);\n"
"border-radius: 20px;")
        self.canScanTodayContainer.setFrameShape(QFrame.StyledPanel)
        self.canScanTodayContainer.setFrameShadow(QFrame.Raised)
        self.canScanTodayLayout = QVBoxLayout(self.canScanTodayContainer)
        self.canScanTodayLayout.setSpacing(10)
        self.canScanTodayLayout.setObjectName(u"canScanTodayLayout")
        self.canScanTodayLayout.setContentsMargins(10, 10, 10, 10)
        self.userScheduleTodayLabel = QLabel("Scheduled For Today")
        self.userScheduleTodayLabel.setObjectName(u"userScheduleTodayLabel")
        self.userScheduleTodayLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.userScheduleTodayLabel.setTextFormat(Qt.PlainText)

        self.canScanTodayLayout.addWidget(self.userScheduleTodayLabel, 0, Qt.AlignHCenter)

        self.userScheduleTodayNumber = QLabel("0")
        self.userScheduleTodayNumber.setObjectName(u"userScheduleTodayNumber")
        self.userScheduleTodayNumber.setStyleSheet(u"font: 75 36pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.userScheduleTodayNumber.setTextFormat(Qt.PlainText)

        self.canScanTodayLayout.addWidget(self.userScheduleTodayNumber, 0, Qt.AlignHCenter)


        self.scanInfoLayout.addWidget(self.canScanTodayContainer)

        self.scansTodayWidget = QFrame(self.scanInfoWidget)
        self.scansTodayWidget.setObjectName(u"scansTodayWidget")
        self.scansTodayWidget.setStyleSheet(u"background-color: rgb(250, 245, 232);\n"
"border: 2px solid rgb(129, 117, 102);\n"
"border-radius: 20px;")
        self.scansTodayWidget.setFrameShape(QFrame.StyledPanel)
        self.scansTodayWidget.setFrameShadow(QFrame.Raised)
        self.scansTodayLayout = QVBoxLayout(self.scansTodayWidget)
        self.scansTodayLayout.setSpacing(10)
        self.scansTodayLayout.setObjectName(u"scansTodayLayout")
        self.scansTodayLayout.setContentsMargins(10, 10, 10, 10)
        self.scansTodayLabel = QLabel("Scans Today")
        self.scansTodayLabel.setObjectName(u"scansTodayLabel")
        self.scansTodayLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.scansTodayLabel.setTextFormat(Qt.PlainText)

        self.scansTodayLayout.addWidget(self.scansTodayLabel, 0, Qt.AlignHCenter)

        self.scansTodayNumber = QLabel("0")
        self.scansTodayNumber.setObjectName(u"scansTodayNumber")
        self.scansTodayNumber.setStyleSheet(u"font: 75 36pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")

        self.scansTodayLayout.addWidget(self.scansTodayNumber, 0, Qt.AlignHCenter)


        self.scanInfoLayout.addWidget(self.scansTodayWidget)

        self.scansThisWeekContainer = QFrame(self.scanInfoWidget)
        self.scansThisWeekContainer.setObjectName(u"scansThisWeekContainer")
        self.scansThisWeekContainer.setStyleSheet(u"background-color: rgb(250, 245, 232);\n"
"border: 2px solid rgb(129, 117, 102);\n"
"border-radius: 20px;")
        self.scansThisWeekContainer.setFrameShape(QFrame.StyledPanel)
        self.scansThisWeekContainer.setFrameShadow(QFrame.Raised)
        self.scansThisWeekLayout = QVBoxLayout(self.scansThisWeekContainer)
        self.scansThisWeekLayout.setSpacing(10)
        self.scansThisWeekLayout.setObjectName(u"scansThisWeekLayout")
        self.scansThisWeekLayout.setContentsMargins(10, 10, 10, 10)
        self.scansThisWeekLabel = QLabel("Scans This Week")
        self.scansThisWeekLabel.setObjectName(u"scansThisWeekLabel")
        self.scansThisWeekLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.scansThisWeekLabel.setTextFormat(Qt.PlainText)

        self.scansThisWeekLayout.addWidget(self.scansThisWeekLabel, 0, Qt.AlignHCenter)

        self.scansThisWeekNumber = QLabel("0")
        self.scansThisWeekNumber.setObjectName(u"scansThisWeekNumber")
        self.scansThisWeekNumber.setStyleSheet(u"font: 75 36pt \"Garamond\";\n"
"background-color: transparent;\n"
"border: none;\n"
"border-radius: 20px;")
        self.scansThisWeekNumber.setTextFormat(Qt.PlainText)

        self.scansThisWeekLayout.addWidget(self.scansThisWeekNumber, 0, Qt.AlignHCenter)


        self.scanInfoLayout.addWidget(self.scansThisWeekContainer)


        self.leftLayout.addWidget(self.scanInfoWidget)



        #Graph
        #--------------------------------------------------------------------------------------------------------------

        self.setupGraphWidget()








        self.leftLayout.addWidget(self.graphWidget)
        self.dashboardLayout.addWidget(self.leftFrame)
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
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(0, 0, 0, 0)



        #DateTime
        #------------------------------------------------------------------------------------------------

        self.dateTimeWidget = QFrame(self.rightFrame)
        self.dateTimeWidget.setObjectName(u"dateTimeWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.dateTimeWidget.sizePolicy().hasHeightForWidth())
        self.dateTimeWidget.setSizePolicy(sizePolicy4)
        self.dateTimeWidget.setStyleSheet(u"background-color: rgb(250, 245, 232);\n"
                                          "border: 2px solid rgb(129, 117, 102);\n"
                                          "border-radius: 20px;")
        self.dateTimeWidget.setFrameShape(QFrame.StyledPanel)
        self.dateTimeWidget.setFrameShadow(QFrame.Raised)
        self.dateTimeLayout = QVBoxLayout(self.dateTimeWidget)
        self.dateTimeLayout.setSpacing(0)
        self.dateTimeLayout.setObjectName(u"dateTimeLayout")
        self.dateTimeLayout.setContentsMargins(10, 10, 10, 10)

        self.dateLabel = QLabel(self.dateTimeWidget)
        self.dateLabel.setObjectName(u"dateLabel")
        self.dateLabel.setStyleSheet(u"font: 75 18pt \"Garamond\";\n"
                                     "background-color: transparent;\n"
                                     "border: none;\n"
                                     "border-radius: 20px;")
        self.dateLabel.setTextFormat(Qt.PlainText)
        self.update_date_label()
        self.dateTimeLayout.addWidget(self.dateLabel)


        self.timeLabel = QLabel(self.dateTimeWidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";\n"
                                     "background-color: transparent;\n"
                                     "border: none;\n"
                                     "border-radius: 20px;")
        self.timeLabel.setTextFormat(Qt.PlainText)
        self.update_time_label()
        self.dateTimeLayout.addWidget(self.timeLabel)

        self.rightLayout.addWidget(self.dateTimeWidget)



        #Current Tickets
        #---------------------------------------------------------------------------------------

        self.ticketsNumContainer = QFrame(self.rightFrame)
        self.ticketsNumContainer.setObjectName(u"ticketsNumContainer")
        sizePolicy4.setHeightForWidth(self.ticketsNumContainer.sizePolicy().hasHeightForWidth())
        self.ticketsNumContainer.setSizePolicy(sizePolicy4)
        self.ticketsNumContainer.setStyleSheet(u"background-color: rgb(250, 245, 232);\n"
                                               "border: 2px solid rgb(129, 117, 102);\n"
                                               "border-radius: 20px;")
        self.ticketsNumContainer.setFrameShape(QFrame.StyledPanel)
        self.ticketsNumContainer.setFrameShadow(QFrame.Raised)
        self.ticketNumberLayout = QVBoxLayout(self.ticketsNumContainer)
        self.ticketNumberLayout.setSpacing(10)
        self.ticketNumberLayout.setObjectName(u"ticketNumberLayout")
        self.ticketNumberLayout.setContentsMargins(10, 10, 10, 10)
        self.currentTicketLabel = QLabel(self.ticketsNumContainer)
        self.currentTicketLabel.setObjectName(u"currentTicketLabel")
        self.currentTicketLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";\n"
                                              "background-color: transparent;\n"
                                              "border: none;\n"
                                              "border-radius: 20px;")
        self.currentTicketLabel.setTextFormat(Qt.PlainText)
        self.currentTicketLabel.setText("Current Tickets")
        self.ticketNumberLayout.addWidget(self.currentTicketLabel, 0, Qt.AlignHCenter)

        self.currentNumOfTickets = QLabel(self.ticketsNumContainer)
        self.currentNumOfTickets.setObjectName(u"currentNumOfTickets")
        self.currentNumOfTickets.setStyleSheet(u"font: 75 36pt \"Garamond\";\n"
                                               "background-color: transparent;\n"
                                               "border: none;\n"
                                               "border-radius: 20px;")
        self.currentNumOfTickets.setFrameShadow(QFrame.Raised)
        self.currentNumOfTickets.setTextFormat(Qt.PlainText)
        self.currentNumOfTickets.setText("0")

        self.ticketNumberLayout.addWidget(self.currentNumOfTickets, 0, Qt.AlignHCenter)

        self.rightLayout.addWidget(self.ticketsNumContainer)







        #Spacer
        #-------------------------------------------------------------------------------
        self.verticalSpacer = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.rightLayout.addItem(self.verticalSpacer)







        # Recent Scans
        #-----------------------------------------
        self.recentScansHeader = QFrame(self.rightFrame)
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
        self.recentscansLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";")
        recentScansHeaderLayout.addWidget(self.recentscansLabel)

        self.rightLayout.addWidget(self.recentScansHeader)




        for i in self.last5Scanned():
            user = dbu.get_user_by_id(i[0])
            photo_path = f"../Database/IndirectUsers/photos/{user.photos}"
            name = f"{user.firstName} {user.lastName}"
            id = user.id
            date_time = i[1]
            recentScan = self.create_recent_scan_widget(photo_path, name, id, date_time)

            self.rightLayout.addWidget(recentScan)


        # x1 = self.create_recent_scan_widget("buttonIcons/user.png", "Nicholas Delavalliere", "0001", "11/5/23 10:11pm")
        # x2 = self.create_recent_scan_widget("buttonIcons/user.png", "Nicholas Delavalliere", "0001", "11/5/23 10:11pm")
        # x3= self.create_recent_scan_widget("buttonIcons/user.png", "Nicholas Delavalliere", "0001", "11/5/23 10:11pm")
        # x4= self.create_recent_scan_widget("buttonIcons/user.png", "Nicholas Delavalliere", "0001", "11/5/23 10:11pm")
        # x5 = self.create_recent_scan_widget("buttonIcons/user.png", "Nicholas Delavalliere", "0001", "11/5/23 10:11pm")
        # self.rightLayout.addWidget(x1)
        # self.rightLayout.addWidget(x2)
        # self.rightLayout.addWidget(x3)
        # self.rightLayout.addWidget(x4)
        # self.rightLayout.addWidget(x5)

        self.rightFrame.update()


        self.dashboardLayout.addWidget(self.rightFrame)


        self.retranslateUi(dashboardWidget)

        self.getData()
    # setupUi

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

    def retranslateUi(self, dashboardWidget):
        dashboardWidget.setWindowTitle(QCoreApplication.translate("dashboardWidget", u"Form", None))

    def create_recent_scan_widget(self, user_image_path, user_name_text, user_id_text, scan_date_time_text):
        recentScansWidget = QFrame()
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
        recentScans.setStyleSheet("background-color: rgb(250, 245, 232);"
                                  "border: 2px solid rgb(129, 117, 102);"
                                  "border-radius: 20px;")
        recentScans.setFrameShape(QFrame.StyledPanel)
        recentScans.setFrameShadow(QFrame.Raised)
        recentScansLayout = QHBoxLayout(recentScans)
        recentScansLayout.setSpacing(5)
        recentScansLayout.setContentsMargins(10, 10, 10, 10)

        # Image Container within Recent Scan Information
        imgContainer = QFrame(recentScans)
        imgContainer.setObjectName("imgContainer")
        imgContainer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        imgContainer.setStyleSheet("background-color: transparent;"
                                   "border: none;"
                                   "border-radius: 20px;")
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
        userInfo.setStyleSheet("background-color: transparent;"
                               "border: none;"
                               "border-radius: 20px;")
        userInfoLayout = QVBoxLayout(userInfo)
        userInfoLayout.setSpacing(5)
        userInfoLayout.setContentsMargins(0, 0, 0, 0)

        # User ID Label
        userID = QLabel(userInfo)
        userID.setObjectName("userID")
        userID.setStyleSheet("font: 75 18pt 'Garamond';")
        userID.setText(user_id_text)
        userInfoLayout.addWidget(userID)

        # User Name Label
        userName = QLabel(userInfo)
        userName.setObjectName("userName")
        userName.setStyleSheet("font: 75 18pt 'Garamond';")
        userName.setText(user_name_text)
        userInfoLayout.addWidget(userName)

        # Scan Date Time Label
        scanDateTime = QLabel(userInfo)
        scanDateTime.setObjectName("scanDateTime")
        scanDateTime.setStyleSheet("font: 75 18pt 'Garamond';")
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
        sizePolicy.setVerticalStretch(10)
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setStyleSheet("background-color: rgb(250, 245, 232);"
                                       "border: 2px solid rgb(129, 117, 102);"
                                       "border-radius: 20px;")
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
        self.plotLineGraph()


    def plotBarGraph(self):
        # Simulated data for user scans
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        users_scanned = [20, 35, 30, 15, 40, 60, 45]  # Random user counts for each day

        # Convert RGB to Matplotlib color format
        def convert_rgb_to_mpl(color):
            return tuple(c / 255 for c in color)

        # Define your colors
        bg_color = convert_rgb_to_mpl((250, 245, 232))
        font_color = convert_rgb_to_mpl((129, 117, 102))
        bar_color = convert_rgb_to_mpl((129, 117, 102))

        ax = self.figure.add_subplot(111)

        # Set the background color for the Axes (plot area)
        ax.set_facecolor(bg_color)

        # Set the graph title, labels, and font properties
        ax.set_title('Users Scanned per Day', fontsize=18, fontname='Garamond', color=font_color)
        ax.set_xlabel('Days of the Week', fontsize=18, fontname='Garamond', color=font_color)
        ax.set_ylabel('Number of Users Scanned', fontsize=18, fontname='Garamond', color=font_color)

        # Plot the bar chart with the specified bar color
        bars = ax.bar(days_of_week, users_scanned, color=[bar_color] * len(days_of_week))

        # Change the font of the ticks on x and y axis
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname('Garamond')
            label.set_fontsize(18)  # Adjust the size as needed

        ax.patch.set_visible(False)

        # Redraw the canvas to reflect the changes
        self.canvas.draw()

    def plotLineGraph(self):
        # Simulated data for user scans
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        users_scanned = [20, 35, 30, 15, 40, 60, 45]  # Random user counts for each day

        # Convert RGB to Matplotlib color format
        def convert_rgb_to_mpl(color):
            return tuple(c / 255 for c in color)

        # Define your colors
        bg_color = convert_rgb_to_mpl((250, 245, 232))
        font_color = convert_rgb_to_mpl((129, 117, 102))
        line_color = convert_rgb_to_mpl((129, 117, 102))

        # Clear the previous figure to prepare for a new plot
        self.figure.clf()

        ax = self.figure.add_subplot(111)

        # Set the background color for the Axes (plot area)
        ax.set_facecolor(bg_color)

        # Set the graph title, labels, and font properties
        ax.set_title('Users Scanned per Day', fontsize=18, fontname='Garamond', color=font_color)
        ax.set_xlabel('Days of the Week', fontsize=18, fontname='Garamond', color=font_color)
        ax.set_ylabel('Number of Users Scanned', fontsize=18, fontname='Garamond', color=font_color)

        # Plot the line chart with the specified line color
        ax.plot(days_of_week, users_scanned, marker='o', linestyle='-', color=line_color)

        # Change the font of the ticks on x and y axis
        for label in (ax.get_xticklabels() + ax.get_yticklabels()):
            label.set_fontname('Garamond')
            label.set_fontsize(18)  # Adjust the size as needed

        ax.patch.set_visible(False)

        # Redraw the canvas to reflect the changes
        self.canvas.draw()

    def getData(self):
        # Indirect User number set text
        self.iUNumber.setText(str(len(dbu.users)))

         # employee Numbers
        deskTechs = []
        securityManager = []
        all_employees = dbe.get_all_employees()
        for emp in all_employees:
            if emp.title == "Security Manager":
                securityManager.append(emp)
            elif emp.title == "Desk Technician":
                deskTechs.append(emp)
            else:
                pass
        self.managerNum.setText(str(len(securityManager)))
        self.techNumber.setText(str(len(deskTechs)))

        # who is scheduled for today
        now = datetime.now()
        current_day_of_week = now.strftime("%A")
        self.userScheduleTodayNumber.setText(str(len(entitiesMain.getSchedule(current_day_of_week))))

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

        self.scansTodayNumber.setText(str(len(users_scanned_today)))

        # get users scanned this week
        start_of_week = now - timedelta(days=now.weekday())
        users_scanned_this_week = [log for log in logs if start_of_week.date() <= datetime.strptime(log['Timestamp'],
                                                                                                    '%Y-%m-%d %H:%M:%S').date() <= now.date()]

        self.scansThisWeekNumber.setText(str(len(users_scanned_this_week)))



    def last5Scanned(self):
        logs_directory = "../Database/Logs/log.csv"
        with open(logs_directory, mode='r') as file:
            reader = csv.DictReader(file)
            logs = list(reader)

            # get last 5 users scanned
            last_5_users_scanned = logs[-3:] if len(logs) >= 3 else logs

            # Extract user IDs and timestamps from the last 5 scanned entries
            user_ids_and_times = [(log['UserID'], log['Timestamp']) for log in last_5_users_scanned]

            return user_ids_and_times

class Ui_logs(object):
    def setupUi(self, logs):
        if not logs.objectName():
            logs.setObjectName("logs")

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
        label.setFixedSize(40, 40)

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

        # Setup the search functionality
        search_input.textChanged.connect(lambda: self.searchTable(object_name + "TableView", search_input.text()))

        # Add search input to the search layout
        search_layout.addWidget(search_input)

        # Save button setup
        save_button = QPushButton(search_widget)
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
        self.tableView.setObjectName(u"tableView")

        self.rightLayout.addWidget(self.tableView)


        self.scheduleLayout.addWidget(self.rightWidget)

class Ui_ticketsWidget(object):
    def setupUi(self, ticketsWidget):
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
        self.leftWidget.setStyleSheet(u"background-color: rgb(250, 245, 232);"
                                      "border: 2px solid rgb(129, 117, 102);"
                                      "border-radius: 20px;")
        self.leftWidget.setFrameShape(QFrame.StyledPanel)
        self.leftWidget.setFrameShadow(QFrame.Raised)
        self.leftLayout = QVBoxLayout(self.leftWidget)
        self.leftLayout.setSpacing(10)
        self.leftLayout.setObjectName(u"leftLayout")
        self.leftLayout.setContentsMargins(10, 10, 10, 10)
        self.ticketNameLabel = QLabel(self.leftWidget)
        self.ticketNameLabel.setObjectName(u"ticketNameLabel")
        self.ticketNameLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";"
                                           "background-color: transparent;"
                                           "border: none;"
                                           "border-radius: 20px;")
        self.leftLayout.addWidget(self.ticketNameLabel, 0, Qt.AlignHCenter)
        self.ticketTextEdit = QTextEdit(self.leftWidget)
        self.ticketTextEdit.setObjectName(u"ticketTextEdit")
        self.ticketTextEdit.setStyleSheet(u"background-color: white;"
                                          "border: none;"
                                          "border-radius: 20px;"
                                          "font: 75 16pt \"Garamond\";")
        self.leftLayout.addWidget(self.ticketTextEdit)
        self.resolvedButton = QPushButton("Resolved")
        self.resolvedButton.clicked.connect(self.deleteCurrentFile)
        self.resolvedButton.setObjectName(u"resolvedButton")
        self.resolvedButton.setStyleSheet(u"background-color: transparent;"
                                          "border: none;"
                                          "border-radius: 20px;"
                                          "font: 75 24pt \"Garamond\";")
        self.leftLayout.addWidget(self.resolvedButton)
        self.ticketsLayout.addWidget(self.leftWidget)
        self.rightWidget = QFrame(ticketsWidget)
        self.rightWidget.setObjectName(u"rightWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.rightWidget.sizePolicy().hasHeightForWidth())
        self.rightWidget.setSizePolicy(sizePolicy1)
        self.rightWidget.setStyleSheet(u"background-color: rgb(250, 245, 232);"
                                       "border: 2px solid rgb(129, 117, 102);"
                                       "border-radius: 20px;")
        self.rightWidget.setFrameShape(QFrame.StyledPanel)
        self.rightWidget.setFrameShadow(QFrame.Raised)
        self.rightLayout = QVBoxLayout(self.rightWidget)
        self.rightLayout.setSpacing(10)
        self.rightLayout.setObjectName(u"rightLayout")
        self.rightLayout.setContentsMargins(10, 10, 10, 10)
        self.ticketLabel = QLabel("Tickets")
        self.ticketLabel.setObjectName(u"ticketLabel")
        self.ticketLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";"
                                       "background-color: transparent;"
                                       "border: none;"
                                       "border-radius: 20px;")
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

    def create_ticket_button(self, text, font_family="Garamond", font_size=24, font_weight=75):
        ticket_button = QPushButton()
        ticket_button.setObjectName(u"ticketButton")
        ticket_button.setText(text)
        style = f"font: {font_weight} {font_size}pt \"{font_family}\";"
        ticket_button.setStyleSheet(style)
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
        addUserWidget.setStyleSheet(u"background-color: transparent; color:black;")
        self.addUserLayout = QVBoxLayout(addUserWidget)
        self.addUserLayout.setSpacing(10)
        self.addUserLayout.setContentsMargins(10, 10, 10, 10)
        self.accountOrganizationFrame = QFrame(addUserWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.accountOrganizationFrame.sizePolicy().hasHeightForWidth())
        self.accountOrganizationFrame.setSizePolicy(sizePolicy)
        self.accountOrganizationLayout = QHBoxLayout(self.accountOrganizationFrame)
        self.accountOrganizationLayout.setSpacing(10)
        self.accountOrganizationLayout.setContentsMargins(0, 0, 0, 0)
        self.accountFrame = QFrame(self.accountOrganizationFrame)
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.accountFrame.sizePolicy().hasHeightForWidth())
        self.accountFrame.setSizePolicy(sizePolicy1)
        self.accountLayout = QVBoxLayout(self.accountFrame)
        self.accountLayout.setSpacing(0)
        self.accountLayout.setContentsMargins(0, 0, 0, 0)
        self.accountLabel = QLabel("Account")
        self.accountLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";")
        self.accountLayout.addWidget(self.accountLabel)
        self.accountForm = QFrame(self.accountFrame)
        self.accountForm.setStyleSheet(u"font: 75 16pt \"Garamond\";")
        self.accountFormLayout = QFormLayout(self.accountForm)
        self.accountFormLayout.setHorizontalSpacing(10)
        self.accountFormLayout.setVerticalSpacing(10)
        self.accountFormLayout.setContentsMargins(10, 10, 10, 10)
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
        sizePolicy1.setHeightForWidth(self.organizationFrame.sizePolicy().hasHeightForWidth())
        self.organizationFrame.setSizePolicy(sizePolicy1)
        self.organizationLayout = QVBoxLayout(self.organizationFrame)
        self.organizationLayout.setSpacing(0)
        self.organizationLayout.setContentsMargins(0, 0, 0, 0)
        self.organizationLabel = QLabel("Organization")
        self.organizationLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";")
        self.organizationLayout.addWidget(self.organizationLabel)
        self.organizationForm = QFrame(self.organizationFrame)
        self.organizationForm.setStyleSheet(u"font: 75 16pt \"Garamond\";")
        self.organizationFormLayout = QFormLayout(self.organizationForm)
        self.organizationFormLayout.setHorizontalSpacing(10)
        self.organizationFormLayout.setVerticalSpacing(10)
        self.organizationFormLayout.setContentsMargins(10, 10, 10, 10)
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
        sizePolicy.setHeightForWidth(self.scheduleFrame.sizePolicy().hasHeightForWidth())
        self.scheduleFrame.setSizePolicy(sizePolicy)
        self.scheduleLayout = QVBoxLayout(self.scheduleFrame)
        self.scheduleLayout.setSpacing(0)
        self.scheduleLayout.setContentsMargins(0, 0, 0, 0)
        self.scheduleLabel = QLabel("Schedule")
        self.scheduleLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";")
        self.scheduleLayout.addWidget(self.scheduleLabel)
        self.scheduleForm = QFrame(self.scheduleFrame)
        self.scheduleForm.setStyleSheet(u"font: 75 16pt \"Garamond\";")
        self.scheduleFormLayout = QGridLayout(self.scheduleForm)
        self.scheduleFormLayout.setSpacing(10)
        self.scheduleFormLayout.setContentsMargins(10, 10, 10, 10)
        self.timeEditStartMonday = QTimeEdit(self.scheduleForm)
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
        sizePolicy2.setHeightForWidth(self.timeEditStartThursday.sizePolicy().hasHeightForWidth())
        self.timeEditStartThursday.setSizePolicy(sizePolicy2)
        self.timeEditStartThursday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartThursday, 5, 1, 1, 1)
        self.timeEditEndThursday = QTimeEdit(self.scheduleForm)
        sizePolicy2.setHeightForWidth(self.timeEditEndThursday.sizePolicy().hasHeightForWidth())
        self.timeEditEndThursday.setSizePolicy(sizePolicy2)
        self.timeEditEndThursday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndThursday, 5, 3, 1, 1)
        self.timeEditStartWednesday = QTimeEdit(self.scheduleForm)
        sizePolicy2.setHeightForWidth(self.timeEditStartWednesday.sizePolicy().hasHeightForWidth())
        self.timeEditStartWednesday.setSizePolicy(sizePolicy2)
        self.timeEditStartWednesday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartWednesday, 4, 1, 1, 1)
        self.timeEditEndSaturday = QTimeEdit(self.scheduleForm)
        sizePolicy2.setHeightForWidth(self.timeEditEndSaturday.sizePolicy().hasHeightForWidth())
        self.timeEditEndSaturday.setSizePolicy(sizePolicy2)
        self.timeEditEndSaturday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndSaturday, 7, 3, 1, 1)
        self.dayLabel = QLabel("Day")
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
        sizePolicy2.setHeightForWidth(self.timeEditEndWednesday.sizePolicy().hasHeightForWidth())
        self.timeEditEndWednesday.setSizePolicy(sizePolicy2)
        self.timeEditEndWednesday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndWednesday, 4, 3, 1, 1)
        self.timeEditEndSunday = QTimeEdit(self.scheduleForm)
        sizePolicy2.setHeightForWidth(self.timeEditEndSunday.sizePolicy().hasHeightForWidth())
        self.timeEditEndSunday.setSizePolicy(sizePolicy2)
        self.timeEditEndSunday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndSunday, 1, 3, 1, 1)
        self.timeEditStartSunday = QTimeEdit(self.scheduleForm)
        sizePolicy2.setHeightForWidth(self.timeEditStartSunday.sizePolicy().hasHeightForWidth())
        self.timeEditStartSunday.setSizePolicy(sizePolicy2)
        self.timeEditStartSunday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartSunday, 1, 1, 1, 1)
        self.checkBoxWednesday = QCheckBox("Wednesday: ")
        sizePolicy3.setHeightForWidth(self.checkBoxWednesday.sizePolicy().hasHeightForWidth())
        self.checkBoxWednesday.setSizePolicy(sizePolicy3)
        self.scheduleFormLayout.addWidget(self.checkBoxWednesday, 4, 0, 1, 1)
        self.timeEditEndTuesday = QTimeEdit(self.scheduleForm)
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
        sizePolicy2.setHeightForWidth(self.timeEditEndFriday.sizePolicy().hasHeightForWidth())
        self.timeEditEndFriday.setSizePolicy(sizePolicy2)
        self.timeEditEndFriday.setTime(QTime(17, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditEndFriday, 6, 3, 1, 1)
        self.timeEditStartFriday = QTimeEdit(self.scheduleForm)
        sizePolicy2.setHeightForWidth(self.timeEditStartFriday.sizePolicy().hasHeightForWidth())
        self.timeEditStartFriday.setSizePolicy(sizePolicy2)
        self.timeEditStartFriday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartFriday, 6, 1, 1, 1)
        self.timeEditStartSaturday = QTimeEdit(self.scheduleForm)
        sizePolicy2.setHeightForWidth(self.timeEditStartSaturday.sizePolicy().hasHeightForWidth())
        self.timeEditStartSaturday.setSizePolicy(sizePolicy2)
        self.timeEditStartSaturday.setTime(QTime(8, 0, 0))
        self.scheduleFormLayout.addWidget(self.timeEditStartSaturday, 7, 1, 1, 1)
        self.scheduleLayout.addWidget(self.scheduleForm)
        self.addUserLayout.addWidget(self.scheduleFrame)



        self.faceEncFrame = QFrame(addUserWidget)
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(1)
        sizePolicy5.setHeightForWidth(self.faceEncFrame.sizePolicy().hasHeightForWidth())
        self.faceEncFrame.setSizePolicy(sizePolicy5)
        self.faceEncLayout = QHBoxLayout(self.faceEncFrame)
        self.faceEncLayout.setSpacing(0)
        self.faceEncLayout.setContentsMargins(0, 0, 0, 0)
        self.pictureframe = QFrame(self.faceEncFrame)
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
        sizePolicy4.setHeightForWidth(self.photoFaceEncFrame.sizePolicy().hasHeightForWidth())
        self.photoFaceEncFrame.setSizePolicy(sizePolicy4)
        self.photoFaceEncLayout = QVBoxLayout(self.photoFaceEncFrame)
        self.photoFaceEncLayout.setContentsMargins(0, 0, 0, 0)
        self.faceEncFrameLabel = QLabel("Face Encoding: ")
        self.faceEncFrameLabel.setStyleSheet(u"font: 75 24pt \"Garamond\";")
        self.photoFaceEncLayout.addWidget(self.faceEncFrameLabel)
        self.photoFaceEncForm = QFrame(self.photoFaceEncFrame)
        self.photoFaceEncForm.setStyleSheet(u"font: 75 16pt \"Garamond\";")
        self.photoFaceEncFormLayout = QFormLayout(self.photoFaceEncForm)
        self.photoFaceEncFormLayout.setHorizontalSpacing(10)
        self.photoFaceEncFormLayout.setVerticalSpacing(10)
        self.photoFaceEncFormLayout.setContentsMargins(10, 10, 10, 10)
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
        for timeEdit in [self.timeEditStartMonday, self.timeEditEndMonday,
                         self.timeEditStartTuesday, self.timeEditEndTuesday,
                         self.timeEditStartWednesday, self.timeEditEndWednesday,
                         self.timeEditStartThursday, self.timeEditEndThursday,
                         self.timeEditStartFriday, self.timeEditEndFriday,
                         self.timeEditStartSaturday, self.timeEditEndSaturday,
                         self.timeEditStartSunday, self.timeEditEndSunday,
                         ]:
            if 'Start' in timeEdit.objectName():
                timeEdit.setTime(defaultStartTime)
            else:
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
        button.setStyleSheet(u"font: 75 24pt \"Garamond\";")
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
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
