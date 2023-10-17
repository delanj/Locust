import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.centerOnScreen()
        self.show()


    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 1000, 600)
        self.setWindowTitle("Splash Screen Example")

        # Set the background color to black
        self.setStyleSheet("background-color: #151316;")

        layout = QVBoxLayout()

        image_label = QLabel(self)
        pixmap = QPixmap('Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.jpg')
        #300 200
        scaled_pixmap = pixmap.scaled(450, 300, Qt.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        layout.addWidget(image_label, alignment=Qt.AlignHCenter)  # Center horizontally

        text_label = QLabel("LocUST", self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet("color: white;")
        font = QFont('Futura')
        font.setPointSize(30)

        text_label.setFont(font)
        layout.addWidget(text_label, alignment=Qt.AlignCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setStyleSheet("QProgressBar {background: #ffffff ;}")
        self.progress_bar.setStyleSheet("QProgressBar::chunk {background: #d7b970;}")

        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Create a QTimer for simulating progress
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.updateProgress)
        self.progress = 0

        # Start the progress timer
        self.progress_timer.start(100)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def centerOnScreen(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

    def updateProgress(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)

        if self.progress_bar.value() >= 100:
            self.progress_timer.stop()
            # Close the splash screen or transition to your main window
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    # QTimer.singleShot(5000, splash.closeSplashScreen)  # Close the splash screen after 5 seconds
    sys.exit(app.exec_())

    # loading_label = QLabel(self)
    # loading_label.setStyleSheet("background-color: transparent;")
    # loading_movie = QMovie('Icons/Spinner.gif')
    # loading_label.setMovie(loading_movie)
    # loading_movie.start()
    # layout.addWidget(loading_label, alignment=Qt.AlignHCenter)  # Center horizontally