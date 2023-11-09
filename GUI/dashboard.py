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
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem, QImage, QPalette, QColor, QBrush
from PyQt5.uic.properties import QtWidgets
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
tittleFontSize = "36px"
subheaderFontSize = "24px"
bodyFontSize = "18px"
bodySecondaryFontSize = "16px"
buttonFontSize = "16px"
buttonLabelSize = "14px"
captionsFontSize = "12px"
dataTablesFontSize = "14px"
toolTipsFontSize = "16px"



primaryColor = "rgb(129, 117, 102)"
secondaryColor = "rgb(250, 250, 232)"
backgroundColor = "rgb(250, 245, 232)"
backgroundColorTransparent = "background-color: transparent;"
textColor = "rgb(0, 0, 0)"
textColorSecondary = "rgb(100, 100, 100)"
accentColor1 = "rgb(200, 200, 200)"
accentColor2 = "rgb(100, 100, 100)"
interactiveElements1 = "rgb(220, 220, 220)"
interactiveElements2 = "rgb(190, 190, 190)"

dataVisualizations = ""
bordersLines = "rgb(0, 0, 0)"
shadowsHighlights = "rgba(0, 0, 0, 0.5)"
fieldBackgroundColor = "rgb(255, 255, 255)"
placeholderColor = "rgb(200, 200, 200)"

buttonBackgroundColor = "rgb(255, 255, 255)"

graph_background_color = (250, 245, 232)
graph_font_color = (0, 0, 0)
graph_bar_color = (255, 255, 255)

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
        self.sideBar.setStyleSheet(f"background-color: {primaryColor};")
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
        self.mainWindow.setStyleSheet(f"background-color: {backgroundColor};")
        self.mainWindow.setFrameShape(QFrame.StyledPanel)
        self.mainWindow.setFrameShadow(QFrame.Raised)

        self.userHeaderContainer = QWidget(self.mainWindow)
        self.userHeaderContainer.setObjectName("userHeaderContainer")
        self.userHeaderUi = Ui_userHeaderWidget()
        self.userHeaderUi.setupUi(self.userHeaderContainer)

        self.displayContainer = QWidget(self.mainWindow)
        self.displayContainer.setObjectName("displayContainer")
        self.displayContainer.setStyleSheet(backgroundColorTransparent)
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

        logoWidget.setStyleSheet(backgroundColorTransparent)

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

        self.logoLabel = QLabel("LocUST")
        self.logoLabel.setObjectName("logoLabel")
        self.logoLabel.setStyleSheet(f"font: 75 {tittleFontSize} '{font}'; color:{textColor};" )

        self.logoLayout.addWidget(self.logoLabel)

