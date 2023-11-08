import csv
import inspect
import json
import os
import sys
import cv2
from PyQt5.QtCore import QTimer, Qt, QDateTime, QDate, QTime, pyqtSignal, QRectF, pyqtProperty, QPropertyAnimation
from PyQt5.QtGui import QImage, QPixmap, QPainter, QLinearGradient, QColor, QPen, QFont, QBrush, QTransform
from PyQt5.QtMultimedia import QCamera, QCameraImageCapture
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, \
    QPushButton, QSpacerItem, QSizePolicy, QFrame, QDesktopWidget, QDateTimeEdit, QCalendarWidget, QTableView, \
    QToolButton, QTableWidget, QTableWidgetItem, QGroupBox, QSpinBox, QComboBox, QDialogButtonBox, QFormLayout, QLayout, \
    QMessageBox, QFileDialog, QTextEdit, QTabBar, QStackedWidget, QGridLayout, QTabWidget
import dlib
import pickle
from PyQt5.uic.properties import QtWidgets, QtGui
import Entities.IndirectUser.User
import Entities.Employee.Employee
import shutil
import LoginWindow
import MainWindow
from Database.firebaseDatabase import database
import Entities.entitiesMain

"""
xLarge_font_size = '75px'
large_font_size = '60px'
medium_font_size = '30px'
small_font_size = '25px'
xSmall_font_size = '20px'

"""

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

xLarge_font_size = '75px'
large_font_size = '60px'
medium_font_size = '30px'
small_font_size = '25px'
xSmall_font_size = '20px'
tiny_font_size = "18px"


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


