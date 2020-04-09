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
    username= db.Column(db.String(255))
    specialDay = db.Column(db.BigInteger)
    workDay = db.Column(db.BigInteger)
    dayOff = db.Column(db.BigInteger)

    def __init__(self, username, specialDay, workDay, dayOff):
        self.username = username
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
    checkinDate = db.Column(db.BigInteger, primary_key=True)
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
            "password": employee.password
        } for employee in employees]
    if request.is_json:
        data = request.get_json()
        login_employee = EmployeesModel(name=data['name'],username=data['username'], password=data['password'])
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

@app.route('/employees', methods=['POST'])
def handle_employees():
    employees = EmployeesModel.query.all()
    results = [
        {
            "name": employee.name,
            "username": employee.username,
            "password": employee.password
        } for employee in employees]

    if request.is_json:
        data = request.get_json()
        get_employee = EmployeesModel(name=data['name'], username=data['username'], password=data['password'])
        for a in results:
            print(a['username'])
            if get_employee.username == a['username']:

                db.session.close()
                
                return {"count": len(results), "employees": results, "message": "success", "error": "null"}
                
                employees.close()
                db.close()
        else:
            db.session.close()

            return {"message": "Wrong username", "error": "username"}

            employees.close()
            db.close()
    else:
        db.session.close()

        return {"message": "get fail", "error": "The request payload is not in JSON format"}

        employees.close()
        db.close()


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

                db.session.close()

                return {"message": "Username exists", "error": "username"}
                
                employees.close()
                db.close()
        else:
            db.session.add(new_employee)
            db.session.commit()

            db.session.close()

            return {"message": "Add success", "error": "username"}

            employees.close()
            db.close()     
    else:
        db.session.close()

        return {"message": "add fail", "error": "The request payload is not in JSON format"}

        employees.close()
        db.close()
        
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

                db.session.close()
                
                return {"message": "update success"}
                
                employees.close()
                db.close()
        else:
            db.session.close()

            return {"message": "Wrong username", "error": "username"}

            employees.close()
            db.close()
    else:
        db.session.close()

        return {"message": "update fail", "error": "The request payload is not in JSON format"}

        employees.close()
        db.close()

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
                
                db.session.close()

                return {"message": "delete success"}

                employees.close()
                db.close()     
        else:
            db.session.close()

            return {"message": "Wrong username", "error": "username"}    
    
            employees.close()
            db.close()
    else:
        db.session.close()

        return {"message": "delete fail", "error": "The request payload is not in JSON format"}

        employees.close()
        db.close()

        


# checkin

@app.route('/checkin', methods=['POST'])
def handle_checkin():
    checkins = CheckinModel.query.all()
    results = [
        {
            "username": checkin.username,
            "workTime": checkin.workTime,
            "checkinDate": checkin.checkinDate,
            "checkinTime": checkin.checkinTime,
            "checkoutTime": checkin.checkoutTime
        } for checkin in checkins]
    print(results[0]['username'])\

    if request.is_json:
        data = request.get_json()
        get_checkin = CheckinModel(username=data['username'], workTime=data['workTime'], checkinDate=data['checkinDate'], checkinTime=data['checkinTime'], checkoutTime=data['checkoutTime'],)
        
        data2 = [a for a in results if a['username'] == get_checkin.username]

        db.session.close()
                
        return {"count": len(results), get_checkin.username: data2, "message": "success", "error": "null"}
                
        checkins.close()
        db.close()
    else:

        db.session.close()

        return {"message": "update fail", "error": "The request payload is not in JSON format"}

        checkins.close()
        db.close()
    
@app.route('/checkin/add', methods=['POST'])
def handle_checkin_add():
    checkins = CheckinModel.query.all()
    results = [
        {
            "username": checkin.username,
            "workTime": checkin.workTime,
            "checkinDate": checkin.checkinDate,
            "checkinTime": checkin.checkinTime,
            "checkoutTime": checkin.checkoutTime
        } for checkin in checkins]
    if request.is_json:
        data = request.get_json()
        new_checkin = CheckinModel(username=data['username'], workTime=data['workTime'], checkinDate=data['checkinDate'], checkinTime=data['checkinTime'], checkoutTime=data['checkoutTime'],)
    
        for a in results:
            if new_checkin.username == a['username']:
                if new_checkin.checkinDate != a['checkinDate']:
                    print(new_checkin.checkinDate,"  +  ",a['checkinDate'])
                    continue
                else:
                    db.session.close()

                    return {"message": "CheckinDate exists", "error": "checkinDate"}
                    
                    checkins.close()
                    db.close()
            else:
                continue
        else:
            db.session.add(new_checkin)
            db.session.commit()

            db.session.close()

            return {"message": "Add success", "error": "null"}

            checkins.close()
            db.close()  
    else:
        db.session.close()

        return {"message": "add fail", "error": "The request payload is not in JSON format"}

        checkins.close()
        db.close()
        
