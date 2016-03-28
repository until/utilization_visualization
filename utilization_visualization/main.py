import os
import sqlite3
from create_events_db import create_db
from add_to_events_db import add_event_types, add_devices, add_events
from event import Event, split_event
from visualize_equipment_log import generate_figure_for_one_week,generate_figure_for_all_weeks


def generate_figures():

    con = sqlite3.connect(r'../test/test_event_log.db', detect_types=sqlite3.PARSE_DECLTYPES) # that 'detect_types' enables returning the datetime as a datetime
    con.text_factory = str
    cur = con.cursor()

    sqlite_query = 'SELECT device, start_time, end_time, event_type, event_notes FROM events'
    cur.execute(sqlite_query)

    events_by_day = []
    events_by_week = []
    for data in cur.fetchall():
        event = Event(*data)
        events_by_day.extend(split_event(event, 'day'))
        events_by_week.extend(split_event(event, 'week'))

    devices = list(set([x.device for x in events_by_week]))
    weeks = list(set([x.beginning_of_week for x in events_by_day]))

    path = r'../test/images/'

    print 'Generating figures for one week...'
    for device in list(set(devices)):
        for week in list(set(weeks)):
            event_subset = []
            for event in events_by_day:
                if event.device == device and event.beginning_of_week == week:
                    event_subset.append(event)

            if event_subset:
                print device
                print week
                print len(event_subset)
                generate_figure_for_one_week(event_subset, path)

    print 'Generating figures for all weeks...'
    for device in list(set(devices)):
        event_subset = []
        for event in events_by_week:
            if event.device == device:
                event_subset.append(event)
        print device
        generate_figure_for_all_weeks(event_subset, path)

    con.commit()
    cur.close()


def store_data():

    print 'Storing data...'
    data_path = r'..\test\log_files\jc_data.txt'
    events = []
    with open(data_path) as in_file:
        for line in in_file:
            event = line.rstrip('\n').split('\t')
            events.append(event)

    if os.path.exists(r'..\test\test_event_log.db'):
        os.remove(r'..\test\test_event_log.db')

    con = sqlite3.connect(r'..\test\test_event_log.db', detect_types=sqlite3.PARSE_DECLTYPES)
    con.text_factory = str
    cur = con.cursor()

    create_db(cur)

    devices = list(set([x[0] for x in events]))
    add_devices(cur, devices)
    add_events(cur, events)

    con.commit()
    cur.close()


def main():

    store_data()
    generate_figures()


main()