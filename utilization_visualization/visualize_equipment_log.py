import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os


def generate_figure_for_all_weeks(events, path):

    assert len(set([x.device for x in events])) == 1, 'Data spans more than one device'
    device = events[0].device

    # TODO add week if there isn't data that week
    weeks = list(set([x.beginning_of_week for x in events]))
    weeks.sort()
    weeks.reverse()

    fig = plt.figure(figsize=(11,8.5))
    ax = fig.add_subplot(111)
    ax.set_position([0.125, 0.1, 0.775, 0.82])

    plt.title('Device: %s' % (device))
    plt.xlabel('Day', fontsize=16)
    plt.ylabel('Week', fontsize=16)

    x = np.array([a*60*60*24 for a in range(0, 8)]) # the '*60*60*24' converts days to seconds
    my_xticks = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    plt.xticks(x, [])

    ax.tick_params(axis='x', labelbottom='off', which='major')
    ax.set_xticks([(a*60*60*24) - (60*60*24/2) for a in range(1, 8)], minor=True)
    ax.set_xticklabels(my_xticks, minor=True)
    ax.tick_params(axis='x', which='minor', labelsize=10, length=0)

    y = np.array(range(0, len(weeks)+1))
    my_yticks = []
    for week in weeks:
        my_yticks.append('%d-%d-%d' % (week.year, week.month, week.day))
    plt.yticks(y, my_yticks, fontsize=10)
    ax.set_ylim(-0.5, len(weeks) - 0.5)

    runtime_height = 0.4
    schedule_height = 0.2
    runtime_color = 'grey'
    factory_color = 'green'
    development_color = 'blue'
    automation_color = 'red'
    lab_services_color = 'yellow'
    none_color = 'black'

    for week in weeks:
        for event in events:
            if event.event_type == 'Runtime':
                rectangle = mpatches.Rectangle([(event.event_start - week).total_seconds(), weeks.index(week) - (0.5 * runtime_height)], (event.event_end - event.event_start).total_seconds(), runtime_height, color=runtime_color, alpha=0.1, linewidth=0)
            elif event.event_type != 'Runtime' and event.event_notes == 'Factory':
                rectangle = mpatches.Rectangle([(event.event_start - week).total_seconds(), weeks.index(week) - (0.5 * schedule_height)], (event.event_end - event.event_start).total_seconds(), schedule_height, color=factory_color, alpha=0.1, linewidth=0)
            elif event.event_type != 'Runtime' and event.event_notes == 'Development':
                rectangle = mpatches.Rectangle([(event.event_start - week).total_seconds(), weeks.index(week) - (0.5 * schedule_height)], (event.event_end - event.event_start).total_seconds(), schedule_height, color=development_color, alpha=0.1, linewidth=0)
            elif event.event_type != 'Runtime' and event.event_notes == 'Automation':
                rectangle = mpatches.Rectangle([(event.event_start - week).total_seconds(), weeks.index(week) - (0.5 * schedule_height)], (event.event_end - event.event_start).total_seconds(), schedule_height, color=automation_color, alpha=0.1, linewidth=0)
            elif event.event_type != 'Runtime' and event.event_notes == 'Lab Services':
                rectangle = mpatches.Rectangle([(event.event_start - week).total_seconds(), weeks.index(week) - (0.5 * schedule_height)], (event.event_end - event.event_start).total_seconds(), schedule_height, color=lab_services_color, alpha=0.1, linewidth=0)
            else:
                rectangle = mpatches.Rectangle([(event.event_start - week).total_seconds(), weeks.index(week) - (0.5 * schedule_height)], (event.event_end - event.event_start).total_seconds(), schedule_height, color=none_color, fill=False, alpha=0.5, linewidth=0.5)
            ax.add_patch(rectangle)

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('none')

    plt.savefig(os.path.join(path, r'%s.png' % (device)))
    plt.clf()