@app.route('/checkin/update', methods=['POST'])
def handle_checkin_update():
    checkins = CheckinModel.query.all()
    results = [
        {
            "username": checkin.username,
            "workTime": checkin.workTime,
            "checkinDate": checkin.checkinDate,
            "checkinTime": checkin.checkinTime,
            "checkoutTime": checkin.checkoutTime
        } for checkin in checkins]
    if request.is_json:
        data = request.get_json()
        update_checkin = CheckinModel(username=data['username'], workTime=data['workTime'], checkinDate=data['checkinDate'], checkinTime=data['checkinTime'], checkoutTime=data['checkoutTime'],)
        for a in results:
            print(a['username'])
            if update_checkin.username == a['username']:
                if update_checkin.checkinDate == a['checkinDate']:
                    update = CheckinModel.query.filter_by(username=update_checkin.username, checkinDate=update_checkin.checkinDate).first()
                    update.workTime = update_checkin.workTime
                    update.checkinDate = update_checkin.checkinDate
                    update.checkinTime = update_checkin.checkinTime
                    update.checkoutTime = update_checkin.checkoutTime
                    
                    db.session.commit()

                    db.session.close()
                    
                    return {"message": "update success"}
                    
                    checkins.close()
                    db.close()
                else:
                    continue
        else:

            db.session.close()

            return {"message": "Wrong username", "error": "username"}

            checkins.close()
            db.close()
    else:

        db.session.close()

        return {"message": "update fail", "error": "The request payload is not in JSON format"}

        checkins.close()
        db.close()

@app.route('/checkin/delete', methods=['POST'])
def handle_checkin_delete():
    checkins = CheckinModel.query.all()
    results = [
        {
            "username": checkin.username,
            "workTime": checkin.workTime,
            "checkinDate": checkin.checkinDate,
            "checkinTime": checkin.checkinTime,
            "checkoutTime": checkin.checkoutTime
        } for checkin in checkins]
    if request.is_json:
        data = request.get_json()
        delete_checkin = CheckinModel(username=data['username'], workTime=data['workTime'], checkinDate=data['checkinDate'], checkinTime=data['checkinTime'], checkoutTime=data['checkoutTime'],)
        for a in results:
            print(a['username'], " assssssssssssss", a)
            if delete_checkin.username == a['username']:
                if delete_checkin.checkinDate == a['checkinDate']:
                    CheckinModel.query.filter_by(username=delete_checkin.username, checkinDate=delete_checkin.checkinDate).delete()
                    db.session.commit()
                    
                    db.session.close()

                    return {"message": "delete success"}

                    checkins.close()
                    db.close()
                else:
                    continue 
        else:

            db.session.close()

            return {"message": "Wrong username", "error": "username"}

            checkins.close()
            db.close()   
    else:

        db.session.close()

        return {"message": "delete fail", "error": "The request payload is not in JSON format"}

        checkins.close()
        db.close()


# calendar

@app.route('/calendar', methods=['POST'])
def handle_calendar():
    calendars = CalendarModel.query.all()
    results = [
        {
            "username": calendar.username,
            "specialDay": calendar.specialDay,
            "workDay": calendar.workDay,
            "dayOff": calendar.dayOff
        } for calendar in calendars]

    if request.is_json:
        data = request.get_json()
        get_calendar = CalendarModel(username=data['username'], specialDay=data['specialDay'], workDay=data['workDay'], dayOff=data['dayOff'])
        
        data2 = [a for a in results if a['username'] == get_calendar.username]

        db.session.close()
                
        return {"count": len(results), get_calendar.username: data2, "message": "success", "error": "null"}

        calendars.close()
        db.close()

    else:

        db.session.close()

        return {"message": "update fail", "error": "The request payload is not in JSON format"}

        calendars.close()
        db.close()
    
