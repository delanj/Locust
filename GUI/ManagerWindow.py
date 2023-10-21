import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout


class MainWindow(QMainWindow):
    def __init__(self, employee=None):
        super().__init__()

        self.setWindowTitle("Main Application Window")
        self.showMaximized()
        self.showFullScreen()
        central_widget = QWidget()

        central_widget.setStyleSheet("background-color: rgb(36, 36, 36);")
        main_layout = QHBoxLayout(central_widget)


        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())