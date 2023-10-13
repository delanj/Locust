import json


class Employee:
    def __init__(self, employeeID, firstName, lastName, gender, title, passcode, phoneNumber, email, hireDate):
        self.employeeID = employeeID
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.title = title
        self.passcode = passcode
        self.phoneNumber = phoneNumber
        self.email = email
        self.hireDate = hireDate

    def getEmployee(self):
        e = Employee(self.employeeID, self.firstName, self.lastName, self.gender, self.title,
                     self.passcode, self.phoneNumber, self.email, self.hireDate)
        return e

class deskTechnician(Employee):
    def __init__(self, techID, employeeID, firstName, lastName, gender, title, passcode, phoneNumber, email, hireDate):
        super().__init__(employeeID, firstName, lastName, gender, title, passcode, phoneNumber, email, hireDate)
        self.techID = techID
    def getDeskTechnician(self):
        e = deskTechnician(self.techID, self.employeeID, self.firstName, self.lastName, self.gender, self.title,
                           self.passcode, self.phoneNumber, self.email, self.hireDate)
        return e


class securityManager(Employee):
    def __init__(self, managerID, employeeID, firstName, lastName, gender, title, passcode, phoneNumber, email, hireDate):
        super().__init__(employeeID, firstName, lastName, gender, title, passcode, phoneNumber, email, hireDate)
        self.managerID = managerID
    def getSecurityManager(self):
        e = deskTechnician(self.managerID, self.employeeID, self.firstName, self.lastName, self.gender, self.title,
                           self.passcode, self.phoneNumber, self.email, self.hireDate)
        return e


class EmployeeDatabase:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.employees = self.load_employees()

    def load_employees(self):
        try:
            with open(self.json_file_path, "r") as json_file:
                employeeData = json.load(json_file)
            employees = []

            for employeeData in employeeData:
                title = employeeData.get("title")
                if title == "Desk Technician":
                    employee = deskTechnician(
                        employeeData.get("techID"),
                        employeeData.get("employeeID"),
                        employeeData.get("firstName"),
                        employeeData.get("lastName"),
                        employeeData.get("gender"),
                        title,
                        employeeData.get("passcode"),
                        employeeData.get("phoneNumber"),
                        employeeData.get("email"),
                        employeeData.get("hireDate")
                    )
                elif title == "Security Manager":
                    employee = securityManager(
                        employeeData.get("managerID"),
                        employeeData.get("employeeID"),
                        employeeData.get("firstName"),
                        employeeData.get("lastName"),
                        employeeData.get("gender"),
                        title,
                        employeeData.get("passcode"),
                        employeeData.get("phoneNumber"),
                        employeeData.get("email"),
                        employeeData.get("hireDate")
                    )
                else:
                    # Handle other types of employees if needed
                    employee = Employee(
                        employeeData.get("employeeID"),
                        employeeData.get("firstName"),
                        employeeData.get("lastName"),
                        employeeData.get("gender"),
                        title,
                        employeeData.get("passcode"),
                        employeeData.get("phoneNumber"),
                        employeeData.get("email"),
                        employeeData.get("hireDate")
                    )

                employees.append(employee)

            return employees
        except FileNotFoundError:
            return []

    def get_employee_by_id(self, employeeID):
        for e in self.employees:
            if e.id == employeeID:
                return e
        return None


