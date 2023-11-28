import csv
import os
import pickle
import sys
from datetime import datetime

import cv2
import dlib
import numpy as np
from PyQt5.QtCore import QSize, Qt, QTimer, pyqtSignal, QEvent
from PyQt5.QtGui import QPixmap, QIcon, QImage, QPalette, QColor, QPainter, \
    QTextOption
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFrame, QSizePolicy, QVBoxLayout, QPushButton, \
    QLineEdit, QGraphicsOpacityEffect, QSpacerItem, QTextEdit, \
    QFormLayout, QDialog
from PyQt5.QtWidgets import QLabel, QHBoxLayout
from collections import Counter
from Entities import entitiesMain
from Entities.entitiesMain import is_within_user_schedule

# Link to data base


FONT = "Copperplate"

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
        self.scan_handle_label = None
        self.window_manager = window_manager
        self.employee = employee
        self.setupUi()
        self.showFullScreen()

    def setupUi(self):

        self.noneStyle = "background-color: transparent; border: none; border-radius: 20px;"

        """ Set up the main window."""
        self.webcam_handler = WebcamHandler()
        self.central_widget = QWidget()
        self.centralLayout = QHBoxLayout(self.central_widget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)

        def setup_sidebar(add_to, stretch):
            """ Set up the sidebar."""
            self.sideBar = QFrame(self.central_widget)
            self.sideBar.setStyleSheet(f"background-color: {SIDEBAR_COLOR};")
            self.sidebarLayout = QVBoxLayout(self.sideBar)
            self.sidebarLayout.setSpacing(0)
            self.sidebarLayout.setContentsMargins(10, 0, 10, 0)

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

            add_to.addWidget(self.sideBar, stretch=stretch)
        setup_sidebar(self.centralLayout, 5)

        def setup_main_window(add_to, stretch):
            """ Set up the main window."""
            self.mainWindow = QFrame(self.central_widget)
            self.mainWindow.setStyleSheet(f"background-color: {MAIN_BACKGROUND_COLOR};")
            self.mainLayout = QVBoxLayout(self.mainWindow)
            self.buttonStyleSheet = f"""
                                QPushButton {{
                                    background-color: {BUTTON_COLOR};
                                    color: {TEXT_COLOR};
                                    border-style: outset;
                                    border-width: 2px;
                                    border-radius: 10px;
                                    border-color: {BORDERS_LINES_COLOR};
                                    font: bold {BODY_FONT_SIZE} "{FONT}";
                                    padding: 5px;
                                }}
                                QPushButton:pressed {{
                                    background-color: {INTERACTIVE_ELEMENT_COLOR_1};
                                    border-style: inset;
                                }}
                                QPushButton:hover:!pressed {{
                                    background-color: {INTERACTIVE_ELEMENT_COLOR_2};
                                }}

                            """

            def setup_header_widget(add_to, stretch):
                """ Set up the header widget."""
                self.userHeaderContainer = QWidget(self.mainWindow)
                self.userHeaderUi = Ui_userHeaderWidget()
                self.userHeaderUi.setupUi(self.userHeaderContainer)
                if self.employee:
                    self.userHeaderUi.employee_name.setText(f"{self.employee.first_name} {self.employee.last_name}")

                self.userHeaderUi.employee_profile.clicked.connect(self.show_popup_window)
                QApplication.instance().installEventFilter(self.central_widget)

                add_to.addWidget(self.userHeaderContainer, stretch=stretch)
            setup_header_widget(self.mainLayout, 1)

            def setup_display_container(add_to, stretch):
                """ Set up the display container."""
                self.displayContainer = QWidget(self.mainWindow)
                self.displayContainer.setObjectName("displayContainer")
                self.displayContainer.setStyleSheet(BACKGROUND_COLOR_TRANSPARENT)
                self.displayLayout = QVBoxLayout(self.displayContainer)
                add_to.addWidget(self.displayContainer, stretch=stretch)

                def setup_scan_container(add_to=None, stretch=None):
                    self.scan_container = QWidget()
                    self.scan_container.setStyleSheet(f"background-color:{CONTENT_CARD_BACKGROUND_COLOR}; "
                                                      f"border: 2px solid {BORDERS_LINES_COLOR};"
                                                      f"border-radius: 20px;")
                    self.scan_layout = QVBoxLayout(self.scan_container)
                    add_to.addWidget(self.scan_container)

                    def setup_scan_header_container(add_to=None, stretch=None):
                        self.scan_handle_widget = QWidget()
                        self.scan_handle_widget.setStyleSheet(self.noneStyle)
                        self.scan_handle_layout = QHBoxLayout(self.scan_handle_widget)
                        self.scan_handle_layout.addStretch(1)
                        self.scan_handle_label = QLabel("Scan Ready")
                        self.scan_handle_label.setAlignment(Qt.AlignCenter)
                        self.scan_handle_label.setStyleSheet(
                            f"color: {TEXT_COLOR}; font: 75 {SUBHEADER_FONT_SIZE} "
                            f"'{FONT}';")
                        self.scan_handle_layout.addWidget(self.scan_handle_label, 10)
                        self.scan_handle_layout.addStretch(1)
                        add_to.addWidget(self.scan_handle_widget, stretch=stretch)
                    setup_scan_header_container(self.scan_layout, 1)

                    def setup_face_recognition_webcam_display(add_to=None, stretch=None):
                        """ Set up the face recognition webcam display."""
                        self.webcam_handler.setUser.connect(self.setUser)
                        self.webcam_handler.user_updated.connect(self.updateUser)
                        self.webcam_handler.webcam_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

                        self.cam_container = QWidget()
                        self.cam_container.setStyleSheet(self.noneStyle)
                        self.cam_layout = QHBoxLayout(self.cam_container)
                        self.cam_layout.addStretch(1)
                        self.cam_layout.addWidget(self.webcam_handler, 10)
                        self.cam_layout.addStretch(1)
                        add_to.addWidget(self.cam_container, stretch=stretch)
                    setup_face_recognition_webcam_display(self.scan_layout, 10)

                    def setup_scan_button(add_to=None, stretch=None):
                        scan_button = QPushButton()
                        scan_button.setStyleSheet(self.buttonStyleSheet)
                        scan_button.setText("Scan")
                        scan_button.clicked.connect(self.start_scan)

                        # Set the fixed width of the button
                        button_width = 250
                        scan_button.setMinimumWidth(button_width)
                        scan_button.setMaximumWidth(button_width)

                        # Create a QHBoxLayout to center the button
                        button_layout = QHBoxLayout()
                        button_layout.addStretch()  # Add stretchable space on the left
                        button_layout.addWidget(scan_button)  # Add the button
                        button_layout.addStretch()  # Add stretchable space on the right

                        add_to.addLayout(button_layout, stretch=stretch)
                    setup_scan_button(self.scan_layout, 1)


                setup_scan_container(self.displayLayout)
            setup_display_container(self.mainLayout, 10)

            add_to.addWidget(self.mainWindow, stretch=stretch)
        setup_main_window(self.centralLayout, 20)

    def start_scan(self):
        self.scan_handle_label.setText("Scan in Progress..")
        self.clearUserContainer()
        self.webcam_handler.handle_timer("start")

        self.webcam_handler.toggle_face_recognition()

    def clearUserContainer(self):
        picture = self.scanInfoWidgetUi.picture
        name = self.scanInfoWidgetUi.name
        gender = self.scanInfoWidgetUi.gender
        id = self.scanInfoWidgetUi.id
        company = self.scanInfoWidgetUi.company
        title = self.scanInfoWidgetUi.title

        pixmap_path = os.path.join(locust_directory, "GUI", "Picture", "file.jpg")
        new_pixmap = QPixmap(pixmap_path)
        picture.setPixmap(new_pixmap.scaled(150, 150))
        name.setText("")
        gender.setText("")
        id.setText("")
        company.setText("")
        title.setText("")

    def setUser(self, user):
        """
        Set the current user.
        @param user: The user object.
        """
        self.current_user = user
        if user:
            pass
        if not user and not self.webcam_handler.start_scanning:
            self.scan_handle_label.setText("No Match Found")

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
            self.scan_handle_label.setText("Match Found")
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
            #self.scan_handle_label.setText("No Match Found")
            pixmap_path = os.path.join(locust_directory, "GUI", "Picture", "file.jpg")
            new_pixmap = QPixmap(pixmap_path)
            picture.setPixmap(new_pixmap.scaled(150, 150))
            name.setText("")
            gender.setText("")
            id.setText("")
            company.setText("")
            title.setText("")
        if user == None:
            self.scan_handle_label.setText("No Match Found")
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

            self.webcam_handler.handle_timer("start")
            self.scan_handle_label.setText("Scan Ready")
            self.clearUserContainer()

        except:
            print("error")
            self.webcam_handler.handle_timer("start")
            self.scan_handle_label.setText("Scan Ready")
            self.clearUserContainer()

    def rejectHandle(self):
        self.webcam_handler.handle_timer("start")
        self.scan_handle_label.setText("Scan Ready")
        self.clearUserContainer()

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

        #self.face_recognition_window = FacialRecognitionWindow()


        db = "Database"
        dbf = "DatabaseDatFiles"

        shape_predictor_path = os.path.join(locust_directory, db, dbf, "shape_predictor_68_face_landmarks.dat")
        self.shape_predictor = dlib.shape_predictor(shape_predictor_path)

        face_recognition_path = os.path.join(locust_directory, db, dbf, "dlib_face_recognition_resnet_model_v1.dat")
        self.face_recognizer = dlib.face_recognition_model_v1(face_recognition_path)

        self.known_face_descriptors = self.load_known_face_descriptors()

        self.recognize_faces_enabled = False

        self.scanner_line_position = 0
        self.start_scanning = False
        self.glow_effect_finished = False

    def toggle_face_recognition(self):
        self.scanner_line_position = 0  # Reset scanner line position
        self.start_scanning = True  # Start scanning
        """Toggle the face recognition process on and off."""
        self.recognize_faces_enabled = not self.recognize_faces_enabled

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

    # def recognize_faces(self, frame, tolerance=50):
    #
    #
    #     frame_for_landmarks = frame.copy()
    #
    #     # Detect faces in the frame
    #     face_locations = self.face_detector(frame)
    #     if not face_locations:
    #         return frame, []
    #
    #     face_match_percentages = []
    #
    #     for face_location in face_locations:
    #         # Detect facial landmarks
    #         shape = self.shape_predictor(frame, face_location)
    #         landmarks = np.array([(point.x, point.y) for point in shape.parts()])
    #
    #         # Define connections between landmarks
    #         # Define connections between landmarks
    #         connections = [
    #             # # Jaw line
    #             # *zip(range(0, 16), range(1, 17)),
    #             # # Right eyebrow
    #             # *zip(range(17, 21), range(18, 22)),
    #             # # Left eyebrow
    #             # *zip(range(22, 26), range(23, 27)),
    #             # # Nose bridge
    #             # *zip(range(27, 30), range(28, 31)),
    #             # # Lower nose
    #             # *zip(range(30, 35), range(31, 36)),
    #             # # Right eye
    #             # *zip(range(36, 41), range(37, 42)), (36, 41),
    #             # # Left eye
    #             # *zip(range(42, 47), range(43, 48)), (42, 47),
    #             # # Outer lip
    #             # *zip(range(48, 59), range(49, 60)), (48, 59),
    #             # # Inner lip
    #             # *zip(range(60, 67), range(61, 68)), (60, 67),
    #             # # Additional lines like in the image provided
    #             # (27, 21),  # Line from nose bridge to right eyebrow
    #             # (27, 22),  # Line from nose bridge to left eyebrow
    #             # (30, 35),  # Line from lower nose to top of lip
    #             # (48, 54),
    #             (26, 30),  # Line from lower nose to top of lip
    #             (26, 34),
    #             # Line from mouth corner to opposite mouth corner
    #
    #             # ... (other additional lines as seen in the image)
    #         ]
    #
    #         # Draw lines between landmarks
    #         for start, end in connections:
    #             cv2.line(frame_for_landmarks, landmarks[start], landmarks[end], (255, 255, 255), 1)
    #
    #         # Optionally draw points on landmarks
    #         for (x, y) in landmarks:
    #             cv2.circle(frame_for_landmarks, (x, y), 1, (255, 255, 255), -1)
    #
    #         # Draw bounding box with corners around the face
    #         border_color = (255, 255, 0)  # Yellow color for the corners
    #         border_thickness = 2
    #         corner_length = 20
    #
    #         # Calculate coordinates for corners
    #         left, top, right, bottom = (face_location.left(), face_location.top(),
    #                                     face_location.right(), face_location.bottom())
    #
    #         # Top left corner
    #         cv2.line(frame_for_landmarks, (left, top), (left + corner_length, top), border_color, border_thickness)
    #         cv2.line(frame_for_landmarks, (left, top), (left, top + corner_length), border_color, border_thickness)
    #         # Top right corner
    #         cv2.line(frame_for_landmarks, (right, top), (right - corner_length, top), border_color, border_thickness)
    #         cv2.line(frame_for_landmarks, (right, top), (right, top + corner_length), border_color, border_thickness)
    #         # Bottom left corner
    #         cv2.line(frame_for_landmarks, (left, bottom), (left + corner_length, bottom), border_color, border_thickness)
    #         cv2.line(frame_for_landmarks, (left, bottom), (left, bottom - corner_length), border_color, border_thickness)
    #         # Bottom right corner
    #         cv2.line(frame_for_landmarks, (right, bottom), (right - corner_length, bottom), border_color, border_thickness)
    #         cv2.line(frame_for_landmarks, (right, bottom), (right, bottom - corner_length), border_color, border_thickness)
    #
    #
    #         # Perform face recognition using the original frame (not the one with landmarks)
    #         face_descriptor = self.face_recognizer.compute_face_descriptor(frame, shape)
    #         match_found, best_match = False, None
    #
    #         # Compare with known faces
    #         for name, known_descriptors in self.known_face_descriptors.items():
    #             for known_descriptor in known_descriptors:
    #                 distance = np.linalg.norm(np.array(known_descriptor) - np.array(face_descriptor))
    #                 match_percent = round(max(0, 1 - distance) * 100, 2)
    #
    #                 if match_percent >= tolerance:
    #                     face_match_percentages.append((name, match_percent))
    #                     if not best_match or match_percent > best_match[1]:
    #                         best_match = (name, match_percent)
    #                     match_found = True
    #
    #         # Draw rectangle and add text
    #         left, top, right, bottom = face_location.left(), face_location.top(), face_location.right(), face_location.bottom()
    #         color, text = (255, 0, 0), "Unknown"
    #         if match_found:
    #             color, text = (0, 128, 0), best_match[0]
    #             user = next((i for i in entitiesMain.getUsers() if i.id == best_match[0].split('_')[0]), None)
    #             if user:
    #                 text = f"{user.first_name} {user.last_name}"
    #                 self.user_updated.emit(user)
    #                 self.setUser.emit(user)
    #         cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
    #         cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    #
    #     return frame_for_landmarks, face_match_percentages
    def recognize_faces(self, frame, tolerance=50):
        frame_for_landmarks = frame.copy()



        # Detect faces in the frame
        face_locations = self.face_detector(frame)
        if not face_locations:
            return frame, []

        face_match_percentages = []

        for face_location in face_locations:
            # Detect facial landmarks
            shape = self.shape_predictor(frame, face_location)
            landmarks = np.array([(point.x, point.y) for point in shape.parts()])

            # Estimate top of the forehead based on the eyebrows and nose
            mid_between_eyebrows = (landmarks[21] + landmarks[22]) // 2
            vertical_distance = landmarks[30][1] - mid_between_eyebrows[1]
            top_forehead_point = (mid_between_eyebrows[0], mid_between_eyebrows[1] - vertical_distance)

            # Estimate additional forehead points
            additional_forehead_points = [
                (landmarks[17][0], top_forehead_point[1]),  # Left forehead point
                (landmarks[26][0], top_forehead_point[1]),  # Right forehead point
                # You can add more points here if needed
            ]

            # Create an 'X' shape by estimating its four points
            x_shape_points = [
                (top_forehead_point[0] - 20, top_forehead_point[1] + 20),  # Top left of the 'X'
                (top_forehead_point[0] + 20, top_forehead_point[1] + 20),  # Top right of the 'X'
                (top_forehead_point[0] - 20, top_forehead_point[1] - 20),  # Bottom left of the 'X'
                (top_forehead_point[0] + 20, top_forehead_point[1] - 20),  # Bottom right of the 'X'
            ]
            left_forehead_point = (landmarks[0][0], top_forehead_point[1])  # Aligned with landmark 1
            right_forehead_point = (landmarks[16][0], top_forehead_point[1])  # Aligned with landmark 17

            cheek_points = []

            # Right cheek points
            right_eye_outer_corner = landmarks[36]
            bottom_of_nose = landmarks[33]
            right_cheek_mid_vertical = (right_eye_outer_corner[1] + bottom_of_nose[1]) // 2
            cheek_points.append((right_eye_outer_corner[0], right_eye_outer_corner[1]))  # Level with the eye
            cheek_points.append((right_eye_outer_corner[0], right_cheek_mid_vertical))  # Midway point
            cheek_points.append((right_eye_outer_corner[0], bottom_of_nose[1]))  # Level with the bottom of the nose

            # Left cheek points
            left_eye_outer_corner = landmarks[45]
            left_cheek_mid_vertical = (left_eye_outer_corner[1] + bottom_of_nose[1]) // 2
            cheek_points.append((left_eye_outer_corner[0], left_eye_outer_corner[1]))  # Level with the eye
            cheek_points.append((left_eye_outer_corner[0], left_cheek_mid_vertical))  # Midway point
            cheek_points.append((left_eye_outer_corner[0], bottom_of_nose[1]))  # Level with the bottom of the nose

            # Combine the original landmarks with the additional forehead, 'X' points, and new cheek points
            landmarks = np.concatenate(
                (landmarks, [top_forehead_point] + additional_forehead_points + x_shape_points + cheek_points), axis=0)

            # Define connections between landmarks
            connections = [
                # Example connections - you can modify these as needed
                #mouth
                (8, 58),
                (48, 58),
                (48, 50),
                (50, 51),
                (51, 52),
                (52, 53),
                (53, 54),
                (54, 56),
                (8, 56),


                #Bottom Jaw
                (4, 6),
                (6, 7),
                (7, 8),
                (8, 9),
                (9, 10),
                (10, 12),


                # Nose
                (27, 28),
                (28, 29),
                (29, 30),
                (30, 33),

                (33, 31),
                (33, 35),

                (48, 4),
                (54, 12),

                (58, 6),
                (56, 10),

                (3, 31),
                (35, 13),
                (3, 17),
                (17,0),
                (3,27),



                # (27, 79),
                # (79, 14),
                # (3, 76),
                # (27, 76),
                # (35, 79),

                # # Nose
                # (27, 31),
                # (27, 35),
                # (31, 33),
                # (33, 35),
                #
                # (31, 30),
                # (30, 35),
                #
                # (10,57),
                # (6,57),
                #
                # #jaw to nose
                #
                # (12, 35),
                # (14, 35),
                #
                # (4, 31),
                # (2, 31),
                #
                # # (2, 27),
                # # (14, 27)
                # (54, 12),
                # (48, 4),



            ]
            # connections = [
            #     # Jawline
            #     (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8),
            #     (8, 9), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16),
            #     # Right eyebrow
            #     (17, 18), (18, 19), (19, 20), (20, 21),
            #     # Left eyebrow
            #     (22, 23), (23, 24), (24, 25), (25, 26),
            #     # Nose bridge
            #     (27, 28), (28, 29), (29, 30),
            #     # Lower nose
            #     (30, 31), (31, 32), (32, 33), (33, 34), (34, 35),
            #     # Right eye
            #     (36, 37), (37, 38), (38, 39), (39, 40), (40, 41), (41, 36),
            #     # Left eye
            #     (42, 43), (43, 44), (44, 45), (45, 46), (46, 47), (47, 42),
            #     # Outer lip
            #     (48, 49), (49, 50), (50, 51), (51, 52), (52, 53), (53, 54), (54, 55), (55, 56),
            #     (56, 57), (57, 58), (58, 59), (59, 48),
            #     # Inner lip
            #     (60, 61), (61, 62), (62, 63), (63, 64), (64, 65), (65, 66), (66, 67), (67, 60),
            #     # You should add more connections based on the additional points you've estimated.
            #     # For example, for the top forehead point (which might be index 68 if it's the first extra point):
            #     (17, 68), (26, 68),
            #     # ...and so on for other additional points you have.
            # ]

            # Draw lines between landmarks
            # for start, end in connections:
            #     cv2.line(frame_for_landmarks, landmarks[start], landmarks[end], (255, 69, 0), 1)

            # selected_landmarks_indices = [0, 4, 6, 8, 10, 12, 16, 27, 31, 35]
            # # Draw selected points on landmarks
            # for i in selected_landmarks_indices:
            #     x, y = landmarks[i]
            #     cv2.circle(frame_for_landmarks, (x, y), 1, (255, 255, 255), -1)
            #     #cv2.putText(frame_for_landmarks, str(i), (x + 2, y + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0), 1)  # Label the point

            # for i, (x, y) in enumerate(landmarks):
            #     cv2.circle(frame_for_landmarks, (x, y), 1, (255, 69, 0), -1)
            #     cv2.putText(frame_for_landmarks, str(i), (x + 2, y + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (255, 0, 0), 1)





            # Perform face recognition using the original frame (not the one with landmarks)
            face_descriptor = self.face_recognizer.compute_face_descriptor(frame, shape)
            match_found, best_match = False, None

            # Compare with known faces
            for name, known_descriptors in self.known_face_descriptors.items():
                for known_descriptor in known_descriptors:
                    distance = np.linalg.norm(np.array(known_descriptor) - np.array(face_descriptor))
                    match_percent = round(max(0, 1 - distance) * 100, 2)

                    if match_percent >= tolerance:
                        face_match_percentages.append((name, match_percent))
                        if not best_match or match_percent > best_match[1]:
                            best_match = (name, match_percent)
                        match_found = True


            border_color, text = (255, 0, 0), "Unknown"
            if match_found:

                border_color, text = (0, 255, 0), best_match[0]
                user = next((i for i in entitiesMain.getUsers() if i.id == best_match[0].split('_')[0]), None)
                if user:
                    text = f"{user.first_name} {user.last_name}"
                    self.user_updated.emit(user)
                    self.setUser.emit(user)

                    is_within_schedule = is_within_user_schedule(user.id)
                    if not is_within_schedule:
                        border_color, text = (255, 255, 0), best_match[0]
                    else:
                        border_color, text = (0, 255, 0), best_match[0]






            border_thickness = 2
            corner_length = 20
            expand_margin = 10  # Pixels to expand the box by on each side

            # Calculate coordinates for expanded corners
            left, top, right, bottom = (face_location.left() - expand_margin,
                                        face_location.top() - expand_margin,
                                        face_location.right() + expand_margin,
                                        face_location.bottom() + expand_margin)

            # Top left corner
            cv2.line(frame_for_landmarks, (left, top), (left + corner_length, top), border_color, border_thickness)
            cv2.line(frame_for_landmarks, (left, top), (left, top + corner_length), border_color, border_thickness)
            # Top right corner
            cv2.line(frame_for_landmarks, (right, top), (right - corner_length, top), border_color, border_thickness)
            cv2.line(frame_for_landmarks, (right, top), (right, top + corner_length), border_color, border_thickness)
            # Bottom left corner
            cv2.line(frame_for_landmarks, (left, bottom), (left + corner_length, bottom), border_color,
                     border_thickness)
            cv2.line(frame_for_landmarks, (left, bottom), (left, bottom - corner_length), border_color,
                     border_thickness)
            # Bottom right corner
            cv2.line(frame_for_landmarks, (right, bottom), (right - corner_length, bottom), border_color,
                     border_thickness)
            cv2.line(frame_for_landmarks, (right, bottom), (right, bottom - corner_length), border_color,
                     border_thickness)

            # cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            #cv2.putText(frame, text, (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return frame_for_landmarks, face_match_percentages
    def update_webcam_feed(self):
        ret, frame = self.cap.read()

        if ret:
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Glow effect logic
            glow_layer = np.zeros((rgb_frame.shape[0], rgb_frame.shape[1]), dtype=np.uint8)

            if self.start_scanning:
                # Configure the glow effect
                line_color = 255  # White color
                line_thickness = 2
                glow_thickness = 15

                # Draw the scanning line
                cv2.line(glow_layer, (0, self.scanner_line_position),
                         (rgb_frame.shape[1], self.scanner_line_position),
                         line_color, line_thickness)

                cv2.line(glow_layer, (0, self.scanner_line_position),
                         (rgb_frame.shape[1], self.scanner_line_position),
                         line_color, glow_thickness)

                # Apply Gaussian blur for the glow effect
                glow_layer = cv2.GaussianBlur(glow_layer, (0, 0), sigmaX=7, sigmaY=7)

                # Convert to 3 channels
                glow_layer = cv2.cvtColor(glow_layer, cv2.COLOR_GRAY2BGR)
                glow_layer = cv2.normalize(glow_layer, None, alpha=0, beta=255,
                                           norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

                # Blend with the original frame
                rgb_frame = cv2.add(rgb_frame, glow_layer)

                # Update the scanner line position
                self.scanner_line_position += 5  # Adjust the speed of the scanner line here
                if self.scanner_line_position > rgb_frame.shape[0]:
                    self.start_scanning = False
                    self.glow_effect_finished = True

            # Face recognition logic
            if not self.start_scanning and self.glow_effect_finished and self.recognize_faces_enabled:
                frame_with_faces, face_names = self.recognize_faces(rgb_frame)
                QTimer.singleShot(250, lambda: self.handle_timer('stop'))

            else:
                frame_with_faces = rgb_frame
                face_names = []

            # Update the webcam feed on the GUI
            height, width, channel = frame_with_faces.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame_with_faces.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            pixmap = pixmap.scaled(self.webcam_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.webcam_label.setPixmap(pixmap)
            self.webcam_label.setAlignment(Qt.AlignCenter)

            # Emit signals if face recognition is performed
            if self.recognize_faces_enabled and not face_names:
                self.user_updated.emit(False)
                self.setUser.emit(None)

    def handle_timer(self, action):
        if action == "stop" and self.webcam_timer.isActive():
            self.webcam_timer.stop()

        if action == "start" and not self.webcam_timer.isActive():
            self.webcam_timer.start(50)
            self.recognize_faces_enabled = False
            #self.face_recognition_window.scan_handle_label.setText("Scan Ready")
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
