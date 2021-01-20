"""Flask app"""

from config import app, db
from flask import render_template, request, Flask, Response, jsonify
from flask_cors import CORS, cross_origin
from models import Instrument, InstrumentSchema, Instructor, InstructorSchema, MusicLesson, MusicLessonSchema
from sqlalchemy.exc import IntegrityError, InvalidRequestError
import sqlite3
import json, pyjokes
import random

# app = Flask(__name__)
# CORS(app)

# ************************************ Function: Get data from database ************************************

def get_data_from_db(query: str):
    # retrieve data from the database and return to the user
    conn = sqlite3.connect("music.sqlite3")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows


# ************************************ instrument list ************************************

instrumentLst = []
dropdown = get_data_from_db(query = "SELECT instrument FROM instrument;")

for row in dropdown:
    for col in row:
        instrumentLst.append(col)


# ************************************ index: API documentation ************************************

@app.route("/")
def welcome():
    return render_template("index.html")


# ************************************ Instrument inventory page ************************************

@app.route("/instrument", methods=["GET", "POST"])
def instrument():

    error = None

    if request.method == "POST":
        if request.form["submit"] == "Add":
            db.session.query(Instrument).filter(Instrument.instrument == request.form.get("instrument")).update({Instrument.quantity : Instrument.quantity + 1})
            db.session.commit()
            error = False
        elif request.form["submit"] == "Remove":
            if db.session.query(Instrument).filter(Instrument.instrument == request.form.get("instrument"), Instrument.quantity == 0).all():
                error = True
            else:
                db.session.query(Instrument).filter(Instrument.instrument == request.form.get("instrument")).update({Instrument.quantity : Instrument.quantity - 1})
                db.session.commit()
                error = False

    selected = request.form.get("instrument")

    instru = Instrument.query.all()
    instrument_schema = InstrumentSchema(many=True)
    return render_template("instrument.html", instru=instrument_schema.dump(instru), error=error, instrumentLst=instrumentLst, selected=selected)


# ************************************ Instructor Info page ************************************

@app.route("/instructor", methods=["GET", "POST"])
def instructor():
    if request.method == "GET":
        instruct = Instructor.query.all()
        instructor_schema = InstructorSchema(many=True)
        return render_template("instructor.html", instruct=instructor_schema.dump(instruct))


# ************************************ Music Lesson Info page ************************************

@app.route("/musiclesson", methods=["GET", "POST"])
def musiclesson():

    paymentError = None
    cancelError = None
    selected = None
    studentLst = []

    dropdown = get_data_from_db(query = "SELECT name FROM musiclesson;")

    for row in dropdown:
        for col in row:
            studentLst.append(col)

    if request.method == "POST":

        selected = request.form.get("name")

        balanceLst = []

        balance = get_data_from_db(query = f"SELECT balance FROM musiclesson WHERE name = '{selected}';")
        for row in balance:
            for col in row:
                balanceLst.append(col)
        
        if request.form["submit"] == "Make Payment":

            payment = request.form.get("payment")

            updatedBalance = float(balanceLst[0]) - float(payment)
            
            if float(payment) <= float(balanceLst[0]) and float(payment) != 0:
                db.session.query(MusicLesson).filter(MusicLesson.name == request.form.get("name")).update({MusicLesson.balance : updatedBalance})
                db.session.commit()
                paymentError = False
            elif float(payment) == 0.0:
                paymentError = None
            else:
                paymentError = True
        
        if request.form["submit"] == "Cancel Lesson":

            if float(balanceLst[0]) == 0.0:
                db.session.query(MusicLesson).filter(MusicLesson.name == request.form.get("name")).delete()
                db.session.commit()
                cancelError = False
            else:
                cancelError = True

    musiclesson = MusicLesson.query.all()
    musiclesson_schema = MusicLessonSchema(many=True)
    return render_template("musiclesson.html", musiclesson=musiclesson_schema.dump(musiclesson), paymentError = paymentError, cancelError = cancelError, studentLst = studentLst, selected = selected)


# ************************************ Music Lesson Scheduling page ************************************