class Ui_navigationWidget(object):

    def setupUi(self, navigationWidget):
        if not navigationWidget.objectName():
            navigationWidget.setObjectName("navigationWidget")
        navigationWidget.setStyleSheet(backgroundColorTransparent)

        self.navigationLayout = QVBoxLayout(navigationWidget)
        self.navigationLayout.setSpacing(0)
        self.navigationLayout.setContentsMargins(0, 5, 0, 5)

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
        button.setText("  " + text)
        button.setIcon(QIcon(f"buttonIcons/{iconPath}"))
        button.setIconSize(QSize(20, 20))

        # Stylesheet with hover and pressed states
        button.setStyleSheet(f"""
                    QPushButton {{
                        color: {textColor}; 
                        font: 75 {buttonFontSize} '{font}';
                        padding-left: 30px; /* Size of the icon plus desired spacing */
                        text-align: left;
                        border: none; /* Remove border */
                        background-color: transparent;
                    }}
                    QPushButton:hover {{
                        background-color: {interactiveElements1}; /* Lighter shade for hover */
                    }}
                    QPushButton:pressed {{
                        background-color: {interactiveElements2}; /* Even lighter for pressed */
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
        label.setStyleSheet(f"color: {textColor}; font: 75 {buttonLabelSize} '{font}'; padding-left: 10px;")
        label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return label

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
                background-color: {accentColor1};  /* Your desired background color for the normal state */
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
        self.employeeName.setStyleSheet(f"font: 75 {bodyFontSize} '{font}'; color:{textColor};")
        self.userHeaderLayout.addWidget(self.employeeName)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)
        self.employeeName.setGraphicsEffect(opacity_effect)

class Ui_dashboardWidget(object):
    def setupUi(self, dashboardWidget):
        self.containerStylesheet = f"""
            QFrame {{
                background-color: {backgroundColor};
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

        if not dashboardWidget.objectName():
            dashboardWidget.setObjectName(u"dashboardWidget")
        dashboardWidget.setStyleSheet(backgroundColorTransparent)
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

        self.iunContainer.setStyleSheet(self.containerStylesheet)
        self.iunContainer.setFrameShape(QFrame.StyledPanel)
        self.iunContainer.setFrameShadow(QFrame.Raised)
        self.iunLayout = QVBoxLayout(self.iunContainer)
        self.iunLayout.setSpacing(10)
        self.iunLayout.setObjectName(u"iunLayout")
        self.iunLayout.setContentsMargins(10, 10, 10, 10)

        self.iULabel = QLabel("Users")
        self.iULabel.setObjectName(u"iULabel")
        self.iULabel.setStyleSheet(self.font1)
        self.iULabel.setTextFormat(Qt.PlainText)
        self.iunLayout.addWidget(self.iULabel, 0, Qt.AlignHCenter)


        self.iUNumber = QLabel("0")
        self.iUNumber.setObjectName(u"iUNumber")
        self.iUNumber.setStyleSheet(self.font2)
        self.iUNumber.setTextFormat(Qt.PlainText)
        self.iunLayout.addWidget(self.iUNumber, 0, Qt.AlignHCenter)
        self.entLayout.addWidget(self.iunContainer)


        self.techNumberContainer = QFrame(self.entWidget)
        self.techNumberContainer.setObjectName(u"techNumberContainer")
        self.techNumberContainer.setStyleSheet(self.containerStylesheet)
        self.techNumberContainer.setFrameShape(QFrame.StyledPanel)
        self.techNumberContainer.setFrameShadow(QFrame.Raised)
        self.techNumberLayout = QVBoxLayout(self.techNumberContainer)
        self.techNumberLayout.setSpacing(10)
        self.techNumberLayout.setObjectName(u"techNumberLayout")
        self.techNumberLayout.setContentsMargins(10, 10, 10, 10)

        self.techLabel = QLabel("Desk Technicians")
        self.techLabel.setObjectName(u"techLabel")
        self.techLabel.setStyleSheet(self.font1)
        self.techLabel.setTextFormat(Qt.PlainText)

        self.techNumberLayout.addWidget(self.techLabel, 0, Qt.AlignHCenter)

        self.techNumber = QLabel("0")
        self.techNumber.setObjectName(u"techNumber")
        self.techNumber.setStyleSheet(self.font2)
        self.techNumber.setTextFormat(Qt.PlainText)

        self.techNumberLayout.addWidget(self.techNumber, 0, Qt.AlignHCenter)


        self.entLayout.addWidget(self.techNumberContainer)

        self.empNumberContainer = QFrame(self.entWidget)
        self.empNumberContainer.setObjectName(u"empNumberContainer")
        self.empNumberContainer.setStyleSheet(self.containerStylesheet)
        self.empNumberContainer.setFrameShape(QFrame.StyledPanel)
        self.empNumberContainer.setFrameShadow(QFrame.Raised)
        self.empNumberLayout = QVBoxLayout(self.empNumberContainer)
        self.empNumberLayout.setSpacing(10)
        self.empNumberLayout.setObjectName(u"empNumberLayout")
        self.empNumberLayout.setContentsMargins(10, 10, 10, 10)
        self.mangerLabel = QLabel("Security Managers")
        self.mangerLabel.setObjectName(u"mangerLabel")
        self.mangerLabel.setStyleSheet(self.font1)
        self.mangerLabel.setTextFormat(Qt.PlainText)

        self.empNumberLayout.addWidget(self.mangerLabel, 0, Qt.AlignHCenter)

        self.managerNum = QLabel("0")
        self.managerNum.setObjectName(u"managerNum")
        self.managerNum.setStyleSheet(self.font2)
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
        self.canScanTodayContainer.setStyleSheet(self.containerStylesheet)
        self.canScanTodayContainer.setFrameShape(QFrame.StyledPanel)
        self.canScanTodayContainer.setFrameShadow(QFrame.Raised)
        self.canScanTodayLayout = QVBoxLayout(self.canScanTodayContainer)
        self.canScanTodayLayout.setSpacing(10)
        self.canScanTodayLayout.setObjectName(u"canScanTodayLayout")
        self.canScanTodayLayout.setContentsMargins(10, 10, 10, 10)
        self.userScheduleTodayLabel = QLabel("Scheduled For Today")
        self.userScheduleTodayLabel.setObjectName(u"userScheduleTodayLabel")
        self.userScheduleTodayLabel.setStyleSheet(self.font1)
        self.userScheduleTodayLabel.setTextFormat(Qt.PlainText)

        self.canScanTodayLayout.addWidget(self.userScheduleTodayLabel, 0, Qt.AlignHCenter)

        self.userScheduleTodayNumber = QLabel("0")
        self.userScheduleTodayNumber.setObjectName(u"userScheduleTodayNumber")
        self.userScheduleTodayNumber.setStyleSheet(self.font2)
        self.userScheduleTodayNumber.setTextFormat(Qt.PlainText)

        self.canScanTodayLayout.addWidget(self.userScheduleTodayNumber, 0, Qt.AlignHCenter)


        self.scanInfoLayout.addWidget(self.canScanTodayContainer)

        self.scansTodayWidget = QFrame(self.scanInfoWidget)
        self.scansTodayWidget.setObjectName(u"scansTodayWidget")
        self.scansTodayWidget.setStyleSheet(self.containerStylesheet)
        self.scansTodayWidget.setFrameShape(QFrame.StyledPanel)
        self.scansTodayWidget.setFrameShadow(QFrame.Raised)
        self.scansTodayLayout = QVBoxLayout(self.scansTodayWidget)
        self.scansTodayLayout.setSpacing(10)
        self.scansTodayLayout.setObjectName(u"scansTodayLayout")
        self.scansTodayLayout.setContentsMargins(10, 10, 10, 10)
        self.scansTodayLabel = QLabel("Scans Today")
        self.scansTodayLabel.setObjectName(u"scansTodayLabel")
        self.scansTodayLabel.setStyleSheet(self.font1)
        self.scansTodayLabel.setTextFormat(Qt.PlainText)

        self.scansTodayLayout.addWidget(self.scansTodayLabel, 0, Qt.AlignHCenter)

        self.scansTodayNumber = QLabel("0")
        self.scansTodayNumber.setObjectName(u"scansTodayNumber")
        self.scansTodayNumber.setStyleSheet(self.font2)

        self.scansTodayLayout.addWidget(self.scansTodayNumber, 0, Qt.AlignHCenter)


        self.scanInfoLayout.addWidget(self.scansTodayWidget)

        self.scansThisWeekContainer = QFrame(self.scanInfoWidget)
        self.scansThisWeekContainer.setObjectName(u"scansThisWeekContainer")
        self.scansThisWeekContainer.setStyleSheet(self.containerStylesheet)
        self.scansThisWeekContainer.setFrameShape(QFrame.StyledPanel)
        self.scansThisWeekContainer.setFrameShadow(QFrame.Raised)
        self.scansThisWeekLayout = QVBoxLayout(self.scansThisWeekContainer)
        self.scansThisWeekLayout.setSpacing(10)
        self.scansThisWeekLayout.setObjectName(u"scansThisWeekLayout")
        self.scansThisWeekLayout.setContentsMargins(10, 10, 10, 10)
        self.scansThisWeekLabel = QLabel("Scans This Week")
        self.scansThisWeekLabel.setObjectName(u"scansThisWeekLabel")
        self.scansThisWeekLabel.setStyleSheet(self.font1)
        self.scansThisWeekLabel.setTextFormat(Qt.PlainText)

        self.scansThisWeekLayout.addWidget(self.scansThisWeekLabel, 0, Qt.AlignHCenter)

        self.scansThisWeekNumber = QLabel("0")
        self.scansThisWeekNumber.setObjectName(u"scansThisWeekNumber")
        self.scansThisWeekNumber.setStyleSheet(self.font2)
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
        self.dateTimeWidget.setStyleSheet(self.containerStylesheet)
        self.dateTimeWidget.setFrameShape(QFrame.StyledPanel)
        self.dateTimeWidget.setFrameShadow(QFrame.Raised)
        self.dateTimeLayout = QVBoxLayout(self.dateTimeWidget)
        self.dateTimeLayout.setSpacing(0)
        self.dateTimeLayout.setObjectName(u"dateTimeLayout")
        self.dateTimeLayout.setContentsMargins(10, 10, 10, 10)

        self.dateLabel = QLabel(self.dateTimeWidget)
        self.dateLabel.setObjectName(u"dateLabel")
        self.dateLabel.setStyleSheet(self.font2)
        self.dateLabel.setTextFormat(Qt.PlainText)
        self.update_date_label()
        self.dateTimeLayout.addWidget(self.dateLabel)


        self.timeLabel = QLabel(self.dateTimeWidget)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setStyleSheet(self.font1)
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
        self.ticketsNumContainer.setStyleSheet(self.containerStylesheet)
        self.ticketsNumContainer.setFrameShape(QFrame.StyledPanel)
        self.ticketsNumContainer.setFrameShadow(QFrame.Raised)
        self.ticketNumberLayout = QVBoxLayout(self.ticketsNumContainer)
        self.ticketNumberLayout.setSpacing(10)
        self.ticketNumberLayout.setObjectName(u"ticketNumberLayout")
        self.ticketNumberLayout.setContentsMargins(10, 10, 10, 10)
        self.currentTicketLabel = QLabel(self.ticketsNumContainer)
        self.currentTicketLabel.setObjectName(u"currentTicketLabel")
        self.currentTicketLabel.setStyleSheet(self.font1)
        self.currentTicketLabel.setTextFormat(Qt.PlainText)
        self.currentTicketLabel.setText("Current Tickets")
        self.ticketNumberLayout.addWidget(self.currentTicketLabel, 0, Qt.AlignHCenter)

        self.currentNumOfTickets = QLabel(self.ticketsNumContainer)
        self.currentNumOfTickets.setObjectName(u"currentNumOfTickets")
        self.currentNumOfTickets.setStyleSheet(self.font2)
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

        self.recentScansframe = QFrame(self.rightFrame)
        self.recentScansframe.setStyleSheet(self.containerStylesheet)
        self.recentScansframeLayout = QVBoxLayout(self.recentScansframe)
        self.rightLayout.addWidget(self.recentScansframe)



        self.recentScansHeader = QFrame(self.rightFrame)
        self.recentScansHeader.setStyleSheet("background-color: transparent;"
                                   "border: none;"
                                   "border-radius: 20px;")
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


        self.rightFrame.update()


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
        recentScans.setStyleSheet("background-color: transparent;"
                                   "border: none;"
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
        userID.setStyleSheet(f"font: 75 {bodySecondaryFontSize} '{font}'; color:{textColor};")
        userID.setText(user_id_text)
        userInfoLayout.addWidget(userID)

        # User Name Label
        userName = QLabel(userInfo)
        userName.setObjectName("userName")
        userName.setStyleSheet(f"font: 75 {bodyFontSize} '{font}'; color:{textColor};")
        userName.setText(user_name_text)
        userInfoLayout.addWidget(userName)

        # Scan Date Time Label
        scanDateTime = QLabel(userInfo)
        scanDateTime.setObjectName("scanDateTime")
        scanDateTime.setStyleSheet(f"font: 75 {bodySecondaryFontSize} '{font}'; color:{textColorSecondary};")
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

        self.table_stylesheet = """
            QTableView {
                border: 1px solid #d4d4d4;
                gridline-color: #d4d4d4;
                selection-background-color: #c2c2c2;
                selection-color: black;
                background-color: white;
                color: black;
            }

            QTableView::item {
                padding: 5px;
                border-color: transparent;
                gridline-color: #d4d4d4;
            }

            QTableView::item:selected {
                background: #e7e7e7;
                color: black;
            }
            QTableView QLineEdit {
        color: black; /* Color of the text while editing */
    }
    

            QTableView::item:hover {
                background-color: #f5f5f5;
            }

            QTableView QTableCornerButton::section {
                background: #e6e6e6;
                border: 1px solid #d4d4d4;
            }

            QHeaderView::section {
                background-color: #f4f4f4;
                padding: 4px;
                border: 1px solid #d4d4d4;
                font-size: 10pt;
                font-weight: bold;
                color: black;
            }

            QHeaderView::section:checked {
                background-color: #d0d0d0;
            }

            QHeaderView::section:horizontal {
                border-top: none;
            }

            QHeaderView::section:vertical {
                border-left: none;
            }
        """
        self.tabStyleSheet = """
            QTabWidget::tab-bar {
                alignment: left;
                background-color: black;
            }

            QTabWidget::pane {
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                background: white;
                color:black;
            }

            QTabBar::tab {
                background: white;
                color: black;
                border: 0px;
                margin: 5px;
                padding: 5px;
                
                
                height: 24px;
               
                border-top-right-radius: 10px; 
                border-bottom-right-radius: 10px;
                border-bottom-left-radius: 10px;
                border-top-left-radius: 10px;
            }



            QTabBar::tab:selected {
                background: black;
                color: white;
            }

            QTabBar::tab:hover {
                background: lightgray;
            }
        """

        self.buttonStyleSheet = """QPushButton {
    background-color: #5CACEE; /* Light blue background */
    color: white; /* White text */
    border-radius: 4px; /* Rounded corners */
    padding: 5px 10px; /* Top and bottom padding of 5px, left and right padding of 10px */
    border: none; /* No border */
    outline: none; /* Remove focus outline */
}

QPushButton:hover {
    background-color: #1E90FF; /* Slightly darker blue on hover */
}

QPushButton:pressed {
    background-color: #1874CD; /* Even darker blue when pressed */
}"""

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

        self.calendar_stylesheet = """
                                        QCalendarWidget {
                                background-color: #f9f9f9;  /* Background color of the entire calendar */
                                border: 3px solid #d9a741;  /* Border color of the entire calendar */
                                border-radius: 4px;         /* Rounded corners for the calendar */
                            }

                            QCalendarWidget QWidget { 
                                color: black;             /* change day numbers */
                            }

                            QCalendarWidget QTableView { 
                                border: 2px solid #d9a741;  /* Border around the table view (contains the days) */
                                gridline-color: #d0d0d0;   /* Color of the grid separating the days */
                                background-color: white; /* Background color of the entire table view */
                            }

                            QCalendarWidget QTableView QHeaderView::section { 
                                background-color: #e9cf8d;  /* Background color of the headers (Mon, Tue, ...) */
                                padding: 6px;               /* Padding for the headers */
                                border: 1px solid #d9a741;  /* Border color for the headers */
                                font-size: 12pt;            /* Font size of the headers */
                                font-weight: bold;          /* Font weight of the headers */
                                color: #000;                /* Text color of the headers */
                            }

                            QCalendarWidget QToolButton { 
                                icon-size: 24px;            /* Size of the navigation icons (previous and next month) */
                                border: none;               /* Remove the border from tool buttons */
                                background-color: transparent;  /* Make tool buttons' background transparent */
                                color: black;             /* Color of the navigation icons */
                            }

                            QCalendarWidget QToolButton:hover { 
                                background-color: #f5e7bc;  /* Background color when hovering over navigation buttons */
                            }

                            QCalendarWidget QMenu { 
                                border: 1px solid #d9a741;  /* Border around the drop-down menu (from the small arrow button) */
                            }

                            QCalendarWidget QMenu::item { 
                                padding: 4px 24px 4px 24px; /* Padding around the items inside the drop-down menu */
                                background-color: #f9f9f9; /* Background color of the menu items */
                                color: black;            /* Text color of the menu items */
                            }

                            QCalendarWidget QMenu::item:selected { 
                                background-color: #d9a741;  /* Background color when an item inside the menu is selected */
                                color: #000;                /* Text color of the selected item inside the menu */
                            }

                            QCalendarWidget QAbstractItemView {
                                selection-background-color: #f5e7bc; /* Background color of the selected date */
                                selection-color: #000;              /* Text color of the selected date */
                            }

                            QCalendarWidget QLabel { 
                                font-size: 28pt;            /* Font size of the large month and year label */
                                color: black;             /* Color of the large month and year label */
                                font-weight: bold;          /* Font weight of the large month and year label */
                            }

                            QCalendarWidget #qt_calendar_navigationbar { 
                                background-color: #f9f9f9;  /* Background color of the navigation bar (contains the month, year, and navigation buttons) */
                                border: 2px solid #d9a741;  /* Border at the bottom of the navigation bar */
                                font-size: 18pt;            /* Font size of the navigation bar */
                            }
                """

        self.table_stylesheet = """
    QTableView {
        border: 1px solid #b6b6b6;
        gridline-color: #cccccc;
        selection-background-color: #6ea1f1;
        selection-color: white;
        background-color: white;
        color: black;
    }

    QTableView::item {
        padding: 5px;
        border-color: transparent;
        gridline-color: #cccccc;
    }

    QTableView::item:selected {
        background: #6ea1f1;
        color: white;
    }

    QTableView::item:hover {
        background-color: #eaeaea;
    }

    QHeaderView::section {
        background-color: #f5f5f5;
        padding: 4px;
        border: 1px solid #b6b6b6;
        font-size: 10pt;
        font-weight: bold;
        color: black;
    }

    QHeaderView::section:horizontal {
        border-top: none;
    }

    QHeaderView::section:vertical {
        border-left: none;
    }

    QHeaderView::section:checked {
        background-color: #d0d0d0;
    }
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
        format.setForeground(QBrush(QColor("#d9a741"), Qt.SolidPattern))
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
            print(f"Processing schedule string: {schedule_str}")  # Debug print

            # Split each schedule string into name and times
            if ': ' in schedule_str:
                name, times = schedule_str.split(': ', 1)
                # Look for a hyphen with optional whitespace around it
                if ' - ' in times or '-' in times:
                    # Remove any potential whitespace around the hyphen before splitting
                    times = times.replace(' - ', '-').replace('–', '-')  # Also replace en-dash if present
                    start_time, end_time = times.split('-')
                else:
                    print(f"Start and end times not properly formatted in string: {times}")  # Debug print
                    start_time = 'N/A'
                    end_time = 'N/A'
            else:
                print(f"No times found in schedule string: {schedule_str}")  # Debug print
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
        if not ticketsWidget.objectName():
            ticketsWidget.setObjectName(u"ticketsWidget")
        ticketsWidget.setStyleSheet("""
                    QWidget#ticketsWidget {
                        background-color: #F5F5F5;
                    }
                    QFrame#leftWidget, QFrame#rightWidget {
                        background-color: #FAF5E8;
                        border: 2px solid #817562;
                        border-radius: 20px;
                    }
                    QLabel#ticketNameLabel, QLabel#ticketLabel {
                        font: 700 18pt "Garamond";
                        background-color: transparent;
                        border: none;
                        border-radius: 20px;
                        color: #333333;
                    }
                    QTextEdit#ticketTextEdit {
                        background-color: white;
                        border: 2px solid #DDD;
                        border-radius: 20px;
                        font: 700 16pt "Garamond";
                        color: #333333;
                        padding: 8px;
                    }
                    QPushButton#resolvedButton {
                        background-color: #CCF2F4;
                        border: 2px solid #30AAB0;
                        border-radius: 20px;
                        font: 700 24pt "Garamond";
                        color: #2F4F4F;
                        padding: 8px;
                        margin-top: 10px;
                    }
                    QPushButton#ticketButton {
                        font: 700 16pt "Garamond";
                        background-color: #F8F8F8;
                        border: 2px solid #DDD;
                        border-radius: 20px;
                        color: #555;
                        padding: 8px;
                        margin-bottom: 10px;
                    }
                    QPushButton#ticketButton:hover {
                        background-color: #E8E8E8;
                    }
                    QPushButton#ticketButton:pressed {
                        background-color: #D0D0D0;
                    }
                """)
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

    def create_ticket_button(self, text, font_family=f"{font}", font_size=16, font_weight=75):
        ticket_button = QPushButton()
        ticket_button.setObjectName(u"ticketButton")
        ticket_button.setText(text)
        #style = f"font: {font_weight} {font_size}pt \"{font_family}\";"
        #ticket_button.setStyleSheet(style)
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
                        background-color: {backgroundColor};
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
    }}"""

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
        background-color: {buttonBackgroundColor};
        color: {textColor};
        border-style: outset;
        border-width: 2px;
        border-radius: 10px;
        border-color: {bordersLines};
        font: bold 14px;
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