class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget { background-color: white; } 
            QLabel { font-size: 72pt; font-family: Copperplate; color: black; }
        """)

        mainLayout = QVBoxLayout(self)

        # Calculate window dimensions
        screen_geometry = QApplication.desktop().screenGeometry()
        window_width = screen_geometry.width()
        middle_window = window_width / 2

        def locustContainer():
            layout = QHBoxLayout()

            layout.setContentsMargins(0, 0, 0, 0)

            # Set up labels
            label = QLabel("L", self)
            image_label = QLabel(self)
            pixmap = QPixmap("Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")
            image_label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            image_label.setFixedSize(60, 60)
            label2 = QLabel("cUST", self)

            labels_size = (label.sizeHint().width() + image_label.sizeHint().width() + label2.sizeHint().width()) / 2
            layout.addSpacing(int(middle_window) - int(labels_size))
            layout.addWidget(label)
            layout.addWidget(image_label)
            layout.addWidget(label2)
            layout.addStretch()
            return layout

        mainLayout.addSpacing(10)
        mainLayout.addLayout(locustContainer())

        # Add other widgets to the main layout
        fadingLine = FadingLine()
        mainLayout.addWidget(fadingLine)
        mainLayout.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        mainLayout.addSpacing(20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(Qt.white)
        painter.drawRect(self.rect())


class ManagerWindow(QMainWindow):
    def __init__(self, employee=None):
        super().__init__()
        self.employee = employee
        self.showMaximized()
        self.showFullScreen()

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: rgb(230, 230, 230);")

        headerWidget = HeaderWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)

        central_layout.addWidget(headerWidget)
        central_layout.setAlignment(Qt.AlignTop)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Define displayLayout here
        self.displayWidget = QWidget()
        self.displayWidget.setStyleSheet("background-color: white;"
                                         "border-radius: 10px;")
        self.displayWidget.setContentsMargins(0, 0, 0, 0)
        self.displayLayout = QVBoxLayout(self.displayWidget)

        mainLayout = QHBoxLayout()

        central_layout.addLayout(mainLayout)

        mainLayout.addWidget(self.leftWidgetContainer(), stretch=5)
        mainLayout.addWidget(self.rightWidgetContainer(), stretch=16)

    def leftWidgetContainer(self):
        widget = QWidget()
        widget.setStyleSheet("border-radius: 10px;"
                             "background: transparent;")

        layout = QVBoxLayout(widget)
        layout.setSpacing(5)

        def header():
            headerWidget = QWidget()
            headerLayout = QVBoxLayout(headerWidget)
            width = headerWidget.sizeHint().width()

            headerWidget.setObjectName("headerWidget")  # Add an object name for specificity
            headerWidget.setStyleSheet("""
                QWidget{background-color:white;
                }
                QWidget#headerWidget {  
                    border: 0px solid black;
                    border-radius: 10px;
                }
            """)
            dt = DateTime()
            line = FadingLine()
            headerLayout.addWidget(dt)
            headerLayout.addWidget(line)
            return headerWidget

        def tab():
            def main():
                widget = QWidget()
                layout = QVBoxLayout(widget)

                faceRecButton = CustomButton("Facial Recognition")
                faceRecButton.clicked.connect(self.faceRec)
                layout.addWidget(faceRecButton)

                addUserButton = CustomButton("Add User")
                addUserButton.clicked.connect(self.add_user)
                layout.addWidget(addUserButton)

                layout.addStretch()
                logoutButton = CustomButton("Logout")
                logoutButton.clicked.connect(self.logout)
                layout.addWidget(logoutButton)

                return widget

            def logs():
                logsWidget = QWidget()
                logsWidget.setStyleSheet("background-color: white")
                logsWidget.setContentsMargins(0, 0, 10, 0)

                logsLayout = QVBoxLayout(logsWidget)
                logsLayout.setAlignment(Qt.AlignTop)

                userButton = CustomButton("Indirect Users")
                userButton.clicked.connect(self.on_user_button_clicked)

                employeeButton = CustomButton("Employee")
                employeeButton.clicked.connect(self.on_employee_button_clicked)

                logsButton = CustomButton("Logs")
                logsButton.clicked.connect(self.on_logs_button_clicked)

                logsLayout.addWidget(userButton)
                logsLayout.addWidget(employeeButton)
                logsLayout.addWidget(logsButton)

                logsLayout.addStretch()
                logoutButton = CustomButton("Logout")
                logoutButton.clicked.connect(self.logout)
                logsLayout.addWidget(logoutButton)
                return logsWidget

            def tickets():
                widget = QWidget()
                layout = QVBoxLayout(widget)

                ticketWidget = Tickets(self.displayLayout)
                layout.addWidget(ticketWidget)
                self.num_tickets = ticketWidget.numOfTickets()

                layout.addStretch()
                logoutButton = CustomButton("Logout")
                logoutButton.clicked.connect(self.logout)
                layout.addWidget(logoutButton)
                return widget

            def calender():
                widget = QWidget()
                self.calLayout = QVBoxLayout(widget)
                calender_ = CustomCalendar()
                self.calLayout.addWidget(calender_)
                self.calLayout.addStretch()

                calender_.clicked[QDate].connect(self.on_day_clicked)

                current_date = QDate.currentDate()

                getSchedules = Entities.entitiesMain.getSchedule(current_date.toString("dddd"))
                print(getSchedules)

                self.labels = []
                for schedule in getSchedules:
                    self.label = QLabel(schedule)
                    self.label.setStyleSheet("color:black;")

                    self.labels.append(self.label)
                    self.calLayout.addWidget(self.label)

                self.calLayout.addStretch()

                return widget

            tabWidget = QTabWidget()
            customTabBar = CustomTabBar()
            tabWidget.setTabBar(customTabBar)

            tabWidget.setStyleSheet("""
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
                            }

                            QTabBar::tab {
                                background: white;
                                color: black;
                                border: 0px;
                                margin-top: 5px;
                                margin-bottom: 5px;
                                height: 100px;
                                width: 25px;
                                border-top-right-radius: 10px; 
                                border-bottom-right-radius: 10px;
                            }



                            QTabBar::tab:selected {
                                background: black;
                                color: white;
                            }

                            QTabBar::tab:hover {
                                background: lightgray;
                            }
                        """)

            tabWidget.setTabPosition(QTabWidget.East)

            # Setup your tabs here
            main_tab = main()
            logs_tab = logs()
            tickets_tab = tickets()
            calender_tab = calender()

            # Add tabs to your tab widget
            main_index = tabWidget.addTab(main_tab, 'Main')
            logs_index = tabWidget.addTab(logs_tab, 'Logs')
            tickets_index = tabWidget.addTab(tickets_tab, 'Ticket')
            calender_index = tabWidget.addTab(calender_tab, "Calender")

            customTabBar.setNotification(tickets_index, self.num_tickets)

            return tabWidget

        layout.addWidget(header(), stretch=2)
        layout.addWidget(tab(), stretch=10)

        return widget

    def rightWidgetContainer(self):
        widget = QWidget()
        widget.setStyleSheet("background-color:transparent;"
                             "border-radius: 10px;")

        layout = QVBoxLayout(widget)
        layout.setSpacing(5)

        def header():
            headerWidget = QWidget()

            headerLayout = QVBoxLayout(headerWidget)
            width = headerWidget.sizeHint().width()

            headerWidget.setObjectName("headerWidget")  # Add an object name for specificity
            headerWidget.setStyleSheet("""
                QWidget{background-color:transparent;
                }
                QWidget#headerWidget {  
                    border: 0px solid black;
                    border-radius: 10px;
                }
            """)
            dt = DateTime()
            line = FadingLine()
            # headerLayout.addWidget(dt)
            # headerLayout.addWidget(line)
            return headerWidget

        def display():
            displayWidget = QWidget()
            displayWidget.setContentsMargins(0, 0, 0, 0)
            displayLayout = QVBoxLayout(displayWidget)
            displayLayout.addWidget(self.displayWidget)
            return displayWidget

        layout.addWidget(header(), stretch=1)

        layout.addWidget(display(), stretch=10)
        layout.addWidget(header(), stretch=1)
        layout.addStretch()

        return widget

    def clearLayout(self):
        self.current_displayed_type = None
        for i in reversed(range(self.displayLayout.count())):
            widget = self.displayLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def on_user_button_clicked(self):
        self.clearLayout()
        self.tableWidget = TableWidget(context="Indirect User Button", parent=self)
        self.displayLayout.addWidget(self.tableWidget)
        self.tableWidget.removeRequested.connect(self.removeUserWidget)

    def on_employee_button_clicked(self):
        self.clearLayout()
        self.tableWidget = TableWidget(context="Employee Button", parent=self)
        self.displayLayout.addWidget(self.tableWidget)
        self.tableWidget.removeRequested.connect(self.removeUserWidget)

    def on_logs_button_clicked(self):
        self.clearLayout()
        self.tableWidget = TableWidget(context="Logs", parent=self)
        self.displayLayout.addWidget(self.tableWidget)
        self.tableWidget.removeRequested.connect(self.removeUserWidget)

    def faceRec(self):
        self.faceRecWindow = MainWindow.MainWindow()
        self.faceRecWindow.showFullScreen()
        self.close()  # Close the login window

    def add_user(self):
        self.clearLayout()
        self.userWidget = addUser(self)
        self.displayLayout.addWidget(self.userWidget)
        self.userWidget.removeRequested.connect(self.removeUserWidget)

    def removeUserWidget(self):
        self.userWidget.setParent(None)  # Detach the widget from the main window
        self.userWidget.deleteLater()

    def logout(self):
        self.loginWindow = LoginWindow.LoginWindow()
        self.loginWindow.showFullScreen()
        self.close()

    def on_day_clicked(self, date):

        day_of_the_week = date.toString('dddd')
        getSchedules = Entities.entitiesMain.getSchedule(day_of_the_week)

        for label in self.labels:
            self.calLayout.removeWidget(label)
            label.deleteLater()
        self.labels.clear()

        for schedule in getSchedules:
            self.label = QLabel(schedule)
            self.label.setStyleSheet("color:black;")
            self.labels.append(self.label)
            self.calLayout.addWidget(self.label)


class CustomButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.initUI()
        # self.setFixedWidth(int(leftWidgetWidth))

    def initUI(self):
        self.setStyleSheet("border: 1px solid #CCCCCC; padding: 10px; "
                           "background-color: #F5F5F5; border-radius: 5px; color: black;")

    def enterEvent(self, event):
        # When the mouse hovers over the label, change its color to indicate that it's clickable
        self.setStyleSheet("border: 1px solid #AAAAAA; padding: 10px; "
                           "background-color: #E0E0E0; border-radius: 5px; color: black;")

    def leaveEvent(self, event):
        # When the mouse leaves the label, revert its color
        self.setStyleSheet("border: 1px solid #CCCCCC; padding: 10px; "
                           "background-color: #F5F5F5; border-radius: 5px; color: black;")


class CustomCalendar(QCalendarWidget):
    def __init__(self, parent=None):
        super(CustomCalendar, self).__init__(parent)

        # Set fixed height and margins
        self.setFixedHeight(200)
        self.setContentsMargins(0, 0, 0, 0)
        self.setGridVisible(True)

        format = self.weekdayTextFormat(Qt.Saturday)
        format.setForeground(QBrush(QColor("#d9a741"), Qt.SolidPattern))
        self.setWeekdayTextFormat(Qt.Saturday, format)
        self.setWeekdayTextFormat(Qt.Sunday, format)

        # Set header format
        self.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)

        # Hide navigation buttons
        self.findChild(QToolButton, "qt_calendar_prevmonth").hide()
        self.findChild(QToolButton, "qt_calendar_nextmonth").hide()

        # Apply custom stylesheet
        calendar_stylesheet = """
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

        self.setStyleSheet(calendar_stylesheet)


