import json
from typing import List, Optional, Dict, Union

class Employee:
    def __init__(self, employee_id: str, first_name: str, last_name: str, gender: str,
                 title: str, passcode: str, phone_number: str, email: str, hire_date: str):
        """Initialize an Employee with basic information."""
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.title = title
        self.passcode = passcode
        self.phone_number = phone_number
        self.email = email
        self.hire_date = hire_date

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """Return the employee's attributes as a dictionary."""
        return vars(self)

    def get_special_id(self):
        """Return the special ID if available, otherwise None."""
        if isinstance(self, DeskTechnician):
            return self.tech_id
        elif isinstance(self, SecurityManager):
            return self.manager_id
        else:
            return None


class DeskTechnician(Employee):
    def __init__(self, tech_id: str, *args):
        """Initialize a Desk Technician, which is a type of Employee."""
        super().__init__(*args)
        self.tech_id = tech_id

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """Return the desk technician's attributes as a dictionary."""
        return {"techID": self.tech_id, **super().to_dict()}


class SecurityManager(Employee):
    def __init__(self, manager_id: str, *args):
        """Initialize a Security Manager, which is a type of Employee."""
        super().__init__(*args)
        self.manager_id = manager_id

    def to_dict(self) -> Dict[str, Union[str, int]]:
        """Return the security manager's attributes as a dictionary."""
        return {"managerID": self.manager_id, **super().to_dict()}


class EmployeeDatabase:
    def __init__(self):
        """Initialize the employee database."""
        self.json_file_path = '../Database/Employees/jsonFile/employee.json'
        self.employees = self.load_employees()

    def create_employee(self, data: Dict[str, str]) -> Employee:
        """Factory method to create an employee based on their title."""
        title = data.get("title")
        args = (data.get("employeeID"), data.get("firstName"), data.get("lastName"),
                data.get("gender"), title, data.get("passcode"),
                data.get("phoneNumber"), data.get("email"), data.get("hireDate"))

        if title == "Desk Technician":
            return DeskTechnician(data.get("techID"), *args)
        elif title == "Security Manager":
            return SecurityManager(data.get("managerID"), *args)
        else:
            return Employee(*args)

    def load_employees(self) -> List[Employee]:
        """Load employees from a JSON file."""
        try:
            with open(self.json_file_path, "r") as json_file:
                employee_data = json.load(json_file)
            return [self.create_employee(data) for data in employee_data]
        except FileNotFoundError:
            print("File not found.")
            return []

    def get_employee_by_id(self, employee_id: str) -> Optional[Employee]:
        """Retrieve an employee by their ID."""
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee
        return None

    def save_employees(self):
        """Save the current list of employees to a JSON file."""
        employees_data = [employee.to_dict() for employee in self.employees]
        try:
            with open(self.json_file_path, "w") as json_file:
                json.dump(employees_data, json_file, indent=4)
        except IOError as e:
            print(e)
            pass

    def get_all_employees(self) -> List[Employee]:
        """Return a list of all employees."""
        return self.employees
