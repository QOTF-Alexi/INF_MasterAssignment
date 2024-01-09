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

    def add_skater(self, skater: Skater):
        # Why are these unresolved?
        conn = sqlite3.connect('iceskatingsapp.db')
        query = """
INSERT INTO event_skaters (skater_id, event_id)
SELECT ?, ?
WHERE NOT EXISTS (SELECT 1 FROM event_skaters WHERE skater_id = ? AND event_id = ?)
                """
        # Why is it not using a cursor?
        conn.execute(query, [skater.id, self.id, skater.id, self.id])
        conn.commit()

    def get_skaters(self) -> list:
        conn = sqlite3.connect('iceskatingapp.db')
        cursor = conn.cursor()
        cursor.execute(f"""
SELECT * FROM skaters WHERE id IN (SELECT skater_id FROM event_skaters WHERE event_id = {self.id})
                        """)
        fetch_skaters = cursor.fetchall()
        return fetch_skaters

    def get_track(self) -> Track:
        # Get track for this event.
        pass

    def convert_date(self, to_format: str) -> str:
        return datetime.strftime(self.date, to_format)

    def convert_duration(self, to_format: str) -> str:
        # self.duration is noted in M:SS:mmm
        pass

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}"
                                                               for key, value in self.__dict__.items()]))
