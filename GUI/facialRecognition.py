import csv
import os
import pickle
import sys
from datetime import datetime

import cv2
import dlib
import numpy as np
import pyfirmata
from pyfirmata import Arduino, util
import time
from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal, QEvent
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette, QColor, QPainter, \
    QTextOption
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QSizePolicy, QVBoxLayout, QPushButton, \
    QLineEdit, QGraphicsOpacityEffect, QSpacerItem, QTextEdit, \
    QFormLayout, QDialog
from PyQt5.QtWidgets import QLabel, QHBoxLayout

from Entities import entitiesMain

# Link to data base



FONT = "Garamond"

# Font Sizes
TITLE_FONT_SIZE = "36px"
SUBHEADER_FONT_SIZE = "24px"
BODY_FONT_SIZE = "18px"
BODY_SECONDARY_FONT_SIZE = "16px"
BUTTON_FONT_SIZE = "16px"
BUTTON_LABEL_SIZE = "14px"
CAPTIONS_FONT_SIZE = "12px"
DATA_TABLES_FONT_SIZE = "14px"
TOOLTIPS_FONT_SIZE = "16px"

# Colors
BACKGROUND_COLOR_TRANSPARENT = "background-color: transparent;"
SIDEBAR_COLOR = "#333940"
ICON_COLOR = "white"
SIDEBAR_TEXT_COLOR = "#E0E0E0"
MAIN_BACKGROUND_COLOR = "#FAFAFA"
CONTENT_CARD_BACKGROUND_COLOR = "#FEFEFE"
SECONDARY_FONT_COLOR = "#4A4A4A"
BUTTON_COLOR = "#B0BEC5"
TEXT_COLOR = "#4A4A4A"
BORDERS_LINES_COLOR = "#E0E0E0"
TEXT_COLOR_SECONDARY = "rgb(100, 100, 100)"
INTERACTIVE_ELEMENT_COLOR_1 = "rgb(220, 220, 220)"
INTERACTIVE_ELEMENT_COLOR_2 = "rgb(190, 190, 190)"
FIELD_BACKGROUND_COLOR = "rgb(255, 255, 255)"
PLACEHOLDER_COLOR = "rgb(200, 200, 200)"

# Graph Colors
GRAPH_BACKGROUND_COLOR = (250, 245, 232)
GRAPH_FONT_COLOR = (74, 74, 74)
GRAPH_BAR_COLOR = (176, 190, 197)

# Other UI Elements
OPACITY_EFFECT = QGraphicsOpacityEffect()
OPACITY_EFFECT.setOpacity(0.5)

current_file_directory = os.path.dirname(os.path.abspath(__file__))
locust_directory = os.path.abspath(os.path.join(current_file_directory, '..'))