@app.route('/calendar/add', methods=['POST'])
def handle_calendar_add():
    calendars = CalendarModel.query.all()
    results = [
        {
            "username": calendar.username,
            "specialDay": calendar.specialDay,
            "workDay": calendar.workDay,
            "dayOff": calendar.dayOff
        } for calendar in calendars]
    if request.is_json:
        data = request.get_json()
        new_calendar = CalendarModel(username=data['username'], specialDay=data['specialDay'], workDay=data['workDay'], dayOff=data['dayOff'])
    
        for a in results:
            if new_calendar.username == a['username']:
                if new_calendar.specialDay != a['specialDay']:
                    if new_calendar.workDay != a['workDay']:
                        if new_calendar.dayOff != a['dayOff']:
                            print(new_calendar.specialDay,"  +  ",a['specialDay'])
                            continue
                        else:
                            db.session.close()

                            return {"message": "DayOff exists", "error": "dayOff"}
                            
                            calendars.close()
                            db.close()
                    else:
                        db.session.close()

                        return {"message": "WorkDay exists", "error": "workDay"}
                        
                        calendars.close()
                        db.close()
                else:
                    db.session.close()

                    return {"message": "SpecialDay exists", "error": "specialDay"}
                    
                    calendars.close()
                    db.close()
            else:
                continue
        else:
            db.session.add(new_calendar)
            db.session.commit()

            db.session.close()

            return {"message": "Add success", "error": "null"}

            calendars.close()
            db.close() 
    else:
        db.session.close()

        return {"message": "add fail", "error": "The request payload is not in JSON format"}

        calendars.close()
        db.close()
        
@app.route('/calendar/update', methods=['POST'])
def handle_calendar_update():
    calendars = CalendarModel.query.all()
    results = [
        {
            "username": calendar.username,
            "specialDay": calendar.specialDay,
            "workDay": calendar.workDay,
            "dayOff": calendar.dayOff
        } for calendar in calendars]
    if request.is_json:
        data = request.get_json()
        update_calendar = CalendarModel(username=data['username'], specialDay=data['specialDay'], workDay=data['workDay'], dayOff=data['dayOff'])
        for a in results:
            print(a['username'])
            if update_calendar.username == a['username']:
                if update_calendar.dayOff == a['dayOff']:
                    update = CalendarModel.query.filter_by(username=update_calendar.username, dayOff=update_calendar.dayOff).first()
                    update.specialDay = update_calendar.specialDay
                    update.workDay = update_calendar.workDay
                    update.dayOff = update_calendar.dayOff
                    
                    db.session.commit()

                    db.session.close()
                    
                    return {"message": "update success"}
                    
                    calendars.close()
                    db.close()
                else:
                    continue
        else:

            db.session.close()

            return {"message": "Wrong username", "error": "username"}

            calendars.close()
            db.close()
    else:

        db.session.close()

        return {"message": "update fail", "error": "The request payload is not in JSON format"}

        calendars.close()
        db.close()

@app.route('/calendar/delete', methods=['POST'])
def handle_calendar_delete():
    calendars = CalendarModel.query.all()
    results = [
        {
            "username": calendar.username,
            "specialDay": calendar.specialDay,
            "workDay": calendar.workDay,
            "dayOff": calendar.dayOff
        } for calendar in calendars]
    if request.is_json:
        data = request.get_json()
        delete_calendar = CalendarModel(username=data['username'], specialDay=data['specialDay'], workDay=data['workDay'], dayOff=data['dayOff'])
        for a in results:
            print(a['username'], " assssssssssssss", a)
            if delete_calendar.username == a['username']:
                if delete_calendar.workDay == a['workDay']:
                    CalendarModel.query.filter_by(username=delete_calendar.username, workDay=delete_calendar.workDay).delete()
                    db.session.commit()
                    
                    db.session.close()

                    return {"message": "delete success"}

                    calendars.close()
                    db.close()
                else:
                    continue     
        else:

            db.session.close()

            return {"message": "Wrong username", "error": "username"}

            calendars.close()
            db.close()   
    else:

        db.session.close()

        return {"message": "delete fail", "error": "The request payload is not in JSON format"}

        calendars.close()
        db.close()

if __name__ == '__main__':
    app.run(debug=True)
