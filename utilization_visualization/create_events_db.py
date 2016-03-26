import sqlite3
import os


def add_event_types(cur):
    cur.execute("INSERT INTO devices (device) VALUES ('Tecan 1')")
    cur.execute("INSERT INTO devices (device) VALUES ('Tecan 2')")
    cur.execute("INSERT INTO devices (device) VALUES ('Tecan 3')")
    cur.execute("INSERT INTO devices (device) VALUES ('Bravo 1')")

def add_devices(cur):
    cur.execute("INSERT INTO event_types (event_type) VALUES ('Scheduled')")
    cur.execute("INSERT INTO event_types (event_type) VALUES ('Maintenance')")
    cur.execute("INSERT INTO event_types (event_type) VALUES ('Runtime')")

def create_db(cur):
    cur.execute('''
                CREATE TABLE if not EXISTS events(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device TEXT,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                event_type TEXT,
                event_notes TEXT,
                UNIQUE(device, start_time, end_time, event_type, event_notes)
                )
                ''')
    cur.execute('CREATE TABLE if not EXISTS devices(id INTEGER PRIMARY KEY AUTOINCREMENT, device TEXT, UNIQUE(device))')
    cur.execute('CREATE TABLE if not EXISTS event_types(id INTEGER PRIMARY KEY AUTOINCREMENT, event_type TEXT, UNIQUE(event_type))')

def main():

    os.remove('event_log.db')

    con = sqlite3.connect('event_log.db')
    cur = con.cursor()

    create_db(cur)
    # add_devices(cur)
    # add_event_types(cur)

    con.commit()
    cur.close()


main()