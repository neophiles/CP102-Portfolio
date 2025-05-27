# Tagle, Marc Neil V.

from employee import Employee

name = input("Enter Employee Name: ")
gender = input("Enter Gender (M/F): ").upper()
bdate = input("Enter Birth Date: ")
position = input("Enter Position: ")
rate = int(input("Enter Rate per day: "))
dayswork = int(input("Enter Days Worked: "))

employee1 = Employee(name, gender, bdate, position, rate, dayswork)
print()
employee1.getEmployeeDetails()
print()
employee1.getSalaryDetails()