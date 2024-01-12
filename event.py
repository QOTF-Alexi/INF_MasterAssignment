from datetime import datetime, timedelta
import sqlite3

from skater import Skater
from track import Track


class Event:
    def __init__(self, id: int, name: str, track_id: int, date: datetime, distance: int, duration: float, laps: int,
                 winner: str, category: str) -> None:
        self.id = id
        self.name = name
        self.track_id = track_id
        self.date = date
        self.distance = distance
        self.duration = duration
        self.laps = laps
        self.winner = winner
        self.category = category

    # Connect a skater to this event
    def add_skater(self, skater: Skater):
        conn = sqlite3.connect('iceskatingsapp.db')
        cursor = conn.cursor()
        cursor.execute(f"""
INSERT INTO event_skaters(skater_id, event_id)
VALUES (?, ?)""", (skater.id, self.id))
        conn.commit()

    # Gets skaters that participate in this event.
    def get_skaters(self) -> list:
        conn = sqlite3.connect('iceskatingapp.db')
        cursor = conn.cursor()
        cursor.execute(f"""
SELECT * FROM skaters WHERE id IN (SELECT skater_id FROM event_skaters WHERE event_id = {self.id})
                        """)
        fetch_skaters = cursor.fetchall()
        return fetch_skaters

    # Gets track object where id matches track_id of the event.
    def get_track(self) -> Track:
        conn = sqlite3.connect('iceskatingsapp.db')
        cursor = conn.cursor()
        cursor.execute(f"""SELECT * FROM tracks WHERE id = {self.track_id}""")
        track = cursor.fetchone()
        return Track(*track)

    # Converts date to specified format.
    def convert_date(self, to_format: str) -> str:
        return datetime.strftime(self.date, to_format)

    # Converts event duration to specified format.
    def convert_duration(self, to_format: str) -> str:
        converted = datetime.strptime(str(self.duration), "%S.%f")
        return converted.strftime(to_format)

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}"
                                                               for key, value in self.__dict__.items()]))
