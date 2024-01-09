import os
import sys
import json
import sqlite3

# Why are these unused?
from skater import Skater
from track import Track
from event import Event


# This function will open the JSON file and save it in a dictionary.
def read_json_file():
    json_file = open('events.json', encoding="utf8")
    events_data_dict = json.load(json_file)
    json_file.close()
    return events_data_dict


# This function will create or update all the database tables.
# It will also initialize all the required classes.
def configure_database(data):
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
        event_winner_name = " ".join([event_winner["firstName"], event_winner["lastName"]])

        event_last = event_result_list[-1]
        event_time = event_last["time"].strptime("%M:%S.%f")
        event_time_seconds = event_time.strftime("%S.%f")

        for skater in event_result_list:
            skater_dict = skater["skater"]
            skater_id = skater_dict["id"]
            skater_firstname = skater_dict["firstName"]
            skater_lastname = skater_dict["lastName"]
            skater_nationality = skater_dict["country"]
            skater_gender = skater_dict["gender"]
            skater_dob = skater_dict["dateOfBirth"]
            # Initialize Skater here
        # Initialize Event here
        # Initialize Track here

        # Add class init
        # Write everything into the db
    pass


def main():
    data = read_json_file()
    configure_database(data)
    # truncate_table()
    # print(data)


if __name__ == "__main__":
    main()
