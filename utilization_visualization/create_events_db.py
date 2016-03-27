import sqlite3
import os


def _add_event_types(cur):

    event_types = ['Runtime', 'Offline', 'Intermittent', 'Busy']

    for event_type in event_types:
        cur.execute('INSERT OR IGNORE INTO event_types(event_type) VALUES(?)', (event_type.strip(),))


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

    _add_event_types(cur)


if __name__ == "__main__":

    if os.path.exists(r'..\test\test_event_log.db'):
        os.remove(r'..\test\test_event_log.db')

    con = sqlite3.connect(r'..\test\test_event_log.db')
    cur = con.cursor()

    create_db(cur)

    con.commit()
    cur.close()