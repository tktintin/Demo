"""Building the DB"""

import csv
import os
from config import db
from models import Instrument, Instructor, MusicLesson


def build_db():
    # Delete existing DB
    if os.path.exists("music.sqlite3"):
        os.remove("music.sqlite3")

    # Create an empty DB
    db.create_all()

    # Add existing data to the DB (from csv file)
    with open("csv/instrument.csv") as f:
        content = csv.reader(f)
        next(content)
    
        for line in content:
            instrument = Instrument(
                instrument = line[0],
                category = line[1],
                quantity = line[2],
                price = line[3],
                rentalFee = line[4]
            )
            db.session.add(instrument)
        db.session.commit()

    with open("csv/instructor.csv") as f:
        content = csv.reader(f)
        next(content)
    
        for line in content:
            instructor = Instructor(
                name = line[0],
                email = line[1],
                instrument = line[2],
                availability = line[3],
                lessonFee = line[4]
            )
            db.session.add(instructor)
        db.session.commit()
    
    with open("csv/musiclesson.csv") as f:
        content = csv.reader(f)
        next(content)

        for line in content:
            musiclesson = MusicLesson(
                name = line[0],
                email = line[1],
                instrument = line[2],
                instructor = line[3],
                status = line[4],
                level = line[5],
                balance = line[6]
            )
            db.session.add(musiclesson)
        db.session.commit()

def main():
    build_db()

if __name__ == "__main__":
    main()
