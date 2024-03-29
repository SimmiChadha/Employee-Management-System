import json
class Employee:
    def __init__(self, emp_id, name, title, dept) -> None:
        self.emp_id = emp_id
        self.name = name
        self.title = title
        self.dept = dept

    def get_employee_details(self):
        print(f'Employee Name: {self.name}')
        print(f'Employee ID: {self.emp_id}')
        print(f'Title: {self.title}')
        print(f'Department: {self.dept}')

    def __str__(self) -> str:
        return f'{self.name} ({self.emp_id})'
    
    def to_dict(self):
        return {
            'emp_id':self.emp_id,
            'name':self.name,
            'title':self.title,
            'dept':self.dept
        }

class Department:
    def __init__(self, name) -> None:
        self.name = name
        self.employees = []

    def add_employee(self, employee):
        self.employees.append(employee)

    def remove_employee(self,employee):
        if employee in self.employees:
            self.employees.remove(employee)
        else:
            print('Employee not found in this department')

    def list_employees(self):
        for employee in self.employees:
            print(employee)

    def to_dict(self):
        return {
            'name':self.name, 
            'employees':[emp.to_dict() for emp in self.employees]
            }

class Company:
    def __init__(self):
        self.departments = {}

    def add_department(self, department):
        self.departments[department.name] = department

    def remove_department(self, department_name):
        if department_name in self.departments:
            del self.departments[department_name]
        else:
            print('Department not found ')

    def display_department(self):
        dept = self.departments.keys()
        print(f"Department: {','.join(dept)}")
        # for key, val in self.departments.items():
        #     print(f'Department: {key}')
        #     val.list_employees()

    def display_employee_details(self, emp_id):
        found_employee = False
        for department in self.departments.values():
            for employee in department.employees:
                if employee.emp_id == emp_id:
                    employee.get_employee_details()
                    found_employee = True
                    break
            if found_employee:
                break
        if not found_employee:
            print('Employee not found')

    def display_employee_list(self):
        for department in self.departments.values():
            for employee in department.employees:
                employee.get_employee_details()

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            data = {
                'departments': [dept.to_dict() for dept in self.departments.values()]
            }
            json.dump(data, file, indent=4)

    def save_after_changes(self,filepath):
        self.save_to_file(filepath)
        print('company data saved to a file')

    def remove_employee(self, emp_id):
        for department in self.departments.values():
            for employee in department.employees:
                if employee.emp_id == emp_id:
                    department.remove_employee(employee)
                    print('employee reomved successfully')
                    return
            
        print('employee not found')

    @classmethod
    def load_from_file(cls, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            company = cls()
            for dept_data in data['departments']:
                department = Department(dept_data['name'])
                company.add_department(department)
            return company
            

def menu():
    print("Employee Management System")
    print("1. Add Employee")
    print("2. Remove Employee")
    print("3. Add Department")
    print("4. Remove Department")
    print("5. Display Department")
    print("6. Display Single Employee Details")
    print("7. Diplay All Employees Details")
    print("8. Save data to a file")
    print("9. Exit")

def main():
    file_path = 'company_data.json' # specify the file path

    # check if file exists, load data if it does
    try:
        company = Company.load_from_file(file_path)
        print('data loaded successfully')
    except FileNotFoundError:
        company = Company()
        print('no saved data found. starting with an empty company')

    while True:
        menu()
        choice = input('Enter your choice: ')

        if choice == '1':
            name = input('Enter employee name: ')
            emp_id = input('Enter employee id: ')
            title = input('Enter employee title: ')
            dept = input('Enter department name: ')

            # Check if department exists, otherwise add it
            if dept not in company.departments:
                new_department = Department(dept)
                company.add_department(new_department)

            # Add employee to the department 
            emp = Employee(emp_id, name, title, dept)
            company.departments[dept].add_employee(emp)

        elif choice == '2':
            emp_id = input('Enter employee id to remove: ')
            company.remove_employee(emp_id)

        elif choice == '3':
            department_name = input('Enter department name to add: ')
            department = Department(department_name)
            company.add_department(department)

        elif choice == '4':
            department_name = input('Enter department name to remove: ')
            company.remove_department(department_name)

        elif choice == '5':
            company.display_department()

        elif choice == '6':
            emp_id = input("Enter employee id to display details: ")
            company.display_employee_details(emp_id)

        elif choice == '7':
            company.display_employee_list()

        elif choice == '8':
            company.save_after_changes(file_path)
            print('Company data saved to a file')

        elif choice == '9':
            print("Exiting Employee Management System")
            break

        else:
            print("Invalid Choice. Please try again")

if __name__ == "__main__":
    main()


