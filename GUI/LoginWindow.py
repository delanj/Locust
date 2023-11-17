import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from Entities import entitiesMain as db
import dashboard

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

    def __init__(self):
        """ Initialize the main login window. """
        super().__init__()
        logging.basicConfig(level=logging.INFO)
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
        loginLayout.addSpacing(15)
        self.usernameEdit = self.createLineEdit("Username")
        self.passwordEdit = self.createLineEdit("Password", True)
        loginLayout.addWidget(self.usernameEdit)
        loginLayout.addWidget(self.passwordEdit)
        loginLayout.addSpacing(30)
        loginLayout.addLayout(self.createButtonLayout())
        loginLayout.addSpacing(30)
        loginLayout.addWidget(self.createCopyrightLabel())

        return loginWidget

    def createShadowEffect(self):
        """ Creates and returns a shadow effect."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(3, 3)
        return shadow

    def createLogoLabel(self):
        """ Creates and returns the logo label. """
        label = QLabel("LocUST")
        label.setStyleSheet('font-size: 56pt; font-family: "Garamond"; color: #E0E0E0; padding: 6px; min-width: 10;')
        label.setFixedHeight(75)
        label.setAlignment(Qt.AlignCenter)
        return label

    def createImageLabel(self):
        """ Creates and returns the image label."""
        imageLabel = QLabel(self)
        pixmap = QPixmap("Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.png")
        imageLabel.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        imageLabel.setAlignment(Qt.AlignCenter)
        imageLabel.setFixedHeight(225)
        return imageLabel

    def createInvalidLoginLabel(self):
        """ Creates and returns the invalid login label."""
        invalidLabel = QLabel("")
        invalidLabel.setAlignment(Qt.AlignCenter)
        invalidLabel.setStyleSheet('color: #E0E0E0; font: 75 12px "Garamond";')
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
        lineEdit.setFixedHeight(30)
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
        copyrightLabel.setStyleSheet('color: #E0E0E0; font: 75 12px "Garamond";')
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
                        self.dashboard_main = dashboard.DashboardWindow(employee=employee)
                        self.dashboard_main.show()
                    except Exception as e:
                        print("Error opening MainWindow:", e)
                        self.invalidLabel.setText("Error: Problem opening the dashboard.")
                    break

            if not login_successful:
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