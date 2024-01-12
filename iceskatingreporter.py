from track import Track
from event import Event
from skater import Skater

from datetime import datetime
import sqlite3
import csv
from os.path import exists


class Reporter:
    def __init__(self):
        self.conn = sqlite3.connect("iceskatingapp.db")
        self.cursor = (self.conn.cursor())

    # How many skaters are there? -> int
    def total_amount_of_skaters(self) -> int:
        self.cursor.execute("""SELECT * FROM skaters""")
        skaters = self.cursor.fetchall()
        return len(skaters)

    # What is the highest track? -> Track
    def highest_track(self) -> Track:
        self.cursor.execute("""SELECT * FROM tracks WHERE altitude = (SELECT MAX(altitude) FROM tracks)""")
        track = self.cursor.fetchone()
        return Track(*track)

    # What is the longest and shortest event? -> tuple[Event, Event]
    def longest_and_shortest_event(self) -> tuple[Event, Event]:
        self.cursor.execute("""SELECT * FROM events WHERE duration = (SELECT MAX(duration) FROM events)""")
        longest = self.cursor.fetchone()
        longest_evnt = Event(*longest)
        self.cursor.execute("""SELECT * FROM events WHERE duration = (SELECT MIN(duration) FROM events)""")
        shortest = self.cursor.fetchone()
        shortest_evnt = Event(*shortest)
        return tuple((longest_evnt, shortest_evnt))

    # Which event has the most laps for the given track_id -> tuple[Event, ...]
    def events_with_most_laps_for_track(self, track_id: int) -> tuple[Event, ...]:
        self.cursor.execute(f"""SELECT * FROM events WHERE track_id = {track_id}
                                AND laps = (SELECT MAX(laps) FROM events)""")
        events = self.cursor.fetchall()
        events_tup = []
        for row in events:
            events_tup.append(Event(*row))
        return tuple(events_tup)

    # Which skaters have made the most events -> tuple[Skater, ...]
    # Which skaters have made the most succesful events -> tuple[Skater, ...]
    def skaters_with_most_events(self, only_wins: bool = False) -> tuple[Skater, ...]:
        self.cursor.execute(f"""SELECT * FROM skaters""")
        allSkaters = self.cursor.fetchall()
        maxCount = 0
        maxId = []
        if only_wins:
            for skater in allSkaters:
                self.cursor.execute(f"""SELECT * FROM events WHERE winner = {" ".join([skater[1], skater[2]])}""")
                won_on = len(self.cursor.fetchall())
                if won_on > maxCount:
                    maxId.clear()
                    maxId.append(skater[0])
                    maxCount = won_on
        else:
            for skater in allSkaters:
                self.cursor.execute(f"""SELECT * FROM event_skaters WHERE skater_id = {skater[0]}""")
                skated_on = len(self.cursor.fetchall())
                if skated_on > maxCount:
                    maxId.clear()
                    maxId.append(skater[0])
                    maxCount = skated_on
        self.cursor.execute(f"""SELECT * FROM skaters WHERE id IN {maxId}""")
        skatedMost = self.cursor.fetchall()
        skatedMost_tup = []
        for row in skatedMost:
            skatedMost_tup.append(Skater(*row))
        return tuple(skatedMost)

    # Which track has the most events -> Track
    def tracks_with_most_events(self) -> tuple[Track, ...]:
        maxEventCount = 0
        maxTrackId = []
        self.cursor.execute("""SELECT COUNT(*) FROM tracks""")
        number_of_tracks = self.cursor.fetchone()
        for track in number_of_tracks:
            # Assuming sequential numbering
            self.cursor.execute(f"""SELECT COUNT(*) FROM events WHERE track_id = {track}""")
            currentEventCount = self.cursor.fetchone()
            if currentEventCount > maxEventCount:
                maxEventCount = currentEventCount
                maxTrackId = [track]
            elif currentEventCount == maxEventCount and track not in maxTrackId:
                maxTrackId.append(track)
        maxTrackNames = []
        iteration = 0
        while iteration < (len(maxTrackId) - 1):
            self.cursor.execute(f"""SELECT * FROM tracks WHERE track_id = {maxTrackId[iteration]}""")
            maxTrackNames.append(self.cursor.fetchone())
            iteration += 1
        return tuple(maxTrackNames)

    # Which track had the first event? -> Event
    # Which track had the first outdoor event? -> Event
    def get_first_event(self, outdoor_only: bool = False) -> Event:
        if outdoor_only:
            self.cursor.execute(f""" SELECT * FROM tracks WHERE outdoor = 1""")
            outdoorEvents = self.cursor.fetchall()
            outdoorEvents_trackIds = []
            for element in outdoorEvents:
                outdoorEvents_trackIds.append(element[0])
            self.cursor.execute(f"""SELECT * FROM events WHERE date = (SELECT MIN(date) FROM events)
                                    AND track_id IN {outdoorEvents_trackIds}""")
            firstEvent = self.cursor.fetchone()
        else:
            self.cursor.execute(f""" SELECT * FROM events WHERE date = (SELECT MIN(date) FROM events)""")
            firstEvent = self.cursor.fetchone()
        return Event(*firstEvent)

    # Which track had the latest event? -> event
    # Which track had the latetstoutdoor event? -> event
    def get_latest_event(self, outdoor_only: bool = False) -> Event:
        if outdoor_only:
            self.cursor.execute(f""" SELECT * FROM tracks WHERE outdoor = 1""")
            outdoorEvents = self.cursor.fetchall()
            outdoorEvents_trackIds = []
            for element in outdoorEvents:
                outdoorEvents_trackIds.append(element[0])
            self.cursor.execute(f"""SELECT * FROM events WHERE date = (SELECT MAX(date) FROM events)
                                    AND track_id IN {outdoorEvents_trackIds}""")
            firstEvent = self.cursor.fetchone()
        else:
            self.cursor.execute(f""" SELECT * FROM events WHERE date = (SELECT MAX(date) FROM events)""")
            firstEvent = self.cursor.fetchone()
        return Event(*firstEvent)

    # Which skaters have raced track Z between period X and Y? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters on Track Z between X and Y.csv`
    # example: `Skaters on Track Kometa between 2021-03-01 and 2021-06-01.csv`
    # date input always in format: YYYY-MM-DD
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    #   id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_that_skated_track_between(self, track: Track, start: datetime, end: datetime, to_csv: bool = False) -> tuple[Skater, ...]:
        pass

    # Which tracks are located in country X? ->tuple[Track, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Tracks in country X.csv`
    # example: `Tracks in Country USA.csv`
    # otherwise it should just return the value as tuple(Track, ...)
    # CSV example (this are also the headers):
    #   id, name, city, country, outdoor, altitude
    def get_tracks_in_country(self, country: str, to_csv: bool = False) -> tuple[Track, ...]:
        self.cursor.execute("""SELECT * FROM tracks WHERE country = ?""", country)
        tracks = self.cursor.fetchall()
        if to_csv:
            csvname = "".join(['Tracks in country ', country, '.csv'])
            if not exists(csvname):
                with open(csvname, 'w', newline='') as csvfile:
                    trackFile = csv.writer(csvfile, delimiter=' ', encoding='utf8')
                    trackFile.writerow(['id', 'name', 'city', 'country', 'outdoor', 'altitude'])
            with open(csvname, 'w', newline='') as csvfile:
                trackFile = csv.writer(csvfile, delimiter=' ', encoding='utf8')
                for track in tracks:
                    trackFile.writerow(track)
            print("File saved as", csvname)
        else:
            track_tup = []
            for row in tracks:
                track_tup.append(Track(*row))
            return tuple(track_tup)

    # Which skaters have nationality X? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters with nationality X.csv`
    # example: `Skaters with nationality GER.csv`
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    #   id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_with_nationality(self, nationality: str, to_csv: bool = False) -> tuple[Skater, ...]:
        self.cursor.execute("""SELECT * FROM skaters WHERE nationality = ?""", nationality)
        skaters = self.cursor.fetchall()
        if to_csv:
            csvname = "".join(['Skaters with nationality ', nationality, '.csv'])
            if not exists(csvname):
                with open(csvname, 'w', newline='') as csvfile:
                    skatersFile = csv.writer(csvfile, delimiter=' ', encoding='utf8')
                    skatersFile.writerow(['id', 'first_name', 'last_name', 'nationality', 'gender', 'date_of_birth'])
            with open(csvname, 'w', newline='') as csvfile:
                skatersFile = csv.writer(csvfile, delimiter=' ', encoding='utf8')
                for skater in skaters:
                    skatersFile.writerow(skater)
            print("File saved as", csvname)
        else:
            return tuple(skaters)