class Schedule(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)


class Tickets(QWidget):
    def __init__(self, displayWidget, parent=None):
        super().__init__(parent)
        self.displayWidget = displayWidget
        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        class ClickableLabel(QLabel):
            def __init__(self, text, filepath, displayLayout, ticketLayout):
                super().__init__(text)
                self.filepath = filepath
                self.displayLayout = displayLayout
                self.ticketLayout = ticketLayout

                buttonH = int(50)
                self.setFixedHeight(buttonH)
                self.setStyleSheet(
                    "border: 1px solid #CCCCCC; padding: 0px; background-color: #F5F5F5; border-radius: 5px; color:black;"
                )

            def createButton(self, text, connect):
                button = QPushButton(text)
                button.setFixedSize(100, 40)
                button.setStyleSheet("background-color: black; color: black; border-radius: 20px; color:white")
                button.clicked.connect(connect)
                return button

            def enterEvent(self, event):
                # When the mouse hovers over the label, change its color
                self.setStyleSheet(
                    "border: 1px solid #AAAAAA; padding: 0px; background-color: #E0E0E0; border-radius: 5px; color:black;"
                )

            def leaveEvent(self, event):
                # Revert color when mouse leaves the label
                self.setStyleSheet(
                    "border: 1px solid #CCCCCC; padding: 0px; background-color: #F5F5F5; border-radius: 5px; color:black;"
                )

            def mousePressEvent(self, event):
                self.clearLayout()
                fileContentDisplay = QTextEdit()
                fileContentDisplay.setStyleSheet("color:black;")
                if event.button() == Qt.LeftButton:
                    with open(self.filepath, 'r') as file:
                        contents = file.read()
                        fileContentDisplay.setText(contents)
                        self.displayLayout.addWidget(fileContentDisplay)

                        buttonBox = QHBoxLayout()
                        resolvedButton = self.createButton("Resolved", self.resolveTicket)
                        buttonBox.addWidget(resolvedButton)
                        self.displayLayout.addWidget(resolvedButton)

            def clearLayout(self):
                self.current_displayed_type = None
                for i in reversed(range(self.displayLayout.count())):
                    widget = self.displayLayout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()

            def resolveTicket(self):
                try:
                    # 1. Delete the file
                    os.remove(self.filepath)

                    # 2. Clear the ticket (label) that represents this file
                    self.deleteLater()

                    # 3. Clear the displayed content and the resolved button
                    self.clearLayout()

                except Exception as e:
                    print(f"Error while resolving ticket: {e}")

            def clearTickets(self):
                # Clears the tickets (labels) from the ticketLayout
                for i in reversed(range(self.ticketLayout.count())):
                    widget = self.ticketLayout.itemAt(i).widget()
                    if widget is not None:
                        widget.deleteLater()

        def add_tickets_to_layout(directory, layout, displayLayout):
            try:
                # List all files in the directory
                files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

                # For each text file, create a label and add to the layout
                for file in files:
                    if file.endswith('.txt'):
                        label_text = os.path.splitext(file)[0]  # Gets the file name without extension
                        filepath = os.path.join(directory, file)  # Full path to the file
                        label = ClickableLabel(label_text, filepath, displayLayout, layout)
                        layout.addWidget(label)
                layout.addStretch()

            except Exception as e:
                print(f"Error while adding tickets to layout: {e}")

        # Adding new clickable labels as tickets
        directory = "../Database/Tickets"
        add_tickets_to_layout(directory, self.mainLayout, self.displayWidget)

    def numOfTickets(self):
        directory = "../Database/Tickets"
        num_files = sum([len(files) for r, d, files in os.walk(directory)])
        return num_files


