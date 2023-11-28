from GUI.dashboard import DashboardWindow
#from GUI.facialRecognition import FacialRecognitionWindow
from GUI.login import LoginWindow
from GUI.refactor import FacialRecognitionWindow

class WindowManager:
    def __init__(self):
        self.current_window = None
        self.employee = None

    def open_login(self):
        self.close_current_window()
        self.current_window = LoginWindow(self)
        self.current_window.show()

    def open_dashboard(self, employee):
        self.close_current_window()
        self.employee = employee
        self.current_window = DashboardWindow(self, employee=self.employee)
        self.current_window.show()

    def open_facial_recognition(self, employee):
        self.close_current_window()
        self.employee = employee
        self.current_window = FacialRecognitionWindow(self, employee=self.employee)
        self.current_window.show()

    def close_current_window(self):
        if self.current_window is not None:
            self.current_window.close()
