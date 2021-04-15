from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://root@127.0.0.1:3306/schedule'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

HOST = '0.0.0.0'
PORT = 5004 


class Schedule(db.Model):
    __tablename__ = 'schedule'
    SID=db.Column(db.Integer, primary_key=True, nullable=False)
    driver_ID = db.Column(db.Integer, nullable=False)
    delivery_date = db.Column(db.Date, nullable=False)
    t_8_to_10 = db.Column(db.Boolean, nullable=False)
    t_10_to_12 = db.Column(db.Boolean, nullable=False)
    t_12_to_2 = db.Column(db.Boolean, nullable=False)
    t_2_to_4 = db.Column(db.Boolean, nullable=False)
    t_4_to_6 = db.Column(db.Boolean, nullable=False)

    __table_args__ = (
        db.UniqueConstraint('driver_ID', 'delivery_date', name='_driver_dd_uc'),
    )
    
    def __init__(self, SID, driver_ID, delivery_date, t_8_to_10, t_10_to_12, t_12_to_2, t_2_to_4, t_4_to_6):
        self.SID = SID
        self.driver_ID = driver_ID
        self.delivery_date = delivery_date
        self.t_8_to_10 = t_8_to_10
        self.t_10_to_12 = t_10_to_12
        self.t_12_to_2 = t_12_to_2
        self.t_2_to_4 = t_2_to_4
        self.t_4_to_6 = t_4_to_6

    def json(self):
        return {
            "SID": self.SID,
            "driver_ID": self.driver_ID,
            "delivery_date": self.delivery_date,
            "t_8_to_10": self.t_8_to_10,
            "t_10_to_12": self.t_10_to_12,
            "t_12_to_2": self.t_12_to_2,
            "t_2_to_4": self.t_2_to_4,
            "t_4_to_6": self.t_4_to_6,
        }

# 1. Get a specific schedule by SID
@app.route("/schedule/<int:SID>")
def find_by_SID(SID):
    schedule = Schedule.query.filter_by(SID=SID).first()
    if schedule:
        return jsonify(
            {
                "code": 200,
                "data": schedule.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Schedule not found."
        }
    ), 404

# 2. get schedule by driver
@app.route("/schedule/driver/<int:driver_ID>")
def find_by_driver(driver_ID):
    schedule_list = Schedule.query.filter_by(driver_ID=driver_ID).order_by(Schedule.delivery_date).all()
    if len(schedule_list) > 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "schedules": [schedule.json() for schedule in schedule_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Schedule not found."
        }
    ), 404

#3. get schedule by delivery date
@app.route("/schedule/date/<string:delivery_date>")
def find_by_date(delivery_date):
    schedule_list = Schedule.query.filter_by(delivery_date=delivery_date).all()

    if len(schedule_list) > 0:
        return jsonify(
            {
                "code": 200,
                "data": {
                    "schedules": [schedule.json() for schedule in schedule_list]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No available timing for this day."
        }
    ), 404

#4. get schedule by delivery date + TIMESLOT
@app.route('/schedule/date/<string:delivery_date>/<string:timeslot>', methods=['GET'])
def timeslot_query(delivery_date, timeslot):
    first_filter = Schedule.query.filter_by(delivery_date=delivery_date).all()

    if len(first_filter)==0:
        return jsonify(
            {
                "code": 404,
                "message": "No schedule with the provided date."
            }
        ), 404

    timeslots_list=['8_to_10', '10_to_12', '12_to_2', '2_to_4', '4_to_6']
    if timeslot in timeslots_list:
        if timeslot=='8_to_10':
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_8_to_10=0).all()
        elif timeslot=='10_to_12':
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_10_to_12=0).all()
        elif timeslot=='12_to_2':
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_12_to_2=0).all()
        elif timeslot=='2_to_4':
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_2_to_4=0).all()
        elif timeslot=='4_to_6':
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_4_to_6=0).all()

        if len(second_filter) > 0:
            return jsonify(
                {
                    "code": 200,
                    "data": {
                        "schedules": [schedule.json() for schedule in second_filter]
                    }
                }
            )

        else: 
            return jsonify(
            {
                "code": 404,
                "message": "No driver is available at this timeslot."
            }
        ), 404

    else:
        return jsonify(
                {
                    "code": 400,
                    "data": {
                        "timeslot": timeslot
                    },
                    "message": "Invalid timeslot provided"
                }
            ), 400


# 5. Update a schedule
@app.route("/schedule/<int:SID>", methods=['PUT'])
def update_schedule(SID):
    old_schedule = Schedule.query.filter_by(SID=SID).first()
    if not old_schedule:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "SID": SID
                },
                "message": "Schedule does not exist."
            }
        ), 400

    data = request.get_json()
    new_schedule = Schedule(SID, **data)

    try:
        old_schedule.SID = new_schedule.SID
        old_schedule.driver_ID = new_schedule.driver_ID
        old_schedule.delivery_date = new_schedule.delivery_date
        old_schedule.t_8_to_10 = new_schedule.t_8_to_10
        old_schedule.t_10_to_12 = new_schedule.t_10_to_12
        old_schedule.t_12_to_2 = new_schedule.t_12_to_2
        old_schedule.t_2_to_4 = new_schedule.t_2_to_4
        old_schedule.t_4_to_6 = new_schedule.t_4_to_6
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "SID": SID
                },
                "message": "An error occurred updating the schedule."
            }
        ), 500
    
    return jsonify(
        {
            "code": 202,
            'data': old_schedule.json(),
            "message": "Schedule has successfully been updated."
        }
    ), 202


# 6. create schedules for the rest of the month (April), for the driver that was newly added
@app.route("/schedule/new_driver/<int:driver_ID>", methods=['POST'])
def add_schedules_for_month(driver_ID):
    data = request.get_json()
    today_date = data['today_date']

    schedule = Schedule.query.filter_by(driver_ID=driver_ID).first()
    if schedule:
        return jsonify({
            "code": 400,
            'data': schedule.json(),
            "message": "Driver schedule already exists."
        })

    year_and_month='2021-04-'
    schedule = Schedule.query.order_by(Schedule.SID.desc()).first()
    if (schedule):
        SID = schedule.SID + 1
    else:
        SID = 1
    current_day = int(today_date[-2:])
    
    timeslots = {
        "t_8_to_10": False,
        "t_10_to_12": False,
        "t_12_to_2": False,
        "t_2_to_4": False,
        "t_4_to_6": False
    }

    schedule_list=[]

    for i in range (current_day, 31):
        current_date=str(i)    #date of submission: 15 April, can pick until 30 April
        delivery_date = year_and_month + current_date
        schedule= Schedule(SID, driver_ID, delivery_date, **timeslots)

        try:
            db.session.add(schedule)
            db.session.commit()
            schedule_list.append(schedule)
            SID+=1

        except:
            return jsonify(
            {
                "code": 500,
                "data": {
                    "SID": SID
                },
                "message": "An error occurred creating the schedule."
            }
        ), 500
    
    return jsonify(
        {
            "code": 201,
            'data': [schedule.json() for schedule in schedule_list]
        }
    ), 201

if __name__ =='__main__':
    app.run(host=HOST, port=PORT, debug=True)
    print(f'App running on {HOST}:{PORT}')
