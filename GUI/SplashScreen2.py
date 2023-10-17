import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QProgressBar, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class SplashScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.centerOnScreen()
        self.show()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 800, 400)
        self.setWindowTitle("Splash Screen Example")
        self.setStyleSheet("background-color: #151316;")

        layout = QVBoxLayout()

        horizontal_layout = QHBoxLayout()

        loc_label = QLabel("L", self)
        loc_label.setAlignment(Qt.AlignCenter)
        loc_label.setStyleSheet("color: white;")
        font = QFont('Futura')
        font.setPointSize(250)
        loc_label.setFont(font)
        horizontal_layout.addWidget(loc_label, alignment=Qt.AlignCenter)

        image_label = QLabel(self)
        pixmap = QPixmap('Icons/7d597e2c-2613-464e-bd81-d18f1a50bbe1.jpg')
        scaled_pixmap = pixmap.scaled(450, 300, Qt.KeepAspectRatio)
        image_label.setPixmap(scaled_pixmap)
        horizontal_layout.addWidget(image_label, alignment=Qt.AlignCenter)

        ust_label = QLabel("cUST", self)
        ust_label.setAlignment(Qt.AlignCenter)
        ust_label.setStyleSheet("color: white;")
        font = QFont('Futura')
        font.setPointSize(250)
        ust_label.setFont(font)
        horizontal_layout.addWidget(ust_label, alignment=Qt.AlignCenter)

        layout.addLayout(horizontal_layout)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setStyleSheet("QProgressBar {background: #ffffff ;}")
        self.progress_bar.setStyleSheet("QProgressBar::chunk {background: #d7b970;}")
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.updateProgress)
        self.progress = 0
        self.progress_timer.start(100)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def centerOnScreen(self):
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.geometry()
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2
        self.move(x, y)

    def updateProgress(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)

        if self.progress_bar.value() >= 100:
            self.progress_timer.stop()
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    sys.exit(app.exec_())

