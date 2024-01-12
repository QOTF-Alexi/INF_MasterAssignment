import json
import sqlite3


# This function will open the JSON file and save it in a dictionary.
def read_json_file():
    json_file = open('events.json', encoding="utf8")
    events_data_dict = json.load(json_file)
    json_file.close()
    return events_data_dict


# This function will create or update all the database tables.
# It will also initialize all the required classes.
def configure_database(data):
    conn = sqlite3.connect("iceskatingapp.db")
    cursor = conn.cursor()
    for event in data:
        event_id = event["id"]
        event_title = event["title"]
        event_date = event["start"]
        event_distance_dict = event["distance"]
        event_distance = event_distance_dict["distance"]
        event_lapcount = event_distance_dict["lapCount"]
        event_category = event["category"]

        event_track_dict = event["track"]
        event_track_id = event_track_dict["id"]
        event_track_name = event_track_dict["name"]
        event_track_city = event_track_dict["city"]
        event_track_country = event_track_dict["country"]
        event_track_outdoor = event_track_dict["isOutdoor"]
        event_track_alt = event_track_dict["altitude"]

        event_result_list = event["results"]
        event_winner = event_result_list[0]
        event_winner_info = event_winner["skater"]
        event_winner_name = " ".join([event_winner_info["firstName"], event_winner_info["lastName"]])

        selector = -1
        event_last = event_result_list[selector]
        while event_last["time"] is None:
            # Ignore did-not-finish results
            selector -= 1
            event_last = event_result_list[selector]
        event_time = event_last["time"]
        event_time_split = event_time.split(sep=":")
        if len(event_time) == 2:
            # Convert minutes into seconds and add up
            event_time_split[1] = float(event_time_split[1]) + float(event_time_split[0]) * 60.000
            event_time_split.remove(event_time_split[0])
        else:
            # No minutes, so no conversion required
            pass
        event_time_seconds = event_time_split[0]      # Float value

        for skater in event_result_list:
            skater_dict = skater["skater"]
            skater_id = skater_dict["id"]
            skater_firstname = skater_dict["firstName"]
            skater_lastname = skater_dict["lastName"]
            skater_nationality = skater_dict["country"]
            skater_gender = skater_dict["gender"]
            skater_dob = skater_dict["dateOfBirth"]
            cursor.execute("""INSERT OR IGNORE INTO skaters(id, first_name, last_name, nationality, gender,
                                                           date_of_birth)
                               VALUES(?, ?, ?, ?, ?, ?)""",
                           (skater_id, skater_firstname, skater_lastname, skater_nationality,
                            skater_gender, skater_dob))
            cursor.execute("""INSERT OR IGNORE INTO event_skaters(skater_id, event_id) VALUES(?, ?)""",
                           (skater_id, event_id))

        cursor.execute("""INSERT OR IGNORE INTO events(id, name, track_id, date, distance, duration, laps, winner,
                                                      category)
                           VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                       (event_id, event_title, event_track_id, event_date, event_distance,
                        event_time_seconds, event_lapcount, event_winner_name, event_category))

        cursor.execute("""INSERT OR IGNORE INTO tracks(id, name, city, country, outdoor, altitude)
                           VALUES(?, ?, ?, ?, ?, ?)""",
                       (event_track_id, event_track_name, event_track_city, event_track_country,
                        event_track_outdoor, event_track_alt))
    conn.commit()   # Commit all changes at once.


def setup():
    json_database = read_json_file()
    configure_database(json_database)


if __name__ == "__main__":
    setup()