class DateTime(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        def dateTimeWidget():
            dateTimeW = QWidget()
            dateTimeL = QVBoxLayout(dateTimeW)
            dateTimeL.setContentsMargins(0, 0, 0, 0)

            self.date_label = QLabel(self)
            self.date_label.setStyleSheet(f'font-size:{tiny_font_size}; font-family: Copperplate; color: black;')
            self.update_date_label()

            self.time_label = QLabel(self)
            self.time_label.setStyleSheet(f'font-size: {medium_font_size}; font-family: Copperplate; color: black;')
            self.update_time_label()

            dateTimeL.addWidget(self.date_label)
            dateTimeL.addWidget(self.time_label)
            return dateTimeW

        self.mainLayout.addWidget(dateTimeWidget())

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_label)
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(60000)  # Update every 60000 milliseconds (1 minute)

    def update_date_label(self):
        # Update the QLabel with the current date
        current_date = QDate.currentDate().toString("dddd, MMMM dd, yyyy")
        self.date_label.setText(current_date)

    def update_time_label(self):
        # Update the QLabel with the current time
        current_time = QTime.currentTime().toString("hh:mm AP")
        self.time_label.setText(current_time)


class TableWidget(QWidget):
    removeRequested = pyqtSignal()

    def __init__(self, context, parent=None):
        super().__init__(parent)
        self.context = context

        self.employee_mapping = {
            "Employee ID": "employeeID",
            "First Name": "firstName",
            "Last Name": "lastName",
            "Gender": "gender",
            "Title": "title",
            "Pass Code": "passcode",
            "Phone Number": "phoneNumber",
            "Email": "email",
            "Hire Date": "hireDate"
        }

        self.user_mapping = {
            "ID": "id",
            "First Name": "firstName",
            "Last Name": "lastName",
            "Gender": "gender",
            "Company": "company",
            "Title": "title",
            "Photos": "photos",
            "Face Encoding": "faceEncoding"
        }

        self.initUI()

    def initUI(self):
        self.mainLayout = QVBoxLayout(self)
        self.setLayout(self.mainLayout)

        if self.context == "Indirect User Button":
            self.indirectUserFiles()
        if self.context == "Employee Button":
            self.employeeFiles()
        if self.context == "Logs":
            self.logs()

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

    def createTable(self, rowLength, columnLength, objects):
        container, layout = self.setup_container_and_layout()

        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Search...")
        layout.addWidget(self.search_line_edit)

        self.table_widget = self.setup_table_widget(columnLength, rowLength, objects)
        layout.addWidget(self.table_widget)

        self.add_buttons_to_layout(layout)

        # Connect the textChanged signal to your search function
        self.search_line_edit.textChanged.connect(self._on_search)

        return container

    def setup_container_and_layout(self):
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)
        return container, layout

    def setup_table_widget(self, columnLength, rowLength, objects):
        self.table_widget = QTableWidget()
        self._styleTable()
        self.table_widget.setRowCount(rowLength)
        self.table_widget.setColumnCount(columnLength)
        headers, mapping = self.get_headers_and_mapping(objects)
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.populate_table_with_data(objects, headers, mapping, self.table_widget)
        return self.table_widget

    def get_headers_and_mapping(self, objects):
        if all(isinstance(obj, Employee) for obj in objects):
            return list(self.employee_mapping.keys()), self.employee_mapping
        elif all(isinstance(obj, User) for obj in objects):
            return list(self.user_mapping.keys()), self.user_mapping
        else:
            raise ValueError("Invalid object type")

    def populate_table_with_data(self, objects, headers, mapping, table_widget):
        for row, obj in enumerate(objects):
            for column, header in enumerate(headers):
                attribute_name = mapping[header]
                item = getattr(obj, attribute_name, '')
                cell = QTableWidgetItem(str(item))
                table_widget.setItem(row, column, cell)

    def add_buttons_to_layout(self, layout):
        """Add buttons to the provided layout."""
        button_layout = self._createButtonLayout()
        layout.addLayout(button_layout)

    def _createButtonLayout(self):
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignLeft)
        saveButtonStyle = "background-color: black; color:white; border-radius: 20px;"
        self._addButton(buttonLayout, "Save", self.on_save_button_clicked, saveButtonStyle)
        self._addButton(buttonLayout, "Close", self.on_close_button_clicked, saveButtonStyle)
        return buttonLayout

    def _addButton(self, layout, text, callback, style):
        button = QPushButton(text)
        button.setFixedSize(150, 40)
        button.setStyleSheet(style)
        button.clicked.connect(callback)
        layout.addWidget(button)

    def indirectUserFiles(self):
        self.current_displayed_type = User
        loaded_users = [user.getUser() for user in dbu.load_users()]
        self.original_users = list(loaded_users)
        container = self.createTable(len(loaded_users), 8, loaded_users)
        self.mainLayout.addWidget(container)

    def employeeFiles(self):
        self.current_displayed_type = Employee
        loaded_employees = [Employee.getEmployee() for Employee in dbe.load_employees()]
        self.original_employees = list(loaded_employees)
        container = self.createTable(len(loaded_employees), 9, loaded_employees)
        self.mainLayout.addWidget(container)

    def logs(self):
        csv_path = "../Database/Logs/log.csv"
        self.mainLayout.addWidget(self.csv_widget(csv_path))

    def csv_widget(self, csv_path):
        container = QWidget()
        layout = QVBoxLayout(container)

        self.search_line_edit = QLineEdit()
        self.search_line_edit.setPlaceholderText("Search...")
        layout.addWidget(self.search_line_edit)

        self.table_widget = QTableWidget()
        self._styleTable()
        self._populateTableFromCSV(csv_path)
        layout.addWidget(self.table_widget)
        layout.addLayout(self._createButtonLayout())

        self.search_line_edit.textChanged.connect(self._on_search)

        container.setLayout(layout)
        return container

    def _populateTableFromCSV(self, csv_path):
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

    def on_save_button_clicked(self):
        # Check the type of object currently displayed
        if self.current_displayed_type == Employee:
            mapping = self.employee_mapping
            obj_type = Employee
            original_objects = self.original_employees
            db = dbe
            print("emp")
        elif self.current_displayed_type == User:
            mapping = self.user_mapping
            obj_type = User
            original_objects = self.original_users
            db = dbu
        else:
            sender = self.sender()
            parent_widget = sender.parent()
            parent_widget.deleteLater()
            return

        updated_objects = []  # List to store the updated objects

        # Iterate through each row of the table
        for row in range(self.table_widget.rowCount()):
            attributes = {}  # Temporary dictionary to store the updated attributes

            # Iterate through each column of the table
            for col in range(self.table_widget.columnCount()):
                table_item = self.table_widget.item(row, col)

                if table_item:
                    table_value = table_item.text()  # Value from the table
                    header = self.table_widget.horizontalHeaderItem(col).text()  # Column header

                    # Using the mapping to get the corresponding attribute name of the object
                    attribute_name = mapping[header]

                    # Update the temporary dictionary with the new value
                    attributes[attribute_name] = table_value

            # Create a new object using the updated attributes from the temporary dictionary
            # Assuming both User and Employee have the same constructor signature
            updated_object = obj_type(**attributes)
            updated_objects.append(updated_object)

        # Replace the old objects with the updated ones
        if obj_type == Employee:
            db.employees = updated_objects
            db.save_employees()
        elif obj_type == User:
            db.users = updated_objects
            db.save_users()

        # Close the current table container
        sender = self.sender()
        parent_widget = sender.parent()
        parent_widget.deleteLater()

    def _on_search(self):
        search_text = self.search_line_edit.text().lower()
        for i in range(self.table_widget.rowCount()):
            row_matches = False
            for j in range(self.table_widget.columnCount()):
                item = self.table_widget.item(i, j)
                if item and search_text in item.text().lower():
                    row_matches = True
                    break
            self.table_widget.setRowHidden(i, not row_matches)

    def on_close_button_clicked(self):
        # Define the behavior for when the close button is clicked
        # For example, if you just want to close the widget:
        self.close()


