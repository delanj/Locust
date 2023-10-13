import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, \
    QTableWidgetItem, QTableWidget, QDesktopWidget
from PyQt5.QtGui import QPixmap, QImage, QImageReader
from PyQt5.QtCore import Qt, QTimer

class WebcamHandler(QWidget):
    def __init__(self):
        super().__init__()
        self.webcam_label = QLabel(self)
        self.init_webcam()

        layout = QVBoxLayout()
        layout.addWidget(self.webcam_label)
        self.setLayout(layout)

    def init_webcam(self):
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            print("Error: Unable to access the webcam.")
            return
        self.webcam_timer = QTimer(self)
        self.webcam_timer.timeout.connect(self.update_webcam_feed)
        self.webcam_timer.start(50)  # Update every 50 milliseconds

    def update_webcam_feed(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.webcam_label.setPixmap(pixmap)


class TableView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        table_widget = QTableWidget(self)
        table_widget.setColumnCount(3)
        table_widget.setHorizontalHeaderLabels(["Name", "Age", "City"])
        table_widget.setStyleSheet("background-color: rgb(255,255,255);")

        data = [("John", "30", "New York"),
                ("Alice", "25", "Los Angeles"),
                ("Bob", "35", "Chicago"),
                ("Eve", "28", "San Francisco"),
                ("Charlie", "32", "Miami")]

        for i, (name, age, city) in enumerate(data):
            table_widget.insertRow(i)
            table_widget.setItem(i, 0, QTableWidgetItem(name))
            table_widget.setItem(i, 1, QTableWidgetItem(age))
            table_widget.setItem(i, 2, QTableWidgetItem(city))

        table_widget.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(table_widget)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application Window")
        self.showMaximized()
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: rgb(36, 36, 36);")
        main_layout = QHBoxLayout(central_widget)

        layout_left = QVBoxLayout()

        colored_widget = QWidget()
        colored_widget.setStyleSheet("background-color: rgb(105, 105, 105);")
        colored_layout = QVBoxLayout(colored_widget)

        picture = QLabel(self)
        picturePixmap = QPixmap("Picture/file.jpg")
        picture.setPixmap(picturePixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        picture.setAlignment(Qt.AlignCenter)
        colored_layout.addWidget(picture)

        nameLabel = QLabel("Name")
        colored_layout.addWidget(nameLabel)

        genderLabel = QLabel("Gender")
        colored_layout.addWidget(genderLabel)

        idLabel = QLabel("ID")
        colored_layout.addWidget(idLabel)

        companyLabel = QLabel("Company")
        colored_layout.addWidget(companyLabel)

        tittleLabel = QLabel("Title")
        colored_layout.addWidget(tittleLabel)

        buttonBox = QHBoxLayout()
        colored_layout.addLayout(buttonBox)

        acceptButton = QPushButton("Accept")
        acceptButton.setFixedWidth(50)
        acceptButton.setStyleSheet("background-color: rgb(105, 105, 105);")
        acceptButton.clicked.connect(self.acceptHandle)
        buttonBox.addWidget(acceptButton)

        rejectButton = QPushButton("Reject")
        rejectButton.setFixedWidth(50)
        rejectButton.setStyleSheet("background-color: rgb(105, 105, 105);")
        rejectButton.clicked.connect(self.rejectHandle)
        buttonBox.addWidget(rejectButton)

        layout_left.addWidget(colored_widget, alignment=Qt.AlignLeft)
        main_layout.addLayout(layout_left)

        layout_right = QVBoxLayout()
        main_layout.addLayout(layout_right)

        webcam_handler = WebcamHandler()
        layout_right.addWidget(webcam_handler)

        table_view = TableView()
        layout_right.addStretch()
        layout_right.addWidget(table_view, alignment=Qt.AlignBottom)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def rejectHandle(self):
        self.close()

    def acceptHandle(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
