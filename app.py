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
    address = db.Column(db.String(255))
    phone = db.Column(db.Integer)

    def __init__(self, name, username, password, address, phone):
        self.name = name
        self.username = username
        self.password = password
        self.address = address
        self.phone = phone

    def __repr__(self):
        return f"<Employee {self.name}>"

class CalendarModel(db.Model):
    __tablename__ = 'calendar'

    calendarId = db.Column(db.Integer, primary_key=True)
    specialDay = db.Column(db.BigInteger)
    workDay = db.Column(db.BigInteger)
    dayOff = db.Column(db.BigInteger)

    def __init__(self, specialDay, workDay, dayOff):
        self.specialDay = specialDay
        self.workDay = workDay
        self.dayOff = dayOff

    def __repr__(self):
        return f"<Calendar {self.specialDay}>"


class CheckinModel(db.Model):
    __tablename__ = 'checkin'

    checkinId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    workTime = db.Column(db.Integer)
    checkinDate = db.Column(db.BigInteger)
    checkinTime = db.Column(db.BigInteger)
    checkoutTime = db.Column(db.BigInteger)

    def __init__(self, username, workTime, checkinDate, checkinTime, checkoutTime):
        self.username = username
        self.workTime = workTime
        self.checkinDate = checkinDate
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
            "password": employee.password,
            "address": employee.address,
            "phone": employee.phone
        } for employee in employees]
    if request.is_json:
        data = request.get_json()
        login_employee = EmployeesModel(name=data['name'],username=data['username'], password=data['password'], address=data['address'], phone=data['phone'])
        for a in results:
            print(a['username'],a['password'])
            if login_employee.username == a['username']:
                if login_employee.password == a['password']:
                    db.session.close()
                    return {"message": "Login Success", "error": "null"}
                    employees.close()
                    db.close()
                else:
                    db.session.close()
                    return {"message": "Wrong password", "error": "password"}
                    employees.close()
                    db.close()
        else:
            db.session.close()
            return {"message": "Wrong username", "error": "username"}
            employees.close()
            db.close()
    else:
        db.session.close()
        return {"message": "add fail", "error": "The request payload is not in JSON format"}
        employees.close()
        db.close()

@app.route('/employees', methods=['GET'])
def handle_employees():
    employees = EmployeesModel.query.all()
    results = [
        {
            "name": employee.name,
            "username": employee.username,
            "password": employee.password,
            "address": employee.address,
            "phone": employee.phone
        } for employee in employees]

    db.session.close()
                
    return {"count": len(results), "employees": results, "message": "success", "error": "null"}


@app.route('/employees/add', methods=['POST'])
def handle_employees_add():
    if request.is_json:
        data = request.get_json()
        new_employee = EmployeesModel(name=data['name'],username=data['username'], password=data['password'], address=data['address'], phone=data['phone'])
    
        try: 
            db.session.add(new_employee)
            db.session.commit()

            db.session.close()

            return {"message": "Add success", "error": "null"}

            employees.close()
            db.close() 
        except:
            return {"message": "Add fail", "error": "username"}
    else:
        db.session.close()

        return {"message": "add fail", "error": "The request payload is not in JSON format"}

        employees.close()
        db.close()
        
@app.route('/employees/update', methods=['POST'])
def handle_employees_update():
    if request.is_json:
        data = request.get_json()
        update_employee = EmployeesModel(name=data['name'],username=data['username'], password=data['password'], address=data['address'], phone=data['phone'])
        
        try:
            update = EmployeesModel.query.filter_by(username=update_employee.username).first()
            update.name = update_employee.name
            update.password = update_employee.password
            update.address = update_employee.address
            update.phone = update_employee.phone
            db.session.commit()

            db.session.close()
                    
            return {"message": "update success"}
        except:
            return {"message": "update fail", "error": "username"}
    else:
        db.session.close()

        return {"message": "update fail", "error": "The request payload is not in JSON format"}

        employees.close()
        db.close()

@app.route('/employees/delete', methods=['POST'])
def handle_employees_delete():
    if request.is_json:
        data = request.get_json()
        delete_employee = EmployeesModel(name=data['name'],username=data['username'], password=data['password'], address=data['address'], phone=data['phone'])
        
        try:
            EmployeesModel.query.filter_by(username=delete_employee.username).delete()
            CheckinModel.query.filter_by(username=delete_employee.username).delete()

            db.session.commit()
                        
            db.session.close()

            return {"message": "delete success"}
        except:
            return {"message": "delete fail", "error": "username"}
    else:
        db.session.close()

        return {"message": "delete fail", "error": "The request payload is not in JSON format"}

        employees.close()
        db.close()

        


# checkin

@app.route('/checkin', methods=['POST'])
def handle_checkin():

    if request.is_json:
        data = request.get_json()
        get_checkin = CheckinModel(username=data['username'], workTime=data['workTime'], checkinDate=data['checkinDate'], checkinTime=data['checkinTime'], checkoutTime=data['checkoutTime'])
        
        try:
            checkins = CheckinModel.query.filter_by(username=get_checkin.username)
            results = [
            {
                "username": checkin.username,
                "workTime": checkin.workTime,
                "checkinDate": checkin.checkinDate,
                "checkinTime": checkin.checkinTime,
                "checkoutTime": checkin.checkoutTime
            } for checkin in checkins]
            return {"count": len(results), "data": results, "message": "success", "error": "null"}
        except:
            return {"count": len(results), "data": "not found", "message": "success", "error": "null"}
    else:

        db.session.close()

        return {"message": "get fail", "error": "The request payload is not in JSON format"}

    