class FacialRecognitionWindow(QMainWindow):
    """ Initialize the main Facial recognition window. """

    def __init__(self, window_manager=None, employee=None):
        """
        # Initialize the main Facial recognition window.
        @param window_manager: The window manager object.
        @param employee: The employee object.
        """
        super().__init__()
        self.window_manager = window_manager
        self.employee = employee
        self.setupUi()
        self.showFullScreen()

    def setupUi(self):
        """ Set up the main window."""
        self.webcam_handler = WebcamHandler()
        self.central_widget = QWidget()
        self.centralLayout = QHBoxLayout(self.central_widget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateLabel)

        def setup_sidebar():
            """ Set up the sidebar."""
            self.sideBar = QFrame(self.central_widget)
            self.sideBar.setStyleSheet(f"background-color: {SIDEBAR_COLOR};")
            self.sidebarLayout = QVBoxLayout(self.sideBar)
            self.sidebarLayout.setSpacing(0)
            self.sidebarLayout.setContentsMargins(0, 0, 0, 0)

            def setup_logo_widget():
                """ Set up the logo widget."""
                self.logoWidgetContainer = QWidget(self.sideBar)
                self.logoWidgetContainer.setObjectName("logoWidgetContainer")
                self.logoWidgetUi = Ui_logoWidget()
                self.logoWidgetUi.setupUi(self.logoWidgetContainer)
                self.sidebarLayout.addWidget(self.logoWidgetContainer, stretch=2)
            setup_logo_widget()

            def setup_scan_info_container():
                """ Set up the scan info container."""
                self.scanInfoContainer = QWidget(self.sideBar)
                self.scanInfoWidgetUi = Ui_scanInfo()
                self.scanInfoWidgetUi.setupUi(self.scanInfoContainer)
                self.sidebarLayout.addWidget(self.scanInfoContainer, stretch=10)
            setup_scan_info_container()

            def setup_buttons():
                """ Set up the buttons."""
                self.scanInfoWidgetUi.logoutButton.clicked.connect(self.closeCam)
                self.scanInfoWidgetUi.acceptButton.clicked.connect(self.acceptHandle)
                self.scanInfoWidgetUi.rejectButton.clicked.connect(self.rejectHandle)
            setup_buttons()

            self.centralLayout.addWidget(self.sideBar, stretch=2)
        setup_sidebar()

        def setup_main_window():
            """ Set up the main window."""
            self.mainWindow = QFrame(self.central_widget)
            self.mainWindow.setStyleSheet(f"background-color: {MAIN_BACKGROUND_COLOR};")
            self.mainLayout = QVBoxLayout(self.mainWindow)

            def setup_header_widget():
                """ Set up the header widget."""
                self.userHeaderContainer = QWidget(self.mainWindow)
                self.userHeaderUi = Ui_userHeaderWidget()
                self.userHeaderUi.setupUi(self.userHeaderContainer)
                if self.employee:
                    self.userHeaderUi.employee_name.setText(f"{self.employee.first_name} {self.employee.last_name}")

                self.userHeaderUi.employee_profile.clicked.connect(self.show_popup_window)
                QApplication.instance().installEventFilter(self.central_widget)

                self.mainLayout.addWidget(self.userHeaderContainer, stretch=1)
            setup_header_widget()

            def setup_display_container():
                """ Set up the display container."""
                self.displayContainer = QWidget(self.mainWindow)
                self.displayContainer.setObjectName("displayContainer")
                self.displayContainer.setStyleSheet(BACKGROUND_COLOR_TRANSPARENT)
                self.displayLayout = QVBoxLayout(self.displayContainer)
                self.mainLayout.addWidget(self.displayContainer, stretch=10)

                def setup_face_recognition_webcam_display():
                    """ Set up the face recognition webcam display."""
                    self.webcam_handler.setUser.connect(self.setUser)
                    self.webcam_handler.user_updated.connect(self.updateUser)

                    self.webcam_handler.webcam_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.webcam_handler.webcam_label.setMinimumWidth(640)

                    def setup_spacer_1():
                        self.spacer1 = QLabel()
                        self.displayLayout.addWidget(self.spacer1, stretch=1)
                    setup_spacer_1()

                    def setup_scan_handle_container():
                        self.scan_handle_frame = QFrame()
                        self.scan_handle_layout = QVBoxLayout(self.scan_handle_frame)
                        self.scan_handle_label = QLabel("")
                        self.scan_handle_label.setStyleSheet(
                            f"color: {TEXT_COLOR}; font: 75 {SUBHEADER_FONT_SIZE} '{FONT}';")
                        self.scan_handle_label.setAlignment(Qt.AlignCenter)
                        self.scan_handle_layout.addWidget(self.scan_handle_label)

                        self.displayLayout.addWidget(self.scan_handle_frame, stretch=1)
                    setup_scan_handle_container()

                    def setup_webcam():
                        self.displayLayout.addWidget(self.webcam_handler, stretch=20)
                    setup_webcam()

                    def setup_spacer_2():
                        self.spacer2 = QLabel()
                        self.displayLayout.addWidget(self.spacer2, stretch=2)
                    setup_spacer_2()


                setup_face_recognition_webcam_display()
            setup_display_container()

            self.centralLayout.addWidget(self.mainWindow, stretch=10)
        setup_main_window()

    def clearDisplayContainer(self):
        """ Clear the display container."""
        for i in reversed(range(self.displayLayout.count())):
            widget = self.displayLayout.itemAt(i).widget()
            if widget is not None:
                self.displayLayout.removeWidget(widget)
                widget.deleteLater()

    def setUser(self, user):
        """
        Set the current user.
        @param user: The user object.
        """
        self.current_user = user

    def closeCam(self):
        """ Close the webcam."""
        if hasattr(self, 'webcam_handler'):
            self.webcam_handler.close_webcam()

        self.close()
        if self.employee:
            self.window_manager.open_dashboard(employee=self.employee)
        else:
            self.window_manager.open_dashboard(employee=None)

    def show_popup_window(self):
        if hasattr(self, 'popup_dialog') and self.popup_dialog.isVisible():
            self.popup_dialog.hide()
            buttonStyleSheetNormal = f"""
                QPushButton {{
                    border: none;
                    border-radius: 20px;  /* Half of width and height to make it circular */
                    background-color: {BUTTON_COLOR};  /* Your desired background color for the normal state */
                }}
                QPushButton:hover {{
                    background-color: {INTERACTIVE_ELEMENT_COLOR_1};  /* Your desired background color when hovered */
                }}
                QPushButton:pressed {{
                    background-color: {INTERACTIVE_ELEMENT_COLOR_2};  /* Your desired background color when pressed */
                }}
            """
            self.userHeaderUi.employee_profile.setStyleSheet(buttonStyleSheetNormal)
            return

        self.popup_dialog = QDialog()
        self.popup_dialog.setWindowFlags(Qt.FramelessWindowHint)

        self.popup_dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {MAIN_BACKGROUND_COLOR};
                border: 2px solid {BORDERS_LINES_COLOR};
            }}

            QLabel {{
                color: {TEXT_COLOR};
                font-family: {FONT};
                font-size: {BODY_FONT_SIZE};
            }}

            QLineEdit {{
                background-color: {FIELD_BACKGROUND_COLOR};
                color: {TEXT_COLOR};
                font-family: {FONT};
                font-size: {BODY_FONT_SIZE};
                border: 1px solid {BORDERS_LINES_COLOR};
            }}

            QTextEdit {{
                background-color: {FIELD_BACKGROUND_COLOR};
                color: {TEXT_COLOR};
                font-family: {FONT};
                font-size: {BODY_FONT_SIZE};
                border: 1px solid {BORDERS_LINES_COLOR};
            }}

            QPushButton {{
                background-color: {BUTTON_COLOR};
                border: 1px solid {BORDERS_LINES_COLOR};
                padding: 5px;
                font-family: {FONT};
                font-size: {BUTTON_FONT_SIZE};
                font-size: {BODY_FONT_SIZE};
            }}
        """)

        def dialog_layout():
            # Create layout for the pop-up window
            self.popup_dialog_layout = QVBoxLayout()

            subject_label = QLabel("Subject")
            self.subject_line_edit = QLineEdit()

            description_label = QLabel("Description")
            self.description_line_edit = QTextEdit()
            self.description_line_edit.setFixedHeight(100)
            self.description_line_edit.setAlignment(Qt.AlignTop)
            self.description_line_edit.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)

            submit_button = QPushButton("Submit")
            submit_button.clicked.connect(self.submit_ticket)

            self.popup_dialog_layout.addWidget(subject_label)
            self.popup_dialog_layout.addWidget(self.subject_line_edit)
            self.popup_dialog_layout.addWidget(description_label)
            self.popup_dialog_layout.addWidget(self.description_line_edit)
            self.popup_dialog_layout.addWidget(submit_button)

            self.popup_dialog.setLayout(self.popup_dialog_layout)

        dialog_layout()

        main_window = self.userHeaderUi.employee_profile.window()

        def set_position():
            # Get the global position of the button
            global_button_position = main_window.mapToGlobal(self.userHeaderUi.employee_profile.pos())

            # Calculate new X and Y position
            x_position = global_button_position.x()
            y_position = global_button_position.y() + self.userHeaderUi.employee_profile.height()

            # Move the dialog to appear directly below the button
            self.popup_dialog.move(x_position, y_position + 30)

        set_position()

        if self.popup_dialog.isVisible():
            self.popup_dialog.hide()
            buttonStyleSheetNormal = f"""
                QPushButton {{
                    border: none;
                    border-radius: 20px;  /* Half of width and height to make it circular */
                    background-color: {BUTTON_COLOR};  /* Your desired background color for the normal state */
                }}
                QPushButton:hover {{
                    background-color: {INTERACTIVE_ELEMENT_COLOR_1};  /* Your desired background color when hovered */
                }}
                QPushButton:pressed {{
                    background-color: {INTERACTIVE_ELEMENT_COLOR_2};  /* Your desired background color when pressed */
                }}
                                            """
            self.userHeaderUi.employee_profile.setStyleSheet(buttonStyleSheetNormal)
        else:
            self.popup_dialog.show()
            buttonStyleSheetClicked = f"""
                        QPushButton {{
                            border: none;
                            border-radius: 20px;  /* Half of width and height to make it circular */
                            background-color: {INTERACTIVE_ELEMENT_COLOR_1};  /* Your desired background color for the normal state */
                        }}
                        QPushButton:hover {{
                            background-color: {INTERACTIVE_ELEMENT_COLOR_1};  /* Your desired background color when hovered */
                        }}
                        QPushButton:pressed {{
                            background-color: {INTERACTIVE_ELEMENT_COLOR_2};  /* Your desired background color when pressed */
                        }}
                    """
            self.userHeaderUi.employee_profile.setStyleSheet(buttonStyleSheetClicked)

        # Show the pop-up dialog
        self.popup_dialog.exec_()

    def submit_ticket(self):
        try:
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d_%H-%M-%S')
            print(formatted_time)

            if self.employee:
                empName = f"{self.employee.first_name} {self.employee.last_name}"
                empID = self.employee.employeeID
            else:
                empName = "Unknown"
                empID = "Unknown"

            subjectHeader = "Subject: "
            subject = self.subject_line_edit.text()
            descriptionHeader = "Description: "
            description = self.description_line_edit.toPlainText()
            print(description)
            database_tickets_directory = os.path.join(locust_directory, "Database", "DatabaseTickets")

            fileName = f"{database_tickets_directory}/{subject}_{str(formatted_time)}.txt"

            with open(fileName,
                      'w') as file:  # 'a' mode is for appending to the file, use 'w' to overwrite the file
                file.write("Timestamp: " + formatted_time + '\n')
                file.write("Employee Name: " + empName + '\n')
                file.write("Employee ID: " + empID + '\n')
                file.write(subjectHeader + subject + '\n')
                file.write(descriptionHeader + description + '\n')
                file.write('-' * 40 + '\n')  # Add a separator line for clarity

            self.subject_line_edit.clear()
            self.description_line_edit.clear()


        except Exception as e:
            print(f"Error: {e}")

    def updateUser(self, user):
        picture = self.scanInfoWidgetUi.picture
        name = self.scanInfoWidgetUi.name
        gender = self.scanInfoWidgetUi.gender
        id = self.scanInfoWidgetUi.id
        company = self.scanInfoWidgetUi.company
        title = self.scanInfoWidgetUi.title


        if user:
            pixmap_path = os.path.join(locust_directory, "Database", "DatabaseIndirectUsers", "photos")
            pixmap_path_ = f"{pixmap_path}/{user.photos}"
            new_pixmap = QPixmap(pixmap_path_)
            picture.setPixmap(new_pixmap.scaled(150, 150))
            name.setText(f"{user.first_name} {user.last_name}")
            gender.setText(user.gender)
            id.setText(user.id)
            company.setText(user.company)
            title.setText(user.title)
        if not user:
            pixmap_path = os.path.join(locust_directory, "GUI", "Picture", "file.jpg")
            new_pixmap = QPixmap(pixmap_path)
            picture.setPixmap(new_pixmap.scaled(150, 150))
            name.setText("")
            gender.setText("")
            id.setText("")
            company.setText("")
            title.setText("")
        if user == None:
            pixmap_path = os.path.join(locust_directory, "GUI", "Picture", "file.jpg")
            new_pixmap = QPixmap(pixmap_path)
            picture.setPixmap(new_pixmap.scaled(150, 150))
            name.setText("Unknown")
            gender.setText("Unknown")
            id.setText("Unknown")
            company.setText("Unknown")
            title.setText("Unknown")

    def acceptHandle(self):
        try:
            if self.employee:
                e = self.employee.get_special_id()
            else:
                e = "Unknown"

            user = self.current_user
            current_time = datetime.now()
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
            data_to_append = [formatted_time,
                              e,
                              user.id,
                              user.first_name,
                              user.last_name,
                              user.company,
                              user.title]


            log_csv_path = os.path.join(locust_directory, "Database", "DatabaseLogs", "log.csv")

            with open(log_csv_path, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(data_to_append)

            #Connecting to the board
            board = Arduino("/dev/cu.usbmodem14201")
            # RBG LED PIN
            red_pin = 10
            green_pin = 9
            blue_pin = 6

            # Set up the RGB LED
            board.digital[red_pin].mode = pyfirmata.PWM
            board.digital[green_pin].mode = pyfirmata.PWM
            board.digital[blue_pin].mode = pyfirmata.PWM

            def set_rgb_color(red, green, blue):
                board.digital[red_pin].write(red / 255)
                board.digital[green_pin].write(green / 255)
                board.digital[blue_pin].write(blue / 255)

            set_rgb_color(0, 255, 0)
            time.sleep(2)
            set_rgb_color(0,0,0)
            print("Test")


            self.scan_handle_label.setText("Access Granted")
            self.timer.start(5000)

        except:
            print("error")

    def rejectHandle(self):
        # Connecting to the board
        board = Arduino("/dev/cu.usbmodem14201")
        # RBG LED PIN
        red_pin = 10
        green_pin = 9
        blue_pin = 6

        # Set up the RGB LED
        board.digital[red_pin].mode = pyfirmata.PWM
        board.digital[green_pin].mode = pyfirmata.PWM
        board.digital[blue_pin].mode = pyfirmata.PWM

        def set_rgb_color(red, green, blue):
            board.digital[red_pin].write(red / 255)
            board.digital[green_pin].write(green / 255)
            board.digital[blue_pin].write(blue / 255)

        set_rgb_color(255, 0, 0)
        time.sleep(2)
        set_rgb_color(0, 0, 0)
        print("Test")
        self.scan_handle_label.setText("Access Denied")
        self.timer.start(5000)

    def updateLabel(self):
        self.scan_handle_label.setText("")
        self.timer.stop()

class Ui_scanInfo(object):
    def setupUi(self, scanInfo):
        self.labelStyle = f"color: {SIDEBAR_TEXT_COLOR}; font: 75 {BUTTON_LABEL_SIZE} '{FONT}'; padding-left: 10px;"
        self.fieldStyle = f'background-color: white; padding: 5px; border: 1px solid black; color:black'
        scanInfo.setStyleSheet(u"background-color:transparent;")

        def setup_main_layout():
            self.mainLayout = QVBoxLayout(scanInfo)
            self.mainLayout.setSpacing(5)
            self.mainLayout.setContentsMargins(0, 0, 0, 0)

            def setup_picture_container():
                self.pictureContainer = QFrame(scanInfo)
                self.pictureLayout = QVBoxLayout(self.pictureContainer)
                self.pictureLayout.setSpacing(5)
                self.pictureLayout.setContentsMargins(5, 5, 5, 5)

                def setup_picture():
                    self.picture = QLabel()
                    pixmap_path = os.path.join(locust_directory, "GUI", "Picture", "file.jpg")
                    self.picturePixmap = QPixmap(pixmap_path)
                    self.picture.setPixmap(self.picturePixmap.scaled(150, 150))
                    self.picture.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
                    self.picture.setMaximumHeight(150)
                    self.pictureLayout.addWidget(self.picture, 0, Qt.AlignHCenter)
                setup_picture()
                self.mainLayout.addWidget(self.pictureContainer)
            setup_picture_container()

            def setup_info_container():
                self.infoContainer = QFrame(scanInfo)
                self.infoContainer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                self.infoLayout = QFormLayout(self.infoContainer)
                self.infoLayout.setHorizontalSpacing(10)
                self.infoLayout.setVerticalSpacing(5)
                self.infoLayout.setContentsMargins(5, 5, 5, 5)
                self.infoLayout.setLabelAlignment(Qt.AlignLeft)  # Ensure labels are right-aligned
                self.infoLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

                def setup_name_label():
                        self.nameLabel = QLabel("Name: ")
                        self.nameLabel.setStyleSheet(self.labelStyle)
                        self.nameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                        self.infoLayout.setWidget(0, QFormLayout.LabelRole, self.nameLabel)

                        self.name = QLabel(self.infoContainer)
                        self.name.setStyleSheet(self.fieldStyle)
                        self.name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                        self.infoLayout.setWidget(0, QFormLayout.FieldRole, self.name)
                setup_name_label()

                def setup_gender_label():
                    self.genderLabel = QLabel("Gender: ")
                    self.genderLabel.setStyleSheet(self.labelStyle)
                    self.genderLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.infoLayout.setWidget(1, QFormLayout.LabelRole, self.genderLabel)

                    self.gender = QLabel(self.infoContainer)
                    self.gender.setStyleSheet(self.fieldStyle)
                    self.gender.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.infoLayout.setWidget(1, QFormLayout.FieldRole, self.gender)
                setup_gender_label()

                def setup_id_label():
                    self.idLabel = QLabel("ID: ")
                    self.idLabel.setStyleSheet(self.labelStyle)
                    self.idLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.infoLayout.setWidget(2, QFormLayout.LabelRole, self.idLabel)

                    self.id = QLabel(self.infoContainer)
                    self.id.setStyleSheet(self.fieldStyle)
                    self.id.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.infoLayout.setWidget(2, QFormLayout.FieldRole, self.id)
                setup_id_label()

                def setup_company_label():
                    self.companyLabel = QLabel("Company: ")
                    self.companyLabel.setStyleSheet(self.labelStyle)
                    self.companyLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.infoLayout.setWidget(3, QFormLayout.LabelRole, self.companyLabel)

                    self.company = QLabel(self.infoContainer)
                    self.company.setStyleSheet(self.fieldStyle)
                    self.company.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.infoLayout.setWidget(3, QFormLayout.FieldRole, self.company)
                setup_company_label()

                def setup_title_label():
                    self.titleLabel = QLabel("Title: ")
                    self.titleLabel.setStyleSheet(self.labelStyle)
                    self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.infoLayout.setWidget(4, QFormLayout.LabelRole, self.titleLabel)

                    self.title = QLabel(self.infoContainer)
                    self.title.setStyleSheet(self.fieldStyle)
                    self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                    self.infoLayout.setWidget(4, QFormLayout.FieldRole, self.title)
                setup_title_label()

                for row in range(self.infoLayout.rowCount()):
                    label_item = self.infoLayout.itemAt(row, QFormLayout.LabelRole)
                    if label_item:
                        label_widget = label_item.widget()
                        label_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

                    # For each field, create a container QWidget with QVBoxLayout
                for row in range(self.infoLayout.rowCount()):
                    field_item = self.infoLayout.itemAt(row, QFormLayout.FieldRole)
                    if field_item:
                        field_widget = field_item.widget()
                        # Create the container widget and layout
                        container_widget = QWidget()
                        container_layout = QVBoxLayout(container_widget)
                        container_layout.setContentsMargins(0, 0, 0, 0)  # Remove any additional margins
                        container_layout.addWidget(field_widget)
                        container_layout.addStretch(1)
                        self.infoLayout.setWidget(row, QFormLayout.FieldRole, container_widget)

                self.mainLayout.addWidget(self.infoContainer)

                #self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
                #self.mainLayout.addItem(self.verticalSpacer_2)
            setup_info_container()

            def setup_button_container():
                self.buttonContainer = QFrame(scanInfo)
                self.buttonLayout = QHBoxLayout(self.buttonContainer)
                self.buttonLayout.setSpacing(5)
                self.buttonLayout.setObjectName(u"buttonLayout")
                self.buttonLayout.setContentsMargins(5, 5, 5, 5)

                def setup_accept_button():
                    self.acceptButton = self.create_button("Accept", "acceptButton",
                                                           "accept-circular-button-outline.png", "green")
                    self.buttonLayout.addWidget(self.acceptButton)
                setup_accept_button()

                def setup_reject_button():
                    self.rejectButton = self.create_button("Reject", "rejectButton",
                                                           "cross-button.png", "red")
                    self.buttonLayout.addWidget(self.rejectButton)
                setup_reject_button()

                self.mainLayout.addWidget(self.buttonContainer)
            setup_button_container()

            self.mainLayout.addSpacing(20)

            def setup_logout_container():
                self.logout_container = QFrame(scanInfo)

                self.logout_layout = QVBoxLayout(self.logout_container)
                self.logout_layout.setSpacing(5)
                self.logout_layout.setObjectName(u"buttonLayout")
                self.logout_layout.setContentsMargins(5, 5, 5, 5)

                def setup_logout_button():
                    self.logoutButton = self.create_button("Exit", "logoutButton", "sign-out-alt.png", "white")
                    self.logout_layout.addWidget(self.logoutButton)
                setup_logout_button()
                self.mainLayout.addWidget(self.logout_container)
            setup_logout_container()
        setup_main_layout()

    def create_button(self, text, objectName, iconPath, setColor):
        button = QPushButton()
        button.setObjectName(objectName)
        button.setText(f"{text}")

        path = os.path.join(locust_directory, "GUI", "buttonIcons")
        pixmap = QPixmap(f"{path}/{iconPath}")

        white_pixmap = QPixmap(pixmap.size())
        white_pixmap.fill(QColor('transparent'))  # Start with a transparent pixmap

        painter = QPainter(white_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)

        painter.fillRect(white_pixmap.rect(), QColor(setColor))
        painter.end()


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
                color: {SIDEBAR_TEXT_COLOR}; 
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
        logoWidget.setStyleSheet(BACKGROUND_COLOR_TRANSPARENT)

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

        icon_path = os.path.join(locust_directory, "GUI", "Icons", "7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")
        # Load the logo image and set it to the label
        pixmap = QPixmap(icon_path)
        self.logoImg.setPixmap(pixmap)
        self.logoLayout.addWidget(self.logoImg)  # Add the logo image to the layout

        # Initialize the label for the logo text
        self.logoLabel = QLabel("LocUST")
        self.logoLabel.setObjectName("logoLabel")
        self.logoLabel.setStyleSheet(f"font: 75 {TITLE_FONT_SIZE} '{FONT}'; color:{SIDEBAR_TEXT_COLOR};")
        self.logoLayout.addWidget(self.logoLabel)  # Add the logo text to the layout

class Ui_userHeaderWidget(object):
    def setupUi(self, userHeaderWidget):
        userHeaderWidget.setStyleSheet(BACKGROUND_COLOR_TRANSPARENT)

        self.user_header_layout = QHBoxLayout(userHeaderWidget)
        self.user_header_layout.setSpacing(20)
        self.user_header_layout.setObjectName(u"userHeaderLayout")
        self.user_header_layout.setContentsMargins(10, 10, 10, 10)

        buttonStyleSheet = f"""
            QPushButton {{
                border: none;
                border-radius: 20px;  /* Half of width and height to make it circular */
                background-color: {BUTTON_COLOR};  /* Your desired background color for the normal state */
            }}
            QPushButton:hover {{
                background-color: {INTERACTIVE_ELEMENT_COLOR_1};  /* Your desired background color when hovered */
            }}
            QPushButton:pressed {{
                background-color: {INTERACTIVE_ELEMENT_COLOR_2};  /* Your desired background color when pressed */
            }}
        """

        def setup_search_icon():
            self.search_icon = QPushButton(userHeaderWidget)
            search_icon_path = os.path.join(locust_directory, "GUI", "buttonIcons", "search.png")
            self.search_icon.setIcon(QIcon(search_icon_path))
            self.search_icon.setIconSize(QSize(18, 18))
            self.search_icon.setStyleSheet(buttonStyleSheet)
            self.search_icon.setFixedSize(40, 40)
            self.user_header_layout.addWidget(self.search_icon)

        setup_search_icon()

        def setup_search_bar():
            search_bar_style = f"""
                            QLineEdit {{
                                border: 1px solid {BORDERS_LINES_COLOR}; /* Light grey border */
                                border-radius: 12px; /* Rounded corners */
                                padding: 0 8px; /* Text padding */
                                background: {FIELD_BACKGROUND_COLOR}; /* White background */
                                selection-background-color: {INTERACTIVE_ELEMENT_COLOR_1}; /* Color when text is selected */
                                font-size: {BODY_SECONDARY_FONT_SIZE}; /* Adjust the font size as needed */
                                opacity: 0.5;
                            }}
                            QLineEdit::placeholder {{
                                color: {PLACEHOLDER_COLOR}; /* Replace with your placeholder text color */
                                font-style: italic;
                                opacity: 0.5;
                            }}
                            QLineEdit:focus {{
                                border: 2px solid {BORDERS_LINES_COLOR}; /* Highlighted border color when focused */

                            }}
                        """
            self.search_bar = QLineEdit(userHeaderWidget)
            self.search_bar.setFixedHeight(24)
            palette = self.search_bar.palette()
            palette.setColor(QPalette.PlaceholderText, QColor(PLACEHOLDER_COLOR))
            self.search_bar.setPalette(palette)
            self.search_bar.setStyleSheet(search_bar_style)
            self.search_bar.setFocusPolicy(Qt.NoFocus)
            self.search_bar.setPlaceholderText("Search...")
            self.user_header_layout.addWidget(self.search_bar)

        setup_search_bar()

        def setup_settings_button():
            self.settings_button = QPushButton(userHeaderWidget)
            settings_icon_path = os.path.join(locust_directory, "GUI", "buttonIcons", "settings.png")
            self.settings_button.setIcon(QIcon(settings_icon_path))
            self.settings_button.setIconSize(QSize(18, 18))
            self.settings_button.setStyleSheet(buttonStyleSheet)
            self.settings_button.setFixedSize(40, 40)
            self.user_header_layout.addWidget(self.settings_button)

        setup_settings_button()

        def setup_notification_button():
            self.notification_button = QPushButton(userHeaderWidget)
            bell_icon_path = os.path.join(locust_directory, "GUI", "buttonIcons", "bell.png")
            self.notification_button.setIcon(QIcon(bell_icon_path))  # Replace with your icon's path
            self.notification_button.setIconSize(QSize(18, 18))  # Icon size
            self.notification_button.setStyleSheet(buttonStyleSheet)
            self.notification_button.setFixedSize(40, 40)  # Adjust size as needed
            self.user_header_layout.addWidget(self.notification_button)

        setup_notification_button()

        def setup_employee_profile():
            self.employee_profile = QPushButton(userHeaderWidget)
            user_icon_path = os.path.join(locust_directory, "GUI", "buttonIcons", "user.png")
            self.employee_profile.setIcon(QIcon(user_icon_path))
            self.employee_profile.setIconSize(QSize(18, 18))  # Icon size, adjust as needed
            self.employee_profile.setStyleSheet(buttonStyleSheet)
            self.employee_profile.setFixedSize(40, 40)
            self.user_header_layout.addWidget(self.employee_profile)

        setup_employee_profile()

        def setup_employee_name():
            self.employee_name = QLabel(userHeaderWidget)
            self.employee_name.setText("None")
            self.employee_name.setStyleSheet(f"font: 75 {BODY_FONT_SIZE} '{FONT}'; color:{SECONDARY_FONT_COLOR};")
            self.user_header_layout.addWidget(self.employee_name)

            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(0.5)
            self.employee_name.setGraphicsEffect(opacity_effect)

        setup_employee_name()

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

        shape_predictor_path = os.path.join(locust_directory, "Database", "DatabaseDatFiles",
                                            "shape_predictor_68_face_landmarks.dat")

        #self.shape_predictor = dlib.shape_predictor("../Database/DatabaseDatFiles/shape_predictor_68_face_landmarks.dat")
        self.shape_predictor = dlib.shape_predictor(shape_predictor_path)
        #self.face_recognizer = dlib.face_recognition_model_v1("../Database/DatabaseDatFiles/dlib_face_recognition_resnet_model_v1.dat")
        face_recognition_path = os.path.join(locust_directory, "Database", "DatabaseDatFiles",
                                            "dlib_face_recognition_resnet_model_v1.dat")

        self.face_recognizer = dlib.face_recognition_model_v1(face_recognition_path)


        self.known_face_descriptors = self.load_known_face_descriptors()

    def init_webcam(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Unable to access the webcam.")
            return
        self.webcam_timer = QTimer(self)
        self.webcam_timer.timeout.connect(self.update_webcam_feed)
        self.webcam_timer.start(50)

    def load_known_face_descriptors(self):
        pickle_directory = os.path.join(locust_directory, "Database", "DatabaseIndirectUsers", "face_encodings")
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
                    for i in entitiesMain.getUsers():
                        if i.id == id:
                            face_names[-1] = f"{i.first_name} {i.last_name}"
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




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = FacialRecognitionWindow()
    mainWin.show()
    sys.exit(app.exec_())
