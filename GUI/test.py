import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame
from PyQt5.QtCore import QPropertyAnimation, QRect
from PyQt5.QtGui import QColor

class Sidebar(QFrame):
    def __init__(self, parent=None, width=200):
        super().__init__(parent)
        self.parent = parent
        self.sidebar_width = width
        self.initUI()

    def initUI(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedWidth(self.sidebar_width)
        self.setGeometry(self.parent.width(), 0, self.sidebar_width, self.parent.height())
        # Set the sidebar color (e.g., light gray)
        self.setStyleSheet("background-color: lightgray;")

        # Animation for sidebar
        self.sidebar_animation = QPropertyAnimation(self, b"geometry")
        self.sidebar_animation.setDuration(500)

    def toggle(self):
        sidebar_geometry = self.geometry()

        if sidebar_geometry.right() > self.parent.width():
            # Sidebar is hidden, show it
            end_value = QRect(self.parent.width() - self.sidebar_width, 0, self.sidebar_width, self.parent.height())
        else:
            # Sidebar is visible, hide it
            end_value = QRect(self.parent.width(), 0, self.sidebar_width, self.parent.height())

        self.sidebar_animation.setStartValue(sidebar_geometry)
        self.sidebar_animation.setEndValue(end_value)
        self.sidebar_animation.start()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sidebar_width = 200
        self.initUI()

    def initUI(self):
        self.setFixedSize(800, 600)
        self.setWindowTitle('Sidebar Example')

        # Set the main window background color (e.g., white)
        self.setStyleSheet("background-color: white;")

        # Sidebar
        self.sidebar = Sidebar(self, self.sidebar_width)

        # Tab button to open/close sidebar, placed at the edge of the window initially
        self.tab_button = QPushButton('>>', self)
        self.tab_button.setGeometry(self.width() - 40, 10, 40, 40)
        self.tab_button.clicked.connect(self.toggleSidebar)

        # Set the button color (e.g., blue)
        self.tab_button.setStyleSheet("background-color: lightblue;")

        # Animation for tab button
        self.tab_button_animation = QPropertyAnimation(self.tab_button, b"geometry")
        self.tab_button_animation.setDuration(500)

        self.show()

    def toggleSidebar(self):
        # Sidebar is visible if its right edge is less than the width of the main window
        sidebar_visible = self.sidebar.geometry().right() < self.width()

        # Determine the new geometry for the button after the toggle
        if sidebar_visible:
            # If the sidebar is visible, hide it and move the button to the window's edge
            tab_button_target_x = self.width() - self.tab_button.width()
            self.tab_button.setText('>>')
        else:
            # If the sidebar is hidden, show it and move the button to the sidebar's edge
            tab_button_target_x = self.width() - self.sidebar_width - self.tab_button.width()
            self.tab_button.setText('<<')

        # Start the toggle animation for the sidebar
        self.sidebar.toggle()

        # Animate the tab button to move with the sidebar
        self.tab_button_animation.setStartValue(self.tab_button.geometry())
        self.tab_button_animation.setEndValue(QRect(tab_button_target_x, 10, 40, 40))

        self.tab_button_animation.start()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