class addUser(QWidget):
    removeRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        """Initializes the UI components."""
        self.mainLayout = QVBoxLayout(self)
        self.qBox()
        self.setLayout(self.mainLayout)

    def qBox(self):
        """Creates the 'Add User' group box with its layout and styles."""
        self._initialize_widgets()
        self._style_widgets()
        self._create_form()
        self.mainLayout.addWidget(self.groupBox)

    def _initialize_widgets(self):
        """Initializes the widgets used in the 'Add User' group box."""
        # Group box
        self.groupBox = QGroupBox("Add User")

        # Line edits
        self.id = self._create_line_edit()
        self.firstName = self._create_line_edit()
        self.lastName = self._create_line_edit()
        self.company = self._create_line_edit()
        self.title = self._create_line_edit()
        self.photo = self._create_line_edit(readonly=True)
        self.faceEncoding = self._create_line_edit(readonly=True)

        # Gender combo box
        self.genderComboBox = QComboBox()
        self.genderComboBox.addItems(["Male", "Female"])
        self.genderComboBox.setCurrentIndex(-1)

    def _create_line_edit(self, readonly=False):
        """Creates a QLineEdit with some default attributes."""
        le = QLineEdit()
        le.setAttribute(Qt.WA_MacShowFocusRect, 0)
        le.setReadOnly(readonly)
        return le

    def _style_widgets(self):
        groupBoxStylesheet = """
            QGroupBox {
                color: black;
                border: 2px solid black;
                border-radius: 15px;
                margin-top: 10px;
                padding: 20px;
                font-size: 25px;
                background-color: #FAFAFA;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px 20px;
                background-color: black;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: bold;
                color: white;
            }

            QLabel {
                qproperty-alignment: AlignCenter;
                color: black;
                background-color: transparent;
                font-weight: bold;
                font-size: 18px;
                margin: 5px 0;
            }

            QComboBox {
                color: black;
                background-color: white;
                font-size: 20px;  /* Increased font size */
                padding: 10px 15px;  /* Adjusted padding for more space */
                border: 1px solid black;
                border-radius: 10px;  /* Slightly larger radius for larger box */
                margin: 5px 0;
                min-height: 20px;  /* Explicitly set a minimum height if needed */
            }
            QComboBox QAbstractItemView {
                background-color: white;

                border: none;  /* Removes the borders */
                outline: none;

            }

            QComboBox::drop-down {
                width: 20px;  /* Adjust if needed to make drop-down arrow region bigger */

            }

            QComboBox::down-arrow {
                width: 20px;
                height: 20px;
            }

            QComboBox:hover {
                border: 1px solid black;
            }

            QLineEdit {
                color: black;
                font-size: 22px;
                padding: 5px 10px;
                border: 1px solid black;
                border-radius: 8px;
                background-color: #FFFFFF;
                margin: 5px 0;
            }

            QLineEdit:hover {
                border: 1px solid black;
            }

            QPushButton {
                color: white;
                font-size: 20px;
                padding: 10px 20px;
                border: none;
                border-radius: 20px;
                background-color: black;
                margin-left: 10px; /* Spacing between buttons */
                margin-right: 10px; /* Spacing between buttons */
            }

            QPushButton:hover {
                background-color: #E5154A;
            }

            QPushButton:pressed {
                background-color: #C4123D;
            }

            QPushButton:disabled {
                background-color: #DDDDDD;
                color: #AAAAAA;
            }
            """

        self.groupBox.setStyleSheet(groupBoxStylesheet)

    def _create_form(self):
        """Creates the form layout inside the 'Add User' group box."""
        formLayout = QFormLayout()
        formLayout.setFormAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        formLayout.addRow(QLabel("User ID: "), self.id)
        formLayout.addRow(QLabel("First Name: "), self.firstName)
        formLayout.addRow(QLabel("Last Name: "), self.lastName)
        formLayout.addRow(QLabel("Gender: "), self.genderComboBox)
        formLayout.addRow(QLabel("Company Name: "), self.company)
        formLayout.addRow(QLabel("Title: "), self.title)
        formLayout.addRow(QLabel("Photo: "), self.photo)
        formLayout.addRow(QLabel("Face Encoding: "), self.faceEncoding)

        buttonLayout = self._create_button_layout()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addStretch()
        self.groupBox.setLayout(mainLayout)

    def _create_button_layout(self):
        """Creates and returns the button layout."""
        self.openCameraButton = self._create_button("Open Cam", self.openCamera, size=(175, 40))
        self.saveProfileButton = self._create_button("Save Profile", self.saveNewUser, size=(175, 40),
                                                     hide_initially=True)
        cancelButton = self._create_button("Cancel", self.emitRemoveRequest, size=(175, 40))

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.openCameraButton)
        buttonLayout.addWidget(self.saveProfileButton)
        buttonLayout.addWidget(cancelButton)
        buttonLayout.addStretch()

        return buttonLayout

    def _create_button(self, label, slot, size=(150, 40), hide_initially=False):
        """Utility function to create a styled QPushButton."""
        btn = QPushButton(label)
        btn.setFixedSize(*size)
        btn.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        btn.clicked.connect(slot)
        if hide_initially:
            btn.hide()
        return btn

    def camInit(self):
        # OpenCV camera initialization
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.camLayout = QVBoxLayout()
        self.displayLabel = QLabel(self)
        self.camLayout.addWidget(self.displayLabel)
        self.camButtonLayout = QHBoxLayout()
        self.initTakePhotoButton = QPushButton("Take Photo")
        self.initTakePhotoButton.setFixedSize(150, 40)
        self.initTakePhotoButton.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        self.camButtonLayout.addWidget(self.initTakePhotoButton)
        self.initTakePhotoButton.clicked.connect(self.capturePhoto)

        self.retakePhotoButton = QPushButton("Retake Photo")
        self.retakePhotoButton.setFixedSize(150, 40)
        self.retakePhotoButton.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        self.camButtonLayout.addWidget(self.retakePhotoButton)
        self.retakePhotoButton.clicked.connect(self.retakePhoto)
        self.retakePhotoButton.hide()

        self.savePhotoButton = QPushButton("Save Photo")
        self.savePhotoButton.setFixedSize(150, 40)
        self.savePhotoButton.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        self.camButtonLayout.addWidget(self.savePhotoButton)
        self.savePhotoButton.clicked.connect(self.saveAndReturn)
        self.savePhotoButton.hide()

        self.camLayout.addLayout(self.camButtonLayout)
        self.mainLayout.addLayout(self.camLayout)

    def cancelAction(self):
        parent = self.parent()
        if isinstance(parent, MainWindow):
            parent.clearLayout()

    def camInit(self):
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.setupCameraUI()

    def setupCameraUI(self):
        self.camLayout = QVBoxLayout()
        self.displayLabel = QLabel(self)
        self.camLayout.addWidget(self.displayLabel)

        self.camButtonLayout = QHBoxLayout()
        self.initTakePhotoButton = self.createButton("Take Photo", self.capturePhoto)
        self.retakePhotoButton = self.createButton("Retake Photo", self.retakePhoto, False)
        self.savePhotoButton = self.createButton("Save Photo", self.saveAndReturn, False)

        self.camButtonLayout.addWidget(self.initTakePhotoButton)
        self.camButtonLayout.addWidget(self.retakePhotoButton)
        self.camButtonLayout.addWidget(self.savePhotoButton)
        self.camLayout.addLayout(self.camButtonLayout)

        self.mainLayout.addLayout(self.camLayout)

    def createButton(self, text, slot, is_visible=True):
        button = QPushButton(text)
        button.setFixedSize(150, 40)
        button.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        button.clicked.connect(slot)
        button.setVisible(is_visible)
        return button

    def openCamera(self):
        self.camInit()
        self.groupBox.hide()
        self.timer.start(30)

    def updateFrame(self):
        ret, frame = self.cap.read()
        if ret:
            self.displayImage(frame)

    def displayImage(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        self.current_qimage = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(self.current_qimage)
        scaled_pixmap = pixmap.scaled(self.displayLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.displayLabel.setPixmap(scaled_pixmap)

    def capturePhoto(self):
        self.timer.stop()
        self.currentPhoto = self.current_qimage.copy()
        self.toggleCameraButtons(False, True, True)

    def retakePhoto(self):
        self.toggleCameraButtons(True, False, False)
        self.timer.start(30)

    def toggleCameraButtons(self, init_visible, retake_visible, save_visible):
        self.initTakePhotoButton.setVisible(init_visible)
        self.retakePhotoButton.setVisible(retake_visible)
        self.savePhotoButton.setVisible(save_visible)

    def saveAndReturn(self):
        directory = "../Database/AddLocal"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, f"{self.id.text()}_0.jpg")
        self.currentPhoto.save(file_path)
        self.savePKL()

        self.closeCameraUI()

    def closeCameraUI(self):
        self.timer.stop()
        self.cap.release()
        self.displayLabel.clear()
        self.toggleCameraButtons(False, False, False)

        self.saveProfileButton.show()
        self.openCameraButton.hide()

        for widget in reversed(self.camLayout.children()):
            widget.deleteLater()

        self.photo.setText(f"{self.id.text()}_0.jpg")
        self.faceEncoding.setText(f"{self.id.text()}_0.pkl")
        self.groupBox.show()

    def closeEvent(self, event):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
            self.removeFiles()

    def cancelAction(self):
        parent = self.parent()
        if isinstance(parent, MainWindow):
            parent.clearLayout()

    # ----- User Data Management -----

    def saveNewUser(self):
        newUser = User(
            id=self.id.text(),
            firstName=self.firstName.text(),
            lastName=self.lastName.text(),
            gender=self.genderComboBox.currentText(),
            company=self.company.text(),
            title=self.title.text(),
            photos=self.photo.text(),
            faceEncoding=self.faceEncoding.text()
        )

        dbu.add_user(newUser)

        self.moveFile(f"../Database/AddLocal/{self.photo.text()}",
                      f"../Database/IndirectUsers/photos/{self.photo.text()}")
        self.moveFile(f"../Database/AddLocal/{self.faceEncoding.text()}",
                      f"../Database/IndirectUsers/face_encodings/{self.faceEncoding.text()}")

        db_conn = database.db
        coll_ref = db_conn.collection("indirectUser")
        coll_ref.add({
            "id": self.id.text(),
            "firstName": self.firstName.text(),
            "lastName": self.lastName.text(),
            "gender": self.genderComboBox.currentText(),
            "company": self.company.text(),
            "title": self.title.text()
        })

        print("data added successfully")

        self.emitRemoveRequest()

    def savePKL(self):
        file_path = f"../Database/AddLocal/{self.id.text()}_0.jpg"
        # Save plk
        face_detector = dlib.get_frontal_face_detector()
        shape_predictor = dlib.shape_predictor("../Database/datFiles/shape_predictor_68_face_landmarks.dat")
        face_recognizer = dlib.face_recognition_model_v1(
            "../Database/datFiles/dlib_face_recognition_resnet_model_v1.dat")
        # Load the image
        image = dlib.load_rgb_image(file_path)
        faces = face_detector(image)  # Detect faces in the image

        known_face_data = {
            "name": f"{self.id.text()}_0",
            "face_descriptors": [],
            "image_path": file_path,
        }

        for face in faces:
            shape = shape_predictor(image, face)
            face_descriptor = face_recognizer.compute_face_descriptor(image, shape)
            known_face_data["face_descriptors"].append(face_descriptor)
        # Save the known_face_data to a pickle file
        pickle_file_path = f"../Database/AddLocal/{self.id.text()}_0.pkl"  # Choose a filename for your pickle file
        with open(pickle_file_path, "wb") as f:
            pickle.dump(known_face_data, f)
        self.faceEncoding.setText(f"{self.id.text()}_0.pkl")

    def moveFile(self, source, destination):
        shutil.move(source, destination)

    def removeFiles(self):
        folder_path = '../Database/AddLocal'
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    def emitRemoveRequest(self):
        self.removeFiles()
        self.removeRequested.emit()


class CustomTabBar(QTabBar):
    def __init__(self, *args, **kwargs):
        super(CustomTabBar, self).__init__(*args, **kwargs)
        self._notifications = {}  # Initialize an empty dictionary to hold notification data

    def setNotification(self, index, value):
        # Update the notification count for a given tab index
        self._notifications[index] = value
        self.update()  # Trigger a repaint so the notification will be shown

    def paintEvent(self, event):
        super(CustomTabBar, self).paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Loop over each tab and draw the notification circle if needed
        for index, value in self._notifications.items():
            if value > 0:  # Only draw the notification if value is greater than 0
                rect = self.tabRect(index)
                circle_x = rect.right() - 20
                circle_y = rect.top() + 80
                circle_radius = 8  # The radius for the notification circle

                # Save the current painter state
                painter.save()

                # Translate painter's origin to the center of the circle for rotation
                painter.translate(circle_x + circle_radius, circle_y + circle_radius)

                # Rotate the painter by 90 degrees
                painter.rotate(90)

                # Set the painter color and brush for the notification circle
                painter.setBrush(Qt.red)
                painter.setPen(Qt.NoPen)

                # Draw the circle (adjust coordinates since we've translated the painter's origin)
                painter.drawEllipse(-circle_radius, -circle_radius, circle_radius * 2, circle_radius * 2)

                # Draw the text number of notifications on the circle
                font = painter.font()
                font.setBold(True)
                painter.setFont(font)
                painter.setPen(Qt.white)
                painter.drawText(QRectF(-circle_radius, -circle_radius, circle_radius * 2, circle_radius * 2),
                                 Qt.AlignCenter, str(value))

                # Restore the painter's state
                painter.restore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ManagerWindow()  # Instantiate HeaderWidget directly
    window.show()
    sys.exit(app.exec_())