@app.route("/schedule", methods=["GET", "POST"])
def schedule():
    selected = {}
    activateRequired = False
    error = None
    table = False
    availabilityError = False
    instructorLst = []

    if request.method == "POST":

        dropdown = get_data_from_db(query = f"SELECT name FROM instructor WHERE instrument == '{request.form.get('instrument')}';")
        for row in dropdown:
            for col in row:
                instructorLst.append(col)

        if request.form["submit"] == "Find Lesson" and request.form.get('name') and request.form.get('email') and request.form.get('instrument'):
            newName = request.form.get('name')
            newEmail = request.form.get('email')
            newInstrument = request.form.get('instrument')

            selected = {"name" : newName,
                        "email" : newEmail,
                        "instrument" : newInstrument}

            findInstructor = db.session.query(Instructor).filter(Instructor.instrument == request.form.get("instrument")).all()
            instructor_schema = InstructorSchema(many=True)
            if findInstructor:
                availableInstructor = True
                activateRequired = True
            else:
                availableInstructor = False
                activateRequired = False
            return render_template("schedule.html", instructorLst = instructorLst, findInstructor=instructor_schema.dump(findInstructor), availableInstructor = availableInstructor, selected = selected, instrumentLst=instrumentLst,  activateRequired = activateRequired)
        
        if request.form["submit"] == "Confirm" and request.form.get('name') and request.form.get('email') and request.form.get('instrument') and request.form.get('instructor'):
            
            newName = request.form.get('name')
            newEmail = request.form.get('email')
            newInstrument = request.form.get('instrument')
            newInstructor = request.form.get('instructor')
            newStatus = request.form.get('status')
            newLevel = request.form.get('level')

            selected = {"name" : newName,
                        "email" : newEmail,
                        "instrument" : newInstrument,
                        "instructor" : newInstructor,
                        "status" : newStatus,
                        "level" : newLevel}

            newBalance = 0.0

            rentalCost = []
            rc = get_data_from_db(query = f"SELECT rentalFee FROM instrument WHERE instrument == '{newInstrument}';")
            for row in rc: 
                for col in row: 
                    rentalCost.append(col)

            fullCost = []
            fc = get_data_from_db(query = f"SELECT price FROM instrument WHERE instrument == '{newInstrument}';")
            for row in fc: 
                for col in row: 
                    fullCost.append(col)

            lessonCost = []
            lc = get_data_from_db(query = f"SELECT lessonFee FROM instructor WHERE name == '{newInstructor}';")
            for row in lc:
                for col in row: 
                    lessonCost.append(col)

            if newStatus == "Rental":
                newBalance += rentalCost[0]
                if db.session.query(Instrument).filter(Instrument.instrument == request.form.get("instrument"), Instrument.quantity == 0).all():
                    availabilityError = True
                else:
                    db.session.query(Instrument).filter(Instrument.instrument == request.form.get("instrument")).update({Instrument.quantity : Instrument.quantity - 1})
                    db.session.commit()
                    availabilityError = False

            if newStatus == "Purchase":
                newBalance += fullCost[0]
                if db.session.query(Instrument).filter(Instrument.instrument == request.form.get("instrument"), Instrument.quantity == 0).all():
                    availabilityError = True
                else:
                    db.session.query(Instrument).filter(Instrument.instrument == request.form.get("instrument")).update({Instrument.quantity : Instrument.quantity - 1})
                    db.session.commit()
                    availabilityError = False
            
            newBalance += lessonCost[0]

            if availabilityError == False:

                try:
                    lesson = MusicLesson(
                                        name = newName,
                                        email = newEmail,
                                        instrument = newInstrument,
                                        instructor = newInstructor,
                                        status = newStatus,
                                        level = newLevel,
                                        balance = newBalance
                                    )
                    db.session.add(lesson)
                    db.session.commit()
                    error = False
                    table = True

                except IntegrityError or InvalidRequestError:
                    error = True
                    table = True
                    db.session.rollback()

            musiclesson = MusicLesson.query.filter(MusicLesson.name == request.form.get("name")).all()
            musiclesson_schema = MusicLessonSchema(many=True)
            return render_template("schedule.html", instructorLst = instructorLst, availabilityError = availabilityError, instrumentLst=instrumentLst, musiclesson=musiclesson_schema.dump(musiclesson), selected = selected, error = error, table = table)

    return render_template("schedule.html", instructorLst = instructorLst, instrumentLst = instrumentLst, selected = selected)


# ************************************ API ************************************

instrumentInfoLst = []
info = get_data_from_db(query = "SELECT * FROM instrument;")
for row in info:
    instrumentInfoLst.append(row)

dict = {}
for i in instrumentInfoLst:
    dict[i[0]] = {"name": i[0], "category": i[1], "quantity": i[2], "price": i[3], "rental fee": i[4]}

@app.route("/api/instruments")
def get_all_instruments():
    res = Response(json.dumps({"inventory": dict}))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/api/instruments/<string:name>")
@cross_origin()
def get_specific_instrument(name):
    try:
        res = Response(json.dumps({name: dict[name]}))
        res.headers["Content-Type"] = "application/json"
        return res
    except:
        return "404 Not Found"

@app.route("/api/instruments/random")
@cross_origin()
def get_random():
    randomInstrument = random.choice(list(dict.keys()))
    res = Response(json.dumps({"random": dict[randomInstrument]}))
    res.headers["Content-Type"] = "application/json"
    return res

if __name__ == "__main__":
    app.run("0.0.0.0")
