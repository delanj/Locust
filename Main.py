import sys
from PyQt5.QtWidgets import QApplication
from GUI.window_manager import WindowManager

def main():
    app = QApplication(sys.argv)  # Assuming you're using PyQt5
    manager = WindowManager()
    manager.open_login()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
