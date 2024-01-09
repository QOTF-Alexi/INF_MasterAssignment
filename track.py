import sqlite3


class Track:
    def __init__(self, id: int, name: str, city: str, country: str, outdoor: bool, altitude: int) -> None:
        self.id = id
        self.name = name
        self.city = city
        self.country = country
        self.outdoor = outdoor
        self.altitude = altitude

    def get_events(self) -> list:
        conn = sqlite3.connect('iceskatingapp.db')
        cursor = conn.cursor()
        query = "SELECT * FROM events WHERE track_id = ?"
        cursor.execute(query, [self.id])
        events = cursor.fetchall()
        return events

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}"
                                                               for key, value in self.__dict__.items()]))
