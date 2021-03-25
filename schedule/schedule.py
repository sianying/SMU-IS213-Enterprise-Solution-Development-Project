from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/schedule_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

HOST = '0.0.0.0'
PORT = 5004 # shouldn't clash with other services when running locally


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

# 1. Return all schedules
@app.route("/schedule")
def get_all():
    schedule_list = Schedule.query.all()
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
            "code": 400,
            "message": "There are no schedules recorded."
        }
    ), 400

# 2. Get a specific schedule by SID
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

# 3. get schedule by driver
@app.route("/schedule/driver/<int:driver_ID>")
def find_by_driver(driver_ID):
    schedule_list = Schedule.query.filter_by(driver_ID=driver_ID).all()
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

#4. get schedule by delivery date
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
            "message": "Schedule not found."
        }
    ), 404

#5. get schedule by delivery date + TIMESLOT
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
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_8_to_10=1).all()
        elif timeslot=='10_to_12':
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_10_to_12=1).all()
        elif timeslot=='12_to_2':
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_12_to_2=1).all()
        elif timeslot=='2_to_4':
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_2_to_4=1).all()
        elif timeslot=='4_to_6':
            second_filter = Schedule.query.filter_by(delivery_date=delivery_date).filter_by(t_4_to_6=1).all()

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
    
    return 'noob'

# 5. get schedule by timeslots, input must be a list!  example-> timeslots=[8_to_10,10_to_12]
# @app.route('/schedule?timeslots=<string:timeslots>', methods=['GET'])
# def timeslot_query(timeslots):
    
#     timeslots = timeslots[1:-1].split(',')

#     for timeslot in timeslots:
#         if timeslot not in timeslot_to_column_map:
#             return jsonify(
#                 {
#                     "code": 400,
#                     "data": {
#                         "timeslot": timeslot
#                     },
#                     "message": "Invalid timeslot provided"
#                 }
#             ), 400

#     conditions = []
#     for timeslot in timeslots:
#         column_reference = timeslot_to_column_map[timeslot]
#         conditions.append(column_reference.is_(True))

#     schedules = Schedule.query.filter.and(()).all()
#     return jsonify(
#         {
#             "code": 200,
#             "data": {
#                 "schedules": [schedule.json() for schedule in schedules]
#             }
#         }
#     )

# 6. Create a new schedule
@app.route("/schedule", methods=['POST'])
def create_schedule():  #create_schedule(SID)
    # if Schedule.query.filter_by(SID=SID).first():
    #     return jsonify(
    #         {
    #             "code": 400,
    #             "data": {
    #                 "SID": SID
    #             },
    #             "message": "Schedule already exists."
    #         }
    #     ), 400

    schedule = Schedule.query.order_by(Schedule.SID.desc()).first()
    SID= schedule.SID + 1
    
    data = request.get_json()
    schedule = Schedule(SID, **data)

    try:
        db.session.add(schedule)
        db.session.commit()
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
            'data': schedule.json()
        }
    ), 201

# 7. Delete a schedule
@app.route("/schedule/<int:SID>", methods=['DELETE'])
def delete_schedule(SID):
    schedule = Schedule.query.filter_by(SID=SID).first()
    if not schedule:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "SID": SID
                },
                "message": "This schedule does not exist."
            }
        ), 400

    try:
        db.session.delete(schedule)
        db.session.commit()
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
            "code": 203,
            'data': schedule.json(),
            "message": "Schedule has successfully been deleted."
        }
    ), 203

# 8. Update a schedule
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


# timeslot_to_column_map = {
#     '8_to_10': Schedule.t_8_to_10,
#     '10_to_12': Schedule.t_10_to_12,
#     '12_to_2': Schedule.t_12_to_2,
#     '2_to_4': Schedule.t_2_to_4,
#     '4_to_6': Schedule.t_4_to_6,
# }


if __name__ =='__main__':
    app.run(host=HOST, port=PORT, debug=True)
    print(f'App running on {HOST}:{PORT}')
