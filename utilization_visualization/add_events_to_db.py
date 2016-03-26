import sqlite3
from datetime import datetime, timedelta


def store_data(cur, data):

    for event in data:
        if len(event) == 4:
            event.append('')  # hack to add an empty event_notes for events without notes
        cur.execute('INSERT OR IGNORE INTO events(device, start_time, end_time, event_type, event_notes) VALUES(?, ?, ?, ?, ?)',
                    (event[0], format_datetime(event[1]), format_datetime(event[2]), event[3], event[4]))


def get_devices(cur):

    cur.execute('SELECT device FROM devices')
    devices = [x[0] for x in cur.fetchall()]

    return devices


def get_event_types(cur):

    cur.execute('SELECT event_type FROM event_types')
    event_types = [x[0] for x in cur.fetchall()]

    return event_types


def format_datetime(time):

    for structure in ('%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M', '%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %I:%M %p', '%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M', '%m/%d/%y %I:%M:%S %p', '%m/%d/%y %I:%M %p'):
        try:
            return datetime.strptime(time, structure)
        except ValueError:
            pass

    raise ValueError


def check_data(cur, data):

    devices = get_devices(cur)
    event_types = get_event_types(cur)
    errors = []

    for event in data:
        if not event[0] in devices:
            errors.append("The device '%s' is not in the valid list of devices %s" % (event[0], devices))
        if not event[3] in event_types:
            errors.append("The event type '%s' is not in the valid list of event types %s" % (event[3], event_types))
        try:
            format_datetime(event[1])
        except ValueError:
            errors.append("The start time '%s' does not use one of the required formats" % event[1])
        try:
            format_datetime(event[2])
        except ValueError:
            errors.append("The end time '%s' does not use one of the required formats" % event[2])
        try:
            # if format_datetime(event[2]) < format_datetime(event[1]):
            if not (format_datetime(event[2]) - format_datetime(event[1])).total_seconds() > 0:
                errors.append("The start time '%s' does not precede the end time '%s'" % (event[1], event[2]))
        except ValueError:
            pass

    if errors:
        print '\n'.join(errors)
        exit()


def get_events_data():

    data_path = ''
    while not data_path:
        # data_path = raw_input('Path to log file:\n  - ')
        # data_path = r'C:\Projects\python\Daily\20160320\test_data_v1.txt'
        # data_path = r'C:\Projects\python\Daily\20160320\test_data_v2.txt'
        # data_path = r'C:\Projects\python\Daily\20160320\test_data_v3.txt'
        # data_path = r'C:\Projects\python\Daily\20160320\test_data_v4.txt'
        data_path = r'C:\Projects\python\Daily\20160320\jc_data.txt'
        if not data_path.strip():
            print "You need to type something in..."
    try:
        data = []
        with open(data_path) as in_file:
            for line in in_file:
                event = line.rstrip('\n').split('\t')
                data.append(event)
    except IOError:
        print 'file %s does not exist' % data_path

    return data


def add_events():

    # TODO How should I set up this program to handle different timedate formats?
    # TODO Add capability to add devices or event types

    con = sqlite3.connect('event_log.db')
    con.text_factory = str
    cur = con.cursor()

    data = get_events_data()
    check_data(cur, data)
    store_data(cur, data)

    con.commit()
    cur.close()


def add_devices():

    data = get_events_data()
    devices = list(set([x[0] for x in data]))

    con = sqlite3.connect('event_log.db')
    con.text_factory = str
    cur = con.cursor()

    for device in devices:
        cur.execute('INSERT OR IGNORE INTO devices(device) VALUES(?)', (device.strip(),))

    con.commit()
    cur.close()


def add_event_types():

    data = get_events_data()
    event_types = list(set([x[3] for x in data]))

    con = sqlite3.connect('event_log.db')
    con.text_factory = str
    cur = con.cursor()

    for event_type in event_types:
        cur.execute('INSERT OR IGNORE INTO event_types(event_type) VALUES(?)', (event_type.strip(),))

    con.commit()
    cur.close()


if __name__ == "__main__":
    add_devices()
    add_event_types()
    add_events()
