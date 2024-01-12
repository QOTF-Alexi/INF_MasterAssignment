from skater import Skater
from event import Event
from track import Track
from datetime import datetime


testEvent = Event(1, "Essent ISU World Cup - 1500m Men Division A", 29, datetime(2003, 11, 8),
                      1500, 117.920, 4, "Erben Wennemars", "M")


# Test to check if the age of a skater is correct based on the date_of_birth
def test_age_of_skater():
    ageSkater = Skater(1, 'Henk', 'Kei', 'NLD', 'M', datetime(1994, 4, 4))
    assert ageSkater.get_age() == 29


# Test to check if the amount of events for a specific skater is returned correctly
def test_amount_of_events_of_skater():
    testSkater = Skater(314, 'Claudia', 'Pechstein', 'GER', 'F', datetime(1972, 2, 22))
    assert len(testSkater.get_events()) == 11


# Test to check if the amount of events for a specific track is returned correctly
def test_amount_of_events_of_track():
    testTrack = Track(29, 'Hamar Olympic Hall', 'Hamar', 'NOR', False, 123)
    assert len(testTrack.get_events()) == 12


# Test to check if the returned date matches the specified format for that event date
def test_event_date_conversion():
    raise NotImplementedError()

# Test to check if the duration is converted from 1H19 to the specified format
def test_event_duration_conversion():
    raise NotImplementedError()


# Test to check the amount of skaters on a specified event
def test_amount_of_skaters_on_event():
    assert len(testEvent.get_skaters()) == 56


# Test to validate if the given track of a specified event is correct
def test_track_on_event():
    assert testEvent.get_track() == "?"
