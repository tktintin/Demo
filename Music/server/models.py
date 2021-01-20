"""Data model"""

from config import db, mm

# ********************** Table: Instrument **********************

class Instrument(db.Model):
    __tablename__ = "INSTRUMENT"
    instrument = db.Column(db.String, primary_key=True)
    category = db.Column(db.String)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    rentalFee = db.Column(db.Float)

class InstrumentSchema(mm.ModelSchema):
    class Meta:
        model = Instrument
        sqla_session = db.session


# ********************** Table: Instructor **********************

class Instructor(db.Model):
    __tablename__ = "INSTRUCTOR"
    name = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    instrument = db.Column(db.String)
    availability = db.Column(db.String)
    lessonFee = db.Column(db.Float)

class InstructorSchema(mm.ModelSchema):
    class Meta:
        model = Instructor
        sqla_session = db.session


# ********************** Table: Music Lesson **********************

class MusicLesson(db.Model):
    __tablename__ = "MUSICLESSON"
    name = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    instrument = db.Column(db.String)
    instructor = db.Column(db.String)
    status = db.Column(db.String)
    level = db.Column(db.String)
    balance = db.Column(db.Float)

class MusicLessonSchema(mm.ModelSchema):
    class Meta:
        model = MusicLesson
        sqla_session = db.session
