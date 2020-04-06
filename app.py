from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://haianh:haianh@pikatech.info:54321/haianh"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class EmployeesModel(db.Model):
    __tablename__ = 'employees'

    employeeId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def __repr__(self):
        return f"<Employee {self.name}>"

class CalendarModel(db.Model):
    __tablename__ = 'calendar'

    calendarId = db.Column(db.Integer, primary_key=True)
    specialDay = db.Column(db.Date)

    def __init__(self, specialDay):
        self.specialDay = specialDay

    def __repr__(self):
        return f"<Calendar {self.specialDay}>"


class CheckinModel(db.Model):
    __tablename__ = 'checkin'

    employeeId = db.Column(db.Integer, primary_key=True)
    checkinDate = db.Column(db.Date, primary_key=True)
    checkinTime = db.Column(db.DateTime)
    checkoutTime = db.Column(db.DateTime)

    def __init__(self, checkinTime, checkoutTime):
        self.checkinTime = checkinTime
        self.checkoutTime = checkoutTime

    def __repr__(self):
        return f"<Checkin {self.checkinTime}>"

@app.route('/')
def hello():
    return {"hello": "world"}

@app.route('/login', methods=['POST'])
def handle_login():
    employees = EmployeesModel.query.all()
    results = [
        {
            "name": employee.name,
            "username": employee.username,
            "password": employee.password
        } for employee in employees]
    if request.is_json:
        data = request.get_json()
        login_employee = EmployeesModel(name=data['name'],username=data['username'], password=data['password'])
        for a in results:
            print(a['username'],a['password'])
            if login_employee.username == a['username']:
                for b in results:
                    if login_employee.password == b['password']:
                        return {"message": "Login Success", "error": "null"}
                else:
                    return {"message": "Wrong password", "error": "password"}
        else:
            return {"message": "Wrong username", "error": "username"}
    else:
        return {"message": "add fail","error": "The request payload is not in JSON format"}

@app.route('/employees', methods=['GET'])
def handle_employees():
    employees = EmployeesModel.query.all()
    results = [
        {
            "name": employee.name,
            "username": employee.username,
            "password": employee.password
        } for employee in employees]

    return {"count": len(results), "employees": results, "message": "success", "error": "null"}
    
@app.route('/employees/add', methods=['POST'])
def handle_employees_add():
    employees = EmployeesModel.query.all()
    results = [
        {
            "name": employee.name,
            "username": employee.username,
            "password": employee.password
        } for employee in employees]
    if request.is_json:
        data = request.get_json()
        new_employee = EmployeesModel(name=data['name'], username=data['username'], password=data['password'])
    
        for a in results:
            if new_employee.username != a['username']:
                print(new_employee.username,"  +  ",a['username'])
                continue
            else:
                return {"message": "Username exists", "error": "username"}
        else:
            db.session.add(new_employee)
            db.session.commit()
            return {"message": "Add success", "error": "username"}       
    else:
        return {"message": "add fail", "error": "The request payload is not in JSON format"}
        
@app.route('/employees/update', methods=['POST'])
def handle_employees_update():
    employees = EmployeesModel.query.all()
    results = [
        {
            "name": employee.name,
            "username": employee.username,
            "password": employee.password
        } for employee in employees]
    if request.is_json:
        data = request.get_json()
        update_employee = EmployeesModel(name=data['name'], username=data['username'], password=data['password'])
        for a in results:
            print(a['username'])
            if update_employee.username == a['username']:

                update = EmployeesModel.query.filter_by(username=update_employee.username).first()
                update.name = update_employee.name
                update.password = update_employee.password
                db.session.commit()
                
                return {"message": "update success"}     
        else:
            return {"message": "Wrong username", "error": "username"}
    else:
        return {"message": "update fail", "error": "The request payload is not in JSON format"}

@app.route('/employees/delete', methods=['POST'])
def handle_employees_delete():
    employees = EmployeesModel.query.all()
    results = [
        {
            "name": employee.name,
            "username": employee.username,
            "password": employee.password
        } for employee in employees]
    if request.is_json:
        data = request.get_json()
        delete_employee = EmployeesModel(name=data['name'], username=data['username'], password=data['password'])
        for a in results:
            print(a['username'], " assssssssssssss", a)
            if delete_employee.username == a['username']:
                EmployeesModel.query.filter_by(username=delete_employee.username).delete()
                db.session.commit()
            
                return {"message": "delete success"}     
        else:
            return {"message": "Wrong username", "error": "username"}    
    else:
        return {"message": "delete fail", "error": "The request payload is not in JSON format"}

if __name__ == '__main__':
    app.run(debug=True)
