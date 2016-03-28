import sqlite3
from datetime import datetime


def _store_data(cur, data):

    for event in data:
        if len(event) == 4:
            event.append('')  # hack to add an empty event_notes for events without notes
        cur.execute('INSERT OR IGNORE INTO events(device, start_time, end_time, event_type, event_notes) VALUES(?, ?, ?, ?, ?)',
                    (event[0], _format_datetime(event[1]), _format_datetime(event[2]), event[3], event[4]))


def _get_devices(cur):

    cur.execute('SELECT device FROM devices')
    devices = [x[0] for x in cur.fetchall()]

    return devices


def _get_event_types(cur):

    cur.execute('SELECT event_type FROM event_types')
    event_types = [x[0] for x in cur.fetchall()]

    return event_types


def _format_datetime(time):

    for structure in ('%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M', '%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %I:%M %p', '%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M', '%m/%d/%y %I:%M:%S %p', '%m/%d/%y %I:%M %p'):
        try:
            return datetime.strptime(time, structure)
        except ValueError:
            pass

    raise ValueError


def _check_data(cur, data):

    devices = _get_devices(cur)
    event_types = _get_event_types(cur)
    errors = []

    for event in data:
        if not event[0] in devices:
            errors.append("The device '%s' is not in the valid list of devices %s" % (event[0], devices))
        if not event[3] in event_types:
            errors.append("The event type '%s' is not in the valid list of event types %s" % (event[3], event_types))
        try:
            _format_datetime(event[1])
        except ValueError:
            errors.append("The start time '%s' does not use one of the required formats" % event[1])
        try:
            _format_datetime(event[2])
        except ValueError:
            errors.append("The end time '%s' does not use one of the required formats" % event[2])
        try:
            if not (_format_datetime(event[2]) - _format_datetime(event[1])).total_seconds() >= 0:
                errors.append("The end time '%s' precedes the start time '%s'" % (event[2], event[1]))
        except ValueError:
            pass

    if errors:
        print '\n'.join(errors)
        exit()


def add_events(cur, events):

    _check_data(cur, events)
    _store_data(cur, events)


def add_devices(cur, devices):

    for device in devices:
        cur.execute('INSERT OR IGNORE INTO devices(device) VALUES(?)', (device.strip(),))


def add_event_types(cur, event_types):

    for event_type in event_types:
        cur.execute('INSERT OR IGNORE INTO event_types(event_type) VALUES(?)', (event_type.strip(),))


if __name__ == "__main__":

    con = sqlite3.connect(r'..\test\test_event_log.db')
    con.text_factory = str
    cur = con.cursor()

    devices = ['test_device']
    event_types = ['test_event_type']
    event_1 = 'test_device\t1/1/2016 8:00:01\t1/1/2016 9:01:02\ttest_event_type\ttest_event_notes'.split('\t')
    event_2 = 'test_device\t1/1/2016 8:00:01\t1/21/2016 9:01:02\ttest_event_type\ttest_event_notes'.split('\t')
    event_3 = 'test_device\t1/6/2016 8:00:01\t1/18/2016 9:01:02\tRuntime\ttest_event_notes'.split('\t')
    event_4 = 'test_device\t1/6/2016 8:00:01\t2/18/2016 9:01:02\tRuntime\ttest_event_notes'.split('\t')
    event_5 = 'test_device\t1/6/2016 8:00:01\t5/18/2016 9:01:02\ttest_event_type\ttest_event_notes'.split('\t')
    event_6 = 'test_device\t1/6/2016 8:00:00\t1/6/2016 8:00:00\ttest_event_type\ttest_event_notes'.split('\t')
    event_7 = 'test_device\t1/6/2016 0:00:00\t1/7/2016 0:00:00\ttest_event_type\ttest_event_notes'.split('\t')
    event_8 = 'test_device\t1/6/2016 0:00:00\t1/5/2016 0:00:00\ttest_event_type\ttest_event_notes'.split('\t')
    events = [event_1, event_2, event_3, event_4, event_5, event_6, event_7, event_8]

    add_devices(cur, devices)
    add_event_types(cur, event_types)
    add_events(cur, events)

    con.commit()
    cur.close()
