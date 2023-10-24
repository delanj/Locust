import csv
import inspect
import json
import os
import sys
import cv2
from PyQt5.QtCore import QTimer, Qt, QDateTime, QDate, QTime
from PyQt5.QtGui import QImage, QPixmap, QPainter, QLinearGradient, QColor, QPen, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, \
    QPushButton, QSpacerItem, QSizePolicy, QFrame, QDesktopWidget, QDateTimeEdit, QCalendarWidget, QTableView, \
    QToolButton, QTableWidget, QTableWidgetItem
import dlib
import pickle

from PyQt5.uic.properties import QtWidgets

import Entities.IndirectUser.User
import Entities.Employee.Employee
import shutil


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
#Employees
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

class CustomWidgetGradient(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(250, 250, 250))
        gradient.setColorAt(1, QColor(230, 230, 230))
        painter.setBrush(gradient)
        painter.drawRect(self.rect())
class BlackLine(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(3)
        self.setStyleSheet("color: black; background-color:black;")
        self.setContentsMargins(0,0,0,0)

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
        self.showMaximized()
        self.showFullScreen()




        central_widget = CustomWidgetGradient()
        headerWidget = HeaderWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.addWidget(headerWidget)
        central_layout.setAlignment(Qt.AlignTop)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)


        mainLayout = QHBoxLayout()
        central_layout.addLayout(mainLayout)
        blackLine = BlackLine()



        #SIZE#
        screen_geometry = QApplication.desktop().screenGeometry()
        window_width = int(screen_geometry.width()-40)
        window_height = int(screen_geometry.height())
        headerSize = headerWidget.sizeHint().height()



        #Left container------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # Size for left widget
        leftWidgetWidth = window_width / 5 # Width
        # Height

        leftWidget = QWidget()
        leftWidget.setStyleSheet("background-color:white;")
        leftWidget.setMaximumWidth(int(leftWidgetWidth))
        #leftWidget.setFixedHeight()


        leftLayout = QVBoxLayout(leftWidget)
        leftLayout.setAlignment(Qt.AlignLeft)
        #leftLayout.setStretchFactor(central_layout, 1)
        # Left content
        #---------------------------------------------------
        # QLabel to display the current date
        self.date_label = QLabel(self)
        self.date_label.setStyleSheet(f'font-size:{tiny_font_size}; font-family: Copperplate; color: black;')
        self.update_date_label()

        # QLabel to display the current time
        self.time_label = QLabel(self)
        self.time_label.setStyleSheet(f'font-size: {medium_font_size}; font-family: Copperplate; color: black;')
        self.update_time_label()

        #Add widget to layout-------------------------
        leftLayout.addWidget(self.date_label)
        leftLayout.addWidget(self.time_label)







        # Logs
        # --------------------------------------------------------------------------------------------------------------
        logsWidget = QWidget()
        logsWidget.setStyleSheet("background-color: transparent")
        logsWidget.setContentsMargins(0, 0, 10, 0)
        logsWidget.setFixedWidth(int(leftWidgetWidth))

        logsLayout = QVBoxLayout(logsWidget)
        logsLayout.setAlignment(Qt.AlignTop)

        logLabel = QLabel("Logs")
        logLabel.setStyleSheet(f'font-size: {medium_font_size}; font-family: Copperplate; color: black;')
        logsLayout.addWidget(logLabel)

        logsLayout.addWidget(blackLine)
        class CustomButton(QPushButton):
            def __init__(self, text):
                super().__init__(text)
                self.initUI()
                #self.setFixedWidth(int(leftWidgetWidth))
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

        userButton = CustomButton("Indirect Users")
        userButton.clicked.connect(self.on_user_button_clicked)

        employeeButton = CustomButton("Employee")
        employeeButton.clicked.connect(self.on_employee_button_clicked)

        logsButton = CustomButton("Logs")
        logsButton.clicked.connect(self.on_logs_button_clicked)

        logsLayout.addWidget(userButton)
        logsLayout.addWidget(employeeButton)
        logsLayout.addWidget(logsButton)


        leftLayout.addWidget(logsWidget)
        leftLayout.addStretch()

        addUserButton = QPushButton("button")
        addUserButton.setFixedSize(150, 40)
        addUserButton.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        addUserButton.clicked.connect(self.add_user)
        leftLayout.addWidget(addUserButton)


        # Middle container---------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------

        #Middle widget
        middleWidget = QWidget()
        middleWidget.setStyleSheet("background-color:transparent;")
        middleWidgetWidth = window_width - (leftWidgetWidth * 2)

        #Middle layout
        middleLayout = QVBoxLayout(middleWidget)
        middleLayout.setAlignment(Qt.AlignTop)

        # Middle content
        displayWidget = QWidget()
        displayWidget.setStyleSheet("background-color: white")
        displayWidget.setFixedWidth(int(middleWidgetWidth))




        self.displayLayout = QVBoxLayout(displayWidget)



        middleLayout.addWidget(displayWidget)
        middleLayout.setStretchFactor(displayWidget, 1)


        # Right container----------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        #rightWidgetWidth = window_width / 5
        rightWidget = QWidget()
        rightWidget.setStyleSheet("background-color:White;")
        rightLayout = QVBoxLayout(rightWidget)
        rightLayout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        rightWidget.setFixedWidth(leftWidget.size().width())

        # Tickets
        # --------------------------------------------------------------------------------------------------------------
        ticketWidget = QWidget()
        ticketWidget.setStyleSheet("background-color: transparent")
        ticketWidget.setContentsMargins(0, 0, 0, 0)
        ticketLayout = QVBoxLayout(ticketWidget)


        # ticketLabel = QLabel("Tickets")
        # ticketLabel.setStyleSheet(f'font-size: {medium_font_size}; font-family: Copperplate; color: black;')
        # rightLayout.addWidget(ticketLabel)
        # ticketLayout.addWidget(blackLine)

        class ClickableLabel(QLabel):
            def __init__(self, text):
                super().__init__(text)
                self.setFixedWidth(int(rightWidget.size().width()/1.3))
                buttonH = int((rightWidget.size().width()/1.3) / 4)
                self.setFixedHeight(buttonH)
                #self.setAlignment(Qt.AlignLeft)
                self.setStyleSheet("border: 1px solid #CCCCCC; padding: 0px; "
                                   "background-color: #F5F5F5; border-radius: 5px; color:black;")
            def enterEvent(self, event):
                # When the mouse hovers over the label, change its color to indicate that it's clickable
                self.setStyleSheet("border: 1px solid #AAAAAA; padding: 0px; "
                                   "background-color: #E0E0E0; border-radius: 5px; color:black;")
            def leaveEvent(self, event):
                # When the mouse leaves the label, revert its color
                self.setStyleSheet("border: 1px solid #CCCCCC; padding: 0px; "
                                   "background-color: #F5F5F5; border-radius: 5px; color:black;")
            def mousePressEvent(self, event):
                if event.button() == Qt.LeftButton:
                    print(f"{self.text()} was clicked!")



        # Adding new clickable labels as tickets
        ticketLabel1 = ClickableLabel("Ticket 1")
        ticketLabel2 = ClickableLabel("Ticket 2")
        ticketLabel3 = ClickableLabel("Ticket 3")
        ticketLabel4 = ClickableLabel("Ticket 4")
        ticketLayout.addWidget(ticketLabel1)
        ticketLayout.addWidget(ticketLabel2)
        ticketLayout.addWidget(ticketLabel3)
        ticketLayout.addWidget(ticketLabel4)




        rightLayout.addWidget(ticketWidget)
        createTicketButton = QPushButton("Create Ticket")
        createTicketButton.setFixedWidth(150)
        createTicketButton.setFixedHeight(40)
        createTicketButton.setStyleSheet("background-color: black; color:white; border-radius: 20px;")

        rightLayout.addWidget(createTicketButton)

        rightLayout.addStretch()



        # Calendar
        # --------------------------------------------------------------------------------------------------------------
        calendar = QCalendarWidget(rightWidget)
        calendar.setFixedHeight(200)
        calendar.setContentsMargins(0, 0, 0, 0)
        calendar.setVerticalHeaderFormat(False)
        calendar.findChild(QToolButton, "qt_calendar_prevmonth").hide()
        calendar.findChild(QToolButton, "qt_calendar_nextmonth").hide()
        calendar_stylesheet = """
        QCalendarWidget {border: none;}
        QCalendarWidget QWidget {background-color: white; color: black;}
        QCalendarWidget QTableView {border: none; gridline-color: #c0c0c0;}
        QCalendarWidget QTableView QHeaderView::section {background-color: #e0e0e0; padding: 4px;
            border: 1px solid #c0c0c0; font-size: 10pt; font-weight: bold;}
        QCalendarWidget QToolButton {icon-size: 20px; border: none; background-color: #e0e0e0;}
        QCalendarWidget QMenu { border: none;}
        QCalendarWidget QMenu::item {padding: 4px 20px 4px 20px;}
        QCalendarWidget QMenu::item:selected {background-color: #c0c0c0;}
        QCalendarWidget QAbstractItemView {border: none;}
        QCalendarWidget QLabel {font-size: 24pt; /* Adjust the font size as needed */}
        """
        calendar.setStyleSheet(calendar_stylesheet)
        rightLayout.addWidget(calendar)


        # --------------------------------------------------------------------------------------------------------------


        mainLayout.addWidget(leftWidget)
        mainLayout.addWidget(middleWidget)

        mainLayout.addWidget(rightWidget)
        #mainLayout.setStretchFactor(rightWidget, 1)






        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_label)
        self.timer.timeout.connect(self.update_time_label)
        self.timer.start(60000)  # Update every 60000 milliseconds (1 minute)

    # ...

    def update_date_label(self):
        # Update the QLabel with the current date
        current_date = QDate.currentDate().toString("dddd, MMMM dd, yyyy")
        self.date_label.setText(current_date)

    def update_time_label(self):
        # Update the QLabel with the current time
        current_time = QTime.currentTime().toString("hh:mm AP")
        self.time_label.setText(current_time)


    def createTable(self, rowLength=None, columnLength=None, objects=None,):
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        self.table_widget = QTableWidget()
        table_stylesheet = """
            QTableWidget {
                gridline-color: #d4d4d4; /* Light gray gridlines */
                border: none;
                color: black; /* Text color for table items */
            }
            QHeaderView::section {
                background-color: #e6e6e6; /* Light gray header */
                padding: 4px;
                border: 1px solid #d4d4d4;
                font-weight: bold;
                color: black; /* Text color for headers */
            }
            QLineEdit { color: black; }
        """
        self.table_widget.setStyleSheet(table_stylesheet)

        self.table_widget.setRowCount(rowLength)
        self.table_widget.setColumnCount(columnLength)


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

        if all(isinstance(obj, Employee) for obj in objects):
            headers = list(self.employee_mapping.keys())
        elif all(isinstance(obj, User) for obj in objects):
            headers = list(self.user_mapping.keys())

        else:
            raise ValueError("Invalid object type")

        self.table_widget.setHorizontalHeaderLabels(headers)

        for row, obj in enumerate(objects):
            if isinstance(obj, Employee):
                mapping = self.employee_mapping
            elif isinstance(obj, User):
                mapping = self.user_mapping
            else:
                mapping = {header: header for header in headers}  # For logs, assuming header matches attribute name

            for column, header in enumerate(headers):
                attribute_name = mapping[header]
                item = getattr(obj, attribute_name, '')
                cell = QTableWidgetItem(
                    str(item))  # Convert item to string to ensure compatibility with QTableWidgetItem
                self.table_widget.setItem(row, column, cell)

        layout.addWidget(self.table_widget)  #

        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)

        self.saveButton = QPushButton("Save")
        self.saveButton.setFixedSize(150, 40)
        self.saveButton.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        self.saveButton.clicked.connect(self.on_save_button_clicked)
        buttonLayout.addWidget(self.saveButton)

        self.closeButton = QPushButton("Close")
        self.closeButton.setFixedSize(150, 40)
        self.closeButton.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        self.closeButton.clicked.connect(self.on_close_button_clicked)
        buttonLayout.addWidget(self.closeButton)

        buttonLayout.setAlignment(Qt.AlignLeft)

        return container  # Return the container holding both the table and the button

    def csv_widget(self, csv_path):
        container = QWidget()
        layout = QVBoxLayout()
        container.setLayout(layout)

        # Create the QTableWidget
        table_widget = QTableWidget()

        table_stylesheet = """
                    QTableWidget {
                        gridline-color: #d4d4d4; /* Light gray gridlines */
                        border: none;
                        color: black; /* Text color for table items */
                    }
                    QHeaderView::section {
                        background-color: #e6e6e6; /* Light gray header */
                        padding: 4px;
                        border: 1px solid #d4d4d4;
                        font-weight: bold;
                        color: black; /* Text color for headers */
                    }
                """
        table_widget.setStyleSheet(table_stylesheet)

        data = []
        try:
            with open(csv_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                data = list(csvreader)
        except FileNotFoundError:
            print("CSV file not found or path is incorrect.")
            return container  # Return empty container if error

        # Set the header labels using the first row from the CSV file
        table_widget.setHorizontalHeaderLabels(data[0])

        # Set the number of rows (minus the header) and columns
        table_widget.setRowCount(len(data) - 1)
        table_widget.setColumnCount(len(data[0]))

        # Populate the table with data, skipping the header row
        for i, row in enumerate(data[1:]):
            for j, value in enumerate(row):
                item = QTableWidgetItem(value)
                table_widget.setItem(i, j, item)

        # Add the table widget to the layout
        layout.addWidget(table_widget)



        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)

        self.saveButton = QPushButton("Save")
        self.saveButton.setFixedSize(150, 40)
        self.saveButton.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        self.saveButton.clicked.connect(self.on_save_button_clicked)
        buttonLayout.addWidget(self.saveButton)

        self.closeButton = QPushButton("Close")
        self.closeButton.setFixedSize(150, 40)
        self.closeButton.setStyleSheet("background-color: black; color:white; border-radius: 20px;")
        self.closeButton.clicked.connect(self.on_close_button_clicked)
        buttonLayout.addWidget(self.closeButton)

        buttonLayout.setAlignment(Qt.AlignLeft)

        return container  # Return the container holding both the table and the button

    def on_user_button_clicked(self):
        self.current_displayed_type = None
        for i in reversed(range(self.displayLayout.count())):
            widget = self.displayLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.current_displayed_type = User
        loaded_users = [user.getUser() for user in dbu.load_users()]
        self.original_users = list(loaded_users)

        container = self.createTable(objects=loaded_users, columnLength=8, rowLength=len(loaded_users))
        self.displayLayout.addWidget(container)
    def on_employee_button_clicked(self):
        self.current_displayed_type = None
        for i in reversed(range(self.displayLayout.count())):
            widget = self.displayLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        self.current_displayed_type = Employee
        loaded_employees = [Employee.getEmployee() for Employee in dbe.load_employees()]
        self.original_employees = list(loaded_employees)

        container = self.createTable(objects=loaded_employees, columnLength=9, rowLength=len(loaded_employees))
        self.displayLayout.addWidget(container)

    def on_logs_button_clicked(self):
        self.current_displayed_type = None
        for i in reversed(range(self.displayLayout.count())):
            widget = self.displayLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Create and add the employee table (and close button)
        csv_path = '../Database/Logs/log.csv'  # Update this to your CSV file's path
        container = self.csv_widget(csv_path)
        self.displayLayout.addWidget(container)

    def on_save_button_clicked(self):
        # Check the type of object currently displayed
        if self.current_displayed_type == Employee:
            mapping = self.employee_mapping
            obj_type = Employee
            original_objects = self.original_employees
            db = dbe
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
            # Assuming both User and Employee have same constructor signature
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
    def on_close_button_clicked(self):
        sender = self.sender()
        parent_widget = sender.parent()
        parent_widget.deleteLater()

    def add_user(self):
        self.current_displayed_type = None
        for i in reversed(range(self.displayLayout.count())):
            widget = self.displayLayout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()


        ucentral_widget = QWidget()
        u_central_layout = QVBoxLayout(ucentral_widget)
        u_central_layout.setContentsMargins(0, 0, 0, 0)
        u_main_layout = QHBoxLayout()
        u_central_layout.addLayout(u_main_layout)

        u_leftLayout = QVBoxLayout()
        u_leftLayout.addSpacing(50)
        u_main_layout.addLayout(u_leftLayout)
        uleftLayoutRow1 = QHBoxLayout()
        uleftLayoutRow2 = QHBoxLayout()
        uleftLayoutRow3 = QHBoxLayout()
        uleftLayoutRow4 = QHBoxLayout()
        u_leftLayout.addLayout(uleftLayoutRow1)
        u_leftLayout.addLayout(uleftLayoutRow2)
        u_leftLayout.addLayout(uleftLayoutRow3)
        u_leftLayout.addLayout(uleftLayoutRow4)

        uleftLayoutRow1.setAlignment(Qt.AlignLeft)
        uleftLayoutRow2.setAlignment(Qt.AlignLeft)
        uleftLayoutRow3.setAlignment(Qt.AlignLeft)
        uleftLayoutRow4.setAlignment(Qt.AlignLeft)

        # id
        idLayout = QVBoxLayout()
        idLabel = QLabel("ID")
        idLabel.setStyleSheet(
            f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: black;')
        idLayout.addWidget(idLabel)
        self.idLineEdit = QLineEdit()
        self.idLineEdit.setStyleSheet(f'background-color: white; padding: 5px; border: 1px solid black; color:black')
        self.idLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        self.idLineEdit.setFixedWidth(100)
        idLayout.addWidget(self.idLineEdit)
        uleftLayoutRow1.addLayout(idLayout)
        idLayout.addSpacing(50)
        idLayout.setContentsMargins(10, 10, 10, 10)

        # firstName
        firstNameLayout = QVBoxLayout()
        firstNameLabel = QLabel("First Name")
        firstNameLabel.setStyleSheet(
            f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: black;')
        firstNameLayout.addWidget(firstNameLabel)
        self.firstNameLineEdit = QLineEdit()
        self.firstNameLineEdit.setMaximumWidth(250)
        self.firstNameLineEdit.setStyleSheet(
            f'background-color: white; padding: 5px; border: 1px solid black; color:black')
        self.firstNameLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        firstNameLayout.addWidget(self.firstNameLineEdit)
        uleftLayoutRow2.addLayout(firstNameLayout)
        firstNameLayout.addSpacing(50)
        firstNameLayout.setContentsMargins(10, 10, 10, 10)

        # lastName
        lastNameLayout = QVBoxLayout()
        lastNameLabel = QLabel("Last Name")
        lastNameLabel.setStyleSheet(
            f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: black;')
        lastNameLayout.addWidget(lastNameLabel)
        self.lastNameLineEdit = QLineEdit()
        self.lastNameLineEdit.setMaximumWidth(250)
        self.lastNameLineEdit.setStyleSheet(
            f'background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.lastNameLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        lastNameLayout.addWidget(self.lastNameLineEdit)
        uleftLayoutRow2.addLayout(lastNameLayout)
        lastNameLayout.addSpacing(50)
        lastNameLayout.setContentsMargins(10, 10, 10, 10)

        # gender
        genderLayout = QVBoxLayout()
        genderLabel = QLabel("Gender")
        genderLabel.setStyleSheet(
            f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: black;')
        genderLayout.addWidget(genderLabel)
        self.genderLineEdit = QLineEdit()
        self.genderLineEdit.setStyleSheet(
            f'background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.genderLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        self.genderLineEdit.setFixedWidth(100)
        genderLayout.addWidget(self.genderLineEdit)
        uleftLayoutRow2.addLayout(genderLayout)
        genderLayout.addSpacing(50)
        genderLayout.setContentsMargins(10, 10, 10, 10)

        # company
        companyLayout = QVBoxLayout()
        companyLabel = QLabel("Company")
        companyLabel.setStyleSheet(
            f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: black;')
        companyLayout.addWidget(companyLabel)
        self.companyLineEdit = QLineEdit()
        self.companyLineEdit.setMaximumWidth(315)
        self.companyLineEdit.setStyleSheet(
            'background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.companyLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        companyLayout.addWidget(self.companyLineEdit)
        uleftLayoutRow3.addLayout(companyLayout)
        companyLayout.addSpacing(50)
        companyLayout.setContentsMargins(10, 10, 10, 10)

        # title
        titleLayout = QVBoxLayout()
        titleLabel = QLabel("Title")
        titleLabel.setStyleSheet(
            f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: black;')
        titleLayout.addWidget(titleLabel)
        self.titleLineEdit = QLineEdit()
        self.titleLineEdit.setMaximumWidth(315)
        self.titleLineEdit.setStyleSheet(
            'background-color: white; padding: 5px; border: 1px solid lableColor; color:black')
        self.titleLineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0);
        titleLayout.addWidget(self.titleLineEdit)
        uleftLayoutRow3.addLayout(titleLayout)
        titleLayout.addSpacing(50)
        titleLayout.setContentsMargins(10, 10, 10, 10)

        # photos
        photoLayout = QVBoxLayout()
        photoLabel = QLabel("Photo")
        photoLabel.setMaximumWidth(200)
        photoLabel.setStyleSheet(
            f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: black;')
        photoLayout.addWidget(photoLabel)
        self.photo = QLabel()
        self.photo.setMaximumWidth(200)
        self.photo.setStyleSheet('background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.photo.setAttribute(Qt.WA_MacShowFocusRect, 0);
        photoLayout.addWidget(self.photo)
        uleftLayoutRow4.addLayout(photoLayout)
        photoLayout.addSpacing(25)
        photoLayout.setContentsMargins(10, 10, 10, 10)

        # faceEncoding
        faceEncodingLayout = QVBoxLayout()
        faceEncodingLabel = QLabel("Face Encoding")
        faceEncodingLabel.setStyleSheet(
            f'background-color: transparent; font-size: 24pt; font-family: Copperplate; color: black;')
        faceEncodingLayout.addWidget(faceEncodingLabel)
        self.faceEncoding = QLabel()
        self.faceEncoding.setMaximumWidth(200)
        self.faceEncoding.setStyleSheet('background-color: white; padding: 5px; border: 1px solid black; color:black;')
        self.faceEncoding.setAttribute(Qt.WA_MacShowFocusRect, 0);
        faceEncodingLayout.addWidget(self.faceEncoding)
        uleftLayoutRow4.addLayout(faceEncodingLayout)
        faceEncodingLayout.addSpacing(25)
        faceEncodingLayout.setContentsMargins(10, 10, 10, 10)




        self.displayLayout.addWidget(ucentral_widget)









if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()  # Instantiate HeaderWidget directly
    window.show()
    sys.exit(app.exec_())