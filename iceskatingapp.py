import os
import sys
import json
import sqlite3

from skater import Skater
from track import Track
from event import Event


def read_json_file():
    jsonFile = open('events.json', encoding="utf8")
    events_data_dict = json.load(jsonFile)
    jsonFile.close()
    return events_data_dict


def configure_database(data):
    tracks = [event['track'] for event in data]
    set_tracks(tracks, data)


def set_tracks(tracks: list, data):
    conn = sqlite3.connect(os.path.join(sys.path[0], 'iceskatingapp.db'))
    conn.set_trace_callback(print)
    for track in tracks:
        query = f"""
INSERT INTO tracks (`id`, `name`, `city`, `country`, `outdoor`, `altitude`)
SELECT NULL, ?, ?, ?, ?, ?
WHERE NOT EXISTS (SELECT 1 FROM tracks WHERE `name` LIKE '%{track['name']}%');
                 """
        values = [
            track['name'],
            track['city'],
            track['country'],
            track['isOutdoor'],
            track['altitude']
        ]
        executedQuery = conn.execute(query, values)
        conn.commit()
        set_event(data, track['name'], executedQuery.lastrowid, conn)


def set_event(data, trackName, trackId, conn):
    for event in data:
        if event['track']['name'] == trackName:
            query = f"""
INSERT INTO events (`id`, `name`, `track_id`, `date`, `distance`, `duration`, `laps`, `winner`, `category`)
SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?
WHERE NOT EXISTS (SELECT 1 FROM events WHERE id = {event['id']})
                     """
            values = [
                event['id'],
                event['name'],
                trackId,
                event['date'],
                event['distance'],
                event['duration'],
                event['laps'],
                event['winner'],
                event['category']
            ]
            conn.execute(query, values)
            conn.commit()
            set_skaters(conn, data, event)


def set_skaters(conn, data, event):
    for skater in event['skaters']:
        query = f"""
INSERT OR IGNORE INTO skaters (id, first_name, last_name, nationality, gender, date_of_birth)
SELECT ?, ?, ?, ?, ?, ?
WHERE NOT EXISTS (SELECT 1 FROM skaters WHERE id = {event['id']})
                 """
        values = [
            skater['id'],
            skater['first_name'],
            skater['last_name'],
            skater['nationality'],
            skater['gender'],
            skater['date_of_birth']
        ]
        for value in values:
            print(type(value))
        return
        conn.execute(query, values)
        set_event_skater(conn, skater['id'], event['id'])


def set_event_skater(conn, skaterId, eventId):
    query = """
        INSERT INTO event_skaters (skater_id, event_id)
        SELECT ?, ?
        WHERE NOT EXISTS (SELECT 1 FROM event_skaters WHERE skater_id = ? AND event_id = ?)
    """
    conn.execute(query, [skaterId, eventId, skaterId, eventId])
    conn.commit()


def truncate_table():
    conn = sqlite3.connect(os.path.join(sys.path[0], 'skatersapp.db'))
    conn.set_trace_callback(print)
    cursor = conn.cursor()
    conn.execute("DELETE FROM skaters")
    conn.execute("DELETE FROM event_skaters")
    conn.execute("DELETE FROM events")
    conn.execute("DELETE FROM tracks")
    conn.commit()
    conn.close()

def main():
    data = read_json_file()
    configure_database(data)
    # truncate_table()
    # print(data)


if __name__ == "__main__":
    main()