@app.route('/checkin/add', methods=['POST'])
def handle_checkin_add():
    if request.is_json:
        data = request.get_json()
        new_checkin = CheckinModel(username=data['username'], workTime=data['workTime'], checkinDate=data['checkinDate'], checkinTime=data['checkinTime'], checkoutTime=data['checkoutTime'])
        
        try:
            db.session.add(new_checkin)
            db.session.commit()

            db.session.close()

            return {"message": "Add success", "error": "null"}
        except:
            return {"message": "Add fail", "error": "null"}
    else:
        db.session.close()

        return {"message": "add fail", "error": "The request payload is not in JSON format"}

        checkins.close()
        db.close()
        
@app.route('/checkin/update', methods=['POST'])
def handle_checkin_update():
    if request.is_json:
        data = request.get_json()
        update_checkin = CheckinModel(username=data['username'], workTime=data['workTime'], checkinDate=data['checkinDate'], checkinTime=data['checkinTime'], checkoutTime=data['checkoutTime'],)
        
        try:
            update = CheckinModel.query.filter_by(username=update_checkin.username, checkinDate=update_checkin.checkinDate).first()
            update.workTime = update_checkin.workTime
            update.checkinTime = update_checkin.checkinTime
            update.checkoutTime = update_checkin.checkoutTime
                        
            db.session.commit()

            db.session.close()
                        
            return {"message": "update success"}
        except:
            return {"message": "update fail"}
    else:
        db.session.close()

        return {"message": "update fail", "error": "The request payload is not in JSON format"}

        checkins.close()
        db.close()

@app.route('/checkin/delete', methods=['POST'])
def handle_checkin_delete():
    if request.is_json:
        data = request.get_json()
        delete_checkin = CheckinModel(username=data['username'], workTime=data['workTime'], checkinDate=data['checkinDate'], checkinTime=data['checkinTime'], checkoutTime=data['checkoutTime'],)
        
        try:
            CheckinModel.query.filter_by(username=delete_checkin.username, checkinDate=delete_checkin.checkinDate).delete()
            db.session.commit()
                        
            db.session.close()

            return {"message": "delete success"}
        except:
            return {"message": "delete fail"}
    else:

        db.session.close()

        return {"message": "delete fail", "error": "The request payload is not in JSON format"}

        checkins.close()
        db.close()


# calendar

@app.route('/calendar', methods=['GET'])
def handle_calendar():
    try:
        calendars = CalendarModel.query.all()
        results = [
            {
                "specialDay": calendar.specialDay,
                "workDay": calendar.workDay,
                "dayOff": calendar.dayOff
            } for calendar in calendars]
        return {"count": len(results), "data": results, "message": "success", "error": "null"}
    except:
        return {"count": len(results), "data": "not found", "message": "success", "error": "null"}
    
@app.route('/calendar/add', methods=['POST'])
def handle_calendar_add():
    if request.is_json:
        data = request.get_json()
        new_calendar = CalendarModel(specialDay=data['specialDay'], workDay=data['workDay'], dayOff=data['dayOff'])
    
        try:
            db.session.add(new_calendar)
            db.session.commit()

            db.session.close()

            return {"message": "Add success", "error": "null"}
        except:
            return {"message": "Add fail", "error": "null"}
    else:
        db.session.close()

        return {"message": "add fail", "error": "The request payload is not in JSON format"}

        calendars.close()
        db.close()
        
@app.route('/calendar/update', methods=['POST'])
def handle_calendar_update():
    if request.is_json:
        data = request.get_json()
        update_calendar = CalendarModel(specialDay=data['specialDay'], workDay=data['workDay'], dayOff=data['dayOff'])
        try:
            update = CalendarModel.query.filter_by(specialDay=update_calendar.specialDay, workDay=update_calendar.workDay, dayOff=update_calendar.dayOff).first()
            update.specialDay = update_calendar.specialDay
            update.workDay = update_calendar.workDay
            update.dayOff = update_calendar.dayOff
                    
            db.session.commit()
        
            return {"message": "update success"}
        except:
            return {"message": "update fail"}
    else:

        db.session.close()

        return {"message": "update fail", "error": "The request payload is not in JSON format"}

        calendars.close()
        db.close()

@app.route('/calendar/delete', methods=['POST'])
def handle_calendar_delete():
    if request.is_json:
        data = request.get_json()
        delete_calendar = CalendarModel(specialDay=data['specialDay'], workDay=data['workDay'], dayOff=data['dayOff'])
        try:    
            CalendarModel.query.filter_by(specialDay=delete_calendar.specialDay, workDay=delete_calendar.workDay, dayOff=delete_calendar.dayOff).delete()
            db.session.commit()
                        
            db.session.close()

            return {"message": "delete success"}
        except:
            return {"message": "delete fail"}
    else:

        db.session.close()

        return {"message": "delete fail", "error": "The request payload is not in JSON format"}

        calendars.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