def generate_figure_for_one_week(events, path):

    assert len(set([x.beginning_of_week for x in events])) == 1, 'Data spans more than one week or no weeks'
    device = events[0].device

    assert len(set([x.device for x in events])) == 1, 'Data spans more than one device or no devices'
    week = events[0].beginning_of_week

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.xlabel('Time')
    plt.ylabel('Weekday')
    plt.title('Week: %d-%d-%d  Device: %s' % (week.year, week.month, week.day, device))

    x = np.array([a*60*60 for a in range(0, 25, 4)])  # the '*60*60' converts hours to seconds
    my_xticks = ['12 AM', '4 AM', '8 AM', '12 PM', '4 PM', '8 PM', '12 AM']
    plt.xticks(x, my_xticks)

    y = np.array(range(0, 7))
    my_yticks = ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']
    my_yticks.reverse()
    plt.yticks(y, my_yticks)

    ax.set_ylim(-0.5, 6.5)

    runtime_height = 0.6
    schedule_height = 0.3
    runtime_color = 'grey'
    factory_color = 'green'
    development_color = 'blue'
    automation_color = 'red'
    lab_services_color = 'yellow'
    none_color = 'black'

    for event in events:
        assert event.event_start.day == event.event_end.day, 'Event spans more than one day (%s to %s)' % (event.event_start, event.event_end)
        event_start_day = [5, 4, 3, 2, 1, 0, 6][event.event_start.weekday()]
        if event.event_type == 'Runtime':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * runtime_height)], (event.event_end - event.event_start).seconds, runtime_height, color=runtime_color, alpha=0.1, linewidth=0)
        elif event.event_type != 'Runtime' and event.event_notes == 'Factory':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * schedule_height)], (event.event_end - event.event_start).seconds, schedule_height, color=factory_color, alpha=0.1, linewidth=0)
        elif event.event_type != 'Runtime' and event.event_notes == 'Development':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * schedule_height)], (event.event_end - event.event_start).seconds, schedule_height, color=development_color, alpha=0.1, linewidth=0)
        elif event.event_type != 'Runtime' and event.event_notes == 'Automation':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * schedule_height)], (event.event_end - event.event_start).seconds, schedule_height, color=automation_color, alpha=0.1, linewidth=0)
        elif event.event_type != 'Runtime' and event.event_notes == 'Lab Services':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * schedule_height)], (event.event_end - event.event_start).seconds, schedule_height, color=lab_services_color, alpha=0.1, linewidth=0)
        else:
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * schedule_height)], (event.event_end - event.event_start).seconds, schedule_height, color=none_color, fill=False, alpha=0.5, linewidth=0.5)
        ax.add_patch(rectangle)

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('none')

    plt.savefig(os.path.join(path, r'%s %d_%d_%d.png' % (device, week.year, week.month, week.day)))
    plt.close()


if __name__ == "__main__":

    import sqlite3
    from event import Event, split_event

    con = sqlite3.connect(r'../test/test_event_log.db', detect_types=sqlite3.PARSE_DECLTYPES) # that 'detect_types' enables returning the datetime as a datetime
    con.text_factory = str
    cur = con.cursor()

    sqlite_query = 'SELECT device, start_time, end_time, event_type, event_notes FROM events'
    cur.execute(sqlite_query)

    events_by_day = []
    events_by_week = []
    devices = []
    weeks = []
    for data in cur.fetchall():
        event = Event(*data)
        events_by_day.extend(split_event(event, 'day'))
        events_by_week.extend(split_event(event, 'week'))

    devices = list(set([x.device for x in events_by_week]))
    weeks = list(set([x.beginning_of_week for x in events_by_day]))

    path = r'../test/images/'

    for device in list(set(devices)):
        for week in list(set(weeks)):
            event_subset = []
            for event in events_by_day:
                if event.device == device and event.beginning_of_week == week:
                    event_subset.append(event)
            if event_subset:
                generate_figure_for_one_week(event_subset, path)

    for device in list(set(devices)):
        event_subset = []
        for event in events_by_week:
            if event.device == device:
                event_subset.append(event)
        generate_figure_for_all_weeks(event_subset, path)

    con.commit()
    cur.close()