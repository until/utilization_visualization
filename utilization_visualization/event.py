from datetime import datetime, timedelta


def split_event(event_to_split, split_type):
    """
    Note that I'm not sure how this will handle events at the transition between daylight savings and standard time.
    :param event_to_split: an Event object
    :param split_type: either 'day' or 'week', with 'day' as the default
    :return: a list of Event objects
    """

    split_types = ['day', 'week']
    if split_type not in split_types:
            raise ValueError("could not find '%s' in ['%s']" % (split_type, "', '".join(split_types)))

    split_events = []


    '''
    I need to figure out if I'm going to allow 0 second events. This comes up when I split events.
    I think I should allow them. This requires a little code refactoring.
    '''


    if split_type == 'day':
        event_to_evaluate = event_to_split # why do I preserve event_to_split
        # while event_to_evaluate.event_end > event_to_evaluate.end_of_day + timedelta(seconds=1):
        while event_to_evaluate.event_end > event_to_evaluate.end_of_day:
            split_events.append(Event(event_to_evaluate.device, event_to_evaluate.event_start, event_to_evaluate.end_of_day, event_to_evaluate.event_type, event_to_evaluate.event_notes))
            event_to_evaluate = Event(event_to_evaluate.device, event_to_evaluate.end_of_day + timedelta(seconds=1), event_to_evaluate.event_end, event_to_evaluate.event_type, event_to_evaluate.event_notes)
        # if event_to_evaluate.duration != timedelta(0):
        # if not event_to_evaluate.event_end == event_to_evaluate.beginning_of_day:
        #     split_events.append(event_to_evaluate)
        split_events.append(event_to_evaluate)
    elif split_type == 'week':
        event_to_evaluate = event_to_split # why do I preserve event_to_split
        while event_to_evaluate.event_end > event_to_evaluate.end_of_week + timedelta(seconds=1): # TODO test this
            split_events.append(Event(event_to_evaluate.device, event_to_evaluate.event_start, event_to_evaluate.end_of_week, event_to_evaluate.event_type, event_to_evaluate.event_notes))
            event_to_evaluate = Event(event_to_evaluate.device, event_to_evaluate.end_of_week + timedelta(seconds=1), event_to_evaluate.event_end, event_to_evaluate.event_type, event_to_evaluate.event_notes)
        if event_to_evaluate.duration != timedelta(0):
            split_events.append(event_to_evaluate)

    return split_events


class Event(object):
    """
    This is an event in an equipment event log. Events have the following properties:

    Attributes:
        start_time: The start time for the event. The format is 'm/d/yyyy h:mm:ss'.
        end_time: The end time for the event. The format is 'm/d/yyyy h:mm:ss'.
        event_type: The event type, either 'Runtime' or 'Scheduled'
            # Add more types here including 'Maintenance', etc.
        event_notes: A detail of the event type.
    """

    def __init__(self, device, event_start, event_end, event_type, event_notes):
        self.device = device
        self.event_type = event_type
        self.event_notes = event_notes
        try:
            self.event_start = event_start
            self.event_end = event_end
            assert (self.event_end - self.event_start).total_seconds() > 0, 'event_start (%s) is not before event_end (%s)' % (self.event_start, self.event_end)
        except:
            raise

    @property
    def duration(self):
        return self.event_end - self.event_start

    @property
    def beginning_of_day(self):
        return self.event_start.replace(hour=0, minute=0, second=0)

    @property
    def beginning_of_week(self):
        weekday_difference = [1, 2, 3, 4, 5, 6, 0]
        return self.event_start.replace(hour=0, minute=0, second=0) - timedelta(weekday_difference[self.event_start.weekday()])

    @property
    def end_of_day(self):
        return self.event_start.replace(hour=23, minute=59, second=59)

    @property
    def end_of_week(self):
        weekday_difference = [5, 4, 3, 2, 1, 0, 6]
        return self.event_start.replace(hour=23, minute=59, second=59) + timedelta(weekday_difference[self.event_start.weekday()])

    def is_within_single_day(self):
        if self.end_of_day > self.event_end:
            return True
        else:
            return False

    def is_within_single_week(self):
        if self.end_of_week > self.event_end:
            return True
        else:
            return False

    def __repr__(self):
        return 'Event(device=%r, event_start=%r, event_end=%r, event_type=%r, event_notes=%r' % (self.device, self.event_start, self.event_end, self.event_type, self.event_notes)


if __name__ == "__main__":

    # TODO test for wrong data types, wrong order
    # TODO in general, add tests

    device = 'Tecan 1'
    event_type = 'Runtime'
    event_notes = 'test notes'

    # nothing to split
    start_time = datetime(2015, 7, 24, 10, 44, 26)
    end_time = datetime(2015, 7, 24, 11, 14, 35)

    # split by day
    start_time = datetime(2015, 7, 23, 10, 44, 26)
    end_time = datetime(2015, 7, 24, 11, 14, 35)

    # starts at midnight
    start_time = datetime(2015, 7, 24, 0, 0, 0)
    end_time = datetime(2015, 7, 24, 11, 14, 35)

    # starts just before midnight
    start_time = datetime(2015, 7, 23, 23, 59, 59)
    end_time = datetime(2015, 7, 24, 11, 14, 35)

    # ends at midnight
    start_time = datetime(2015, 7, 24, 10, 44, 26)
    end_time = datetime(2015, 7, 25, 0, 0, 0)

    # spans several days
    start_time = datetime(2015, 7, 21, 10, 44, 26)
    end_time = datetime(2015, 7, 24, 11, 14, 35)

    # spans week
    start_time = datetime(2015, 7, 18, 10, 44, 26)
    end_time = datetime(2015, 7, 24, 11, 14, 35)

    # spans several weeks
    start_time = datetime(2015, 7, 18, 10, 44, 26)
    end_time = datetime(2015, 7, 28, 11, 14, 35)

    # to corrent week start problem
    start_time = datetime(2015, 7, 18, 10, 44, 26)
    end_time = datetime(2015, 7, 20, 11, 14, 35)

    # to test problem of ending at day break and week break
    start_time = datetime(2015, 7, 18, 00, 00, 00)
    end_time = datetime(2015, 7, 19, 00, 0, 00)

    # to test problem of ending at day break and week break
    # start_time = datetime(2015, 7, 18, 00, 00, 00)
    # end_time = datetime(2015, 7, 19, 00, 0, 01)

    event = Event(device, start_time, end_time, event_type, event_notes)
    print event
    # print event.is_within_single_day()
    # print event.is_within_single_week()
    # print event.beginning_of_day
    # print event.beginning_of_week

    print
    print 'Split events by day...'
    if not event.is_within_single_day():
        events = split_event(event, 'day')
        for e in events:
            print e

    # print
    # print 'Split events by week...'
    # if not event.is_within_single_week():
    #     events = split_event(event, 'week')
    #     for e in events:
    #         print e