from Entities.IndirectUser import User
from Entities.Employee import Employee

dbu = User.UserDatabase("IndirectUser/jsonFile/users.json")
user = User.User

dbe = Employee.EmployeeDatabase("Employee/jsonFile/employee.json")
employee = Employee.Employee

# #Example Display Users
# for i in db.load_users():
#     u = user.getUser(i)
#     print(u.displayUser())


# for i in dbu.load_users():
#     print(i.id)
#
# for i in dbe.load_employees():
#     print(i.title)

dbu.addPhoto("0002")