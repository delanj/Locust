import os
import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, \
    QHBoxLayout, QGraphicsDropShadowEffect, QSizePolicy, QStyle
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPainter, QFontDatabase, QFont, QTextCursor
from PyQt5.QtCore import Qt, QSize

from Entities import entitiesMain as db
from GUI import dashboard


class LoginWindow(QMainWindow):

    # Constants
    FONT_FAMILY = "Copperplate"
    FONT_COLOR = "#E0E0E0"
    MAIN_BACKGROUND_COLOR = "#FAFAFA"
    BACKGROUND_COLOR = "#333940"
    BUTTON_COLOR = "#B0BEC5"
    BUTTON_TEXT_COLOR = "#4A4A4A"
    BORDER_COLOR = "#E0E0E0"
    BUTTON_HOVER_COLOR = "rgb(190, 190, 190)"
    BUTTON_PRESSED_COLOR = "rgb(220, 220, 220)"
    ICON_COLOR = "white"

    def __init__(self, window_manager):
        """ Initialize the main login window. """
        super().__init__()
        self.window_manager = window_manager
        logging.basicConfig(level=logging.INFO)
        #self.loadCustomFont()
        self.initUI()

    def initUI(self):
        """ Initialize the main user interface. """
        self.setWindowTitle("Login")
        self.showFullScreen()
        self.centralWidget = QWidget(self)
        self.centralWidget.setStyleSheet(f"background-color:{self.MAIN_BACKGROUND_COLOR};")
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)
        self.layout.addWidget(self.createLoginWidget(), alignment=Qt.AlignCenter)

    def loadCustomFont(self):
        # Try to load the custom font
        font_id = QFontDatabase.addApplicationFont("../GUI/font/Aquire-BW0ox.otf")

        if font_id != -1:
            # Get the font family name from the loaded font
            font_info = QFontDatabase.applicationFontFamilies(font_id)
            print(font_info)

            if font_info:
                custom_font_family = font_info[0]  # Use the first font family name
            else:
                custom_font_family = "Copperplate"  # Use a fallback font name in case of failure
        else:
            custom_font_family = "Copperplate"  # Use a fallback font name if loading failed

        self.FONT_FAMILY = custom_font_family

    def createLoginWidget(self):
        """ Creates and returns the main login widget. """
        loginWidget = QWidget()
        loginWidget.setFixedSize(350, 600)
        loginWidget.setStyleSheet(f"background-color: {self.BACKGROUND_COLOR}; border-radius: 30px;")
        loginWidget.setGraphicsEffect(self.createShadowEffect())

        loginLayout = QVBoxLayout(loginWidget)
        loginLayout.setAlignment(Qt.AlignCenter)
        loginLayout.addWidget(self.createLogoLabel())
        loginLayout.addWidget(self.createImageLabel())
        self.invalidLabel = self.createInvalidLoginLabel()
        loginLayout.addWidget(self.invalidLabel)
        loginLayout.addSpacing(0)

        def setup_username_line():
            """ Setup the username line."""
            self.usernameEdit = self.createLineEdit("Username")
            loginLayout.addWidget(self.usernameEdit)
            loginLayout.addSpacing(30)

        setup_username_line()

        def setup_password_line():
            """ Setup the password line."""
            self.passwordLayout = QHBoxLayout()

            self.passwordEdit = self.createLineEdit("Password", True)
            current_file_directory = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_file_directory, "buttonIcons", "show.png")

            self.togglePasswordButton = self.create_button(image_path)
            self.togglePasswordButton.setCursor(Qt.PointingHandCursor)
            self.togglePasswordButton.setFixedSize(20, 20)
            self.togglePasswordButton.clicked.connect(self.toggle_password_visibility)

            self.passwordLayout.addWidget(self.passwordEdit)
            self.passwordLayout.addWidget(self.togglePasswordButton)

            loginLayout.addLayout(self.passwordLayout)

            self.togglePasswordButton.setParent(self.passwordEdit)
            buttonSize = self.togglePasswordButton.size()
            editWidth = self.passwordEdit.width()
            self.togglePasswordButton.move(editWidth - buttonSize.width(), 0)
        setup_password_line()

        def setup_buttons():
            """ Setup the buttons."""
            loginLayout.addSpacing(20)
            loginLayout.addLayout(self.createButtonLayout())
            loginLayout.addSpacing(20)
        setup_buttons()

        def setup_copy_right():
            """ Setup the copy right label."""
            loginLayout.addWidget(self.createCopyrightLabel())
        setup_copy_right()

        return loginWidget

    def toggle_password_visibility(self):
        """ Toggle the password visibility."""
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        if self.togglePasswordButton.isChecked():
            image_path = os.path.join(current_file_directory, "buttonIcons", "show.png")
            self.passwordEdit.setEchoMode(QLineEdit.Normal)
            self.setButtonIcon(self.togglePasswordButton, image_path)
        else:
            image_path = os.path.join(current_file_directory, "buttonIcons", "show.png")
            self.passwordEdit.setEchoMode(QLineEdit.Password)
            self.setButtonIcon(self.togglePasswordButton, image_path)

    def setButtonIcon(self, button, iconPath):
        """
        Set the button icon.
        @param button: Button to set icon for.
        @param iconPath: Path to icon.
        """
        pixmap = QPixmap(iconPath)
        white_pixmap = QPixmap(pixmap.size())
        white_pixmap.fill(QColor('transparent'))

        painter = QPainter(white_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(white_pixmap.rect(), QColor(self.ICON_COLOR))
        painter.end()

        button.setIcon(QIcon(white_pixmap))

    def create_button(self, iconPath):
        """
        Create and return a button with an icon.
        @param iconPath: Path to icon.
        """
        button = QPushButton()
        button.setCheckable(True)
        button.setObjectName("togglePasswordVisibility")

        # Load and process the icon
        pixmap = QPixmap(iconPath)
        white_pixmap = QPixmap(pixmap.size())
        white_pixmap.fill(QColor('transparent'))

        painter = QPainter(white_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(white_pixmap.rect(), QColor(self.ICON_COLOR))
        painter.end()

        button.setIcon(QIcon(white_pixmap))
        button.setIconSize(QSize(20, 20))
        button.setStyleSheet("QPushButton { border: none; }")
        button.setMinimumHeight(40)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        return button


    def createShadowEffect(self):
        """ Creates and returns a shadow effect."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(3, 3)
        return shadow

    def createLogoLabel(self):
        """ Creates and returns the logo label. """
        label = QLabel("LocUST")
        label.setStyleSheet(f'font-size: 56pt; font-family: "{self.FONT_FAMILY}"; color: {self.FONT_COLOR}; padding: 6px; min-width: 10;')
        label.setFixedHeight(75)
        label.setAlignment(Qt.AlignCenter)
        return label

    def createImageLabel(self):
        """ Creates and returns the image label."""
        imageLabel = QLabel(self)
        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_file_directory, "Icons", "7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")
        pixmap = QPixmap(image_path)
        imageLabel.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imageLabel.setAlignment(Qt.AlignCenter)
        imageLabel.setFixedHeight(225)
        return imageLabel

    def createInvalidLoginLabel(self):
        """ Creates and returns the invalid login label."""
        invalidLabel = QLabel("")
        invalidLabel.setAlignment(Qt.AlignCenter)
        invalidLabel.setStyleSheet(f'color: {self.FONT_COLOR}; font: 75 12px "{self.FONT_FAMILY}";')
        return invalidLabel

    def createLineEdit(self, placeholder, isPassword=False):
        """
        Create and return line edit.
        @param placeholder: Placeholder text for line edit.
        @param isPassword: Boolean value to determine if line edit is a password field.
        """

        lineEdit = QLineEdit()
        lineEdit.setPlaceholderText(placeholder)
        lineEdit.setStyleSheet(self.lineEditStylesheet())
        lineEdit.setFixedWidth(250)
        lineEdit.setFixedHeight(20)
        lineEdit.setAttribute(Qt.WA_MacShowFocusRect, 0)
        if isPassword:
            lineEdit.setEchoMode(QLineEdit.Password)
        return lineEdit

    def createButtonLayout(self):
        """Create and return button layout."""
        layout = QHBoxLayout()
        loginButton = QPushButton("Login")
        loginButton.setFixedWidth(150)
        loginButton.setFixedHeight(40)
        loginButton.setStyleSheet(self.buttonStylesheet())
        loginButton.clicked.connect(self.login)
        layout.addWidget(loginButton)
        return layout

    def createCopyrightLabel(self):
        """Create and return copy right label."""
        copyrightLabel = QLabel("©2023 LocUST.inc")
        copyrightLabel.setStyleSheet(f'color: {self.FONT_COLOR}; font: 75 12px "{self.FONT_FAMILY}";')
        copyrightLabel.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        return copyrightLabel

    def buttonStylesheet(self):
        """Create and return button stylesheet."""
        return f'''
               QPushButton {{
                   background-color: {self.BUTTON_COLOR};
                   color: {self.BUTTON_TEXT_COLOR};
                   border-style: outset;
                   border-width: 1px;
                   border-radius: 10px;
                   border-color: {self.BORDER_COLOR};
                   font: bold 14px "{self.FONT_FAMILY}";
                   padding: 5px;
               }}
               QPushButton:pressed {{
                   background-color: {self.BUTTON_PRESSED_COLOR};
                   border-style: inset;
               }}
               QPushButton:hover:!pressed {{
                   background-color: {self.BUTTON_HOVER_COLOR};
               }}
           '''

    def lineEditStylesheet(self):
        """Create and return line edit stylesheet."""
        return f'''
               font: 75 16px "{self.FONT_FAMILY}"; 
               background: transparent; 
               border: 1px solid transparent; 
               border-bottom: 1px solid {self.BORDER_COLOR}; 
               selection-background-color: transparent; 
               outline: none; 
               color: {self.FONT_COLOR};
           '''

    def login(self):
        """ Attempt to log in with provided credentials. """
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()

        if not username or not password:
            self.invalidLabel.setText("Please enter both username and password.")
            return

        try:
            username = self.usernameEdit.text()
            password = self.passwordEdit.text()

            login_successful = False
            for i in db.getEmployees():
                if username == i.get_special_id() and password == i.passcode:
                    employee = i
                    print("Login Successful")
                    login_successful = True
                    self.close()
                    try:
                        self.window_manager.open_dashboard(employee=employee)
                    except Exception as e:
                        print("Error opening MainWindow:", e)
                        self.invalidLabel.setText("Error: Problem opening the dashboard.")
                    break

            if not login_successful:
                # Login failed
                print("Login Failed")
                self.invalidLabel.setText("Invalid username or password. Please try again.")

        except Exception as e:
            logging.error(f"Login error: {e}")
            self.invalidLabel.setText("Login error. Please try again.")

    def keyPressEvent(self, event):
        """
        Override keyPressEvent to allow for login on enter press.
        @param event: Key press event.
        """
        if event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.login()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showFullScreen()
    sys.exit(app.exec_())