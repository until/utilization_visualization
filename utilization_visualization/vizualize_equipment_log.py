import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta


def generate_figure_for_all_weeks(events_by_week, device):

    weeks = events_by_week.keys()
    weeks.sort()
    weeks.reverse()

    fig = plt.figure(figsize=(11,8.5))
    # fig = plt.figure(figsize=(22,17))
    # fig = plt.figure()
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

    for week in weeks:
        for event in events_by_week[week]:
            runtime_height = 0.6
            schedule_height = 0.3
            runtime_color = 'red'
            schedule_color = 'grey'
            if event['class'] == 'Runtime':
                rectangle = mpatches.Rectangle([(event['event_start'] - week).total_seconds(), weeks.index(week) - (0.5 * runtime_height)], (event['event_end'] - event['event_start']).total_seconds(), runtime_height, color=runtime_color, alpha=0.1, linewidth=0)
            elif event['class'] == 'Scheduled':
                rectangle = mpatches.Rectangle([(event['event_start'] - week).total_seconds(), weeks.index(week) - (0.5 * schedule_height)], (event['event_end'] - event['event_start']).total_seconds(), schedule_height, color=schedule_color, alpha=0.1, linewidth=0)
            else:
                raise Exception
            ax.add_patch(rectangle)

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('none')

    plt.savefig('%s.png' % (device))  # what is that tool to give files safe names? might want to use that here
    plt.clf()

    return


def generate_figure_for_one_week(events, week, device):
    # import os
    # if os.path.exists(('images/%s %d_%d_%d.png' % (device, week.year, week.month, week.day))):
    #     return

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

    # fix this so it addresses running across days

    for event in events:
        runtime_height = 0.6
        schedule_height = 0.3
        # runtime_color = 'red'
        # schedule_color = 'grey'
        runtime_color = 'grey'
        factory_color = 'green'
        development_color = 'blue'
        automation_color = 'red'
        lab_services_color = 'yellow'
        event_start_day = [5, 4, 3, 2, 1, 0, 6][event.event_start.weekday()]
        # if event.event_type == 'Completed':
        #     rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * runtime_height)], (event.event_end - event.event_start).seconds, runtime_height, color=runtime_color, alpha=0.1, linewidth=0)
        if event.event_type == 'Runtime':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * runtime_height)], (event.event_end - event.event_start).seconds, runtime_height, color=runtime_color, alpha=0.1, linewidth=0)
        elif event.event_notes == 'Factory':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * schedule_height)], (event.event_end - event.event_start).seconds, schedule_height, color=factory_color, alpha=0.1, linewidth=0)
        elif event.event_notes == 'Development':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * schedule_height)], (event.event_end - event.event_start).seconds, schedule_height, color=development_color, alpha=0.1, linewidth=0)
        elif event.event_notes == 'Automation':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * schedule_height)], (event.event_end - event.event_start).seconds, schedule_height, color=automation_color, alpha=0.1, linewidth=0)
        elif event.event_notes == 'Lab Services':
            rectangle = mpatches.Rectangle([(event.event_start - event.beginning_of_day).seconds, event_start_day - (0.5 * schedule_height)], (event.event_end - event.event_start).seconds, schedule_height, color=lab_services_color, alpha=0.1, linewidth=0)
        else:
            raise Exception
        ax.add_patch(rectangle)

    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('none')

    plt.savefig('images/%s %d_%d_%d.png' % (device, week.year, week.month, week.day))
    # plt.clf()
    plt.close()

    return

# def get_data():
#
#     """
#     Might want to change this away from a DictReader that just build another dict
#     Why not just read readlines() and then move into dict
#     Plus, shouldn't the content I'm adding be an even object? Seems reasonable
#     Then I can add the functions to capture time_from_week_start and time_from_day_start and duration calculations in there
#     Then I can handle exceptions that wrap around a day or a week
#     Inlclude those flags in object
#     """
#
#     events_by_week = {}
#     # with open('test_data.txt') as in_file:
#     # with open('test_data2.txt') as in_file:
#     # with open('test_data3.txt') as in_file:
#     # with open('test_data4.txt') as in_file:
#     with open('test_data5.txt') as in_file:
#     # with open('test_data6.txt') as in_file:
#         reader = csv.DictReader(in_file, delimiter='\t')
#         for row in reader:
#             event_start = datetime.strptime(row['Start Time'], '%m/%d/%Y %H:%M:%S')
#             event_end = datetime.strptime(row['End Time'], '%m/%d/%Y %H:%M:%S')
#             beginning_of_day = event_start.replace(hour=0, minute=0, second=0)
#             beginning_of_week = event_start.replace(hour=0, minute=0, second=0) - timedelta(event_start.weekday()+1)
#
#             if beginning_of_week in events_by_week.keys():
#                 events_by_week[beginning_of_week].append({'event_start': event_start, 'event_end': event_end, 'beginning_of_day': beginning_of_day, 'protocol': row['Protocol'], 'class': row['Category']})
#             else:
#                 events_by_week[beginning_of_week] = [{'event_start': event_start, 'event_end': event_end, 'beginning_of_day': beginning_of_day, 'protocol': row['Protocol'], 'class': row['Category']}]
#             # if beginning_of_week in events_by_week.keys():
#             #     events_by_week[beginning_of_week].append({'event_start': event_start, 'event_end': event_end, 'beginning_of_day': beginning_of_day, 'beginning_of_week': beginning_of_week, 'protocol': row['Protocol'], 'class': row['Class']})
#             # else:
#             #     events_by_week[beginning_of_week] = [{'event_start': event_start, 'event_end': event_end, 'beginning_of_day': beginning_of_day, 'beginning_of_week': beginning_of_week, 'protocol': row['Protocol'], 'class': row['Class']}]
#
#     return events_by_week


def build_figures(events, devices, weeks):

    # this is not handling things that bridge the weeks (Sat/Sun)

    for device in list(set(devices)):
        for week in list(set(weeks)):
            event_subset = []
            for event in events:
                if event.device == device and event.beginning_of_week == week:
                    event_subset.append(event)
                    generate_figure_for_one_week(event_subset, week, device)

            print 'Week: %d-%d-%d  Device: %s' % (week.year, week.month, week.day, device)


if __name__ == "__main__":
    # # device = 'Tecan 1'
    # # # device = 'Tecan 2'
    # # events_by_week = get_data()
    # # # check that data is from just one week
    # # # probably turn this into a web form
    # # for week in events_by_week:
    # #     generate_figure_for_week(events_by_week[week], week, device)
    # # generate_figure_for_all_weeks(events_by_week, device)
    #
    #
    #
    # import sqlite3
    # from event import Event
    #
    # con = sqlite3.connect('event_log.db', detect_types=sqlite3.PARSE_DECLTYPES) # that 'detect_types' enables returning the datetime as a datetime
    # con.text_factory = str
    # cur = con.cursor()
    #
    # sqlite_query = 'SELECT device, start_time, end_time, event_type, event_notes FROM events'
    # cur.execute(sqlite_query)
    #
    # # data = cur.fetchone()
    # # week = datetime(2015, 7, 19, 0,0,0)
    # # device = 'Tecan 1'
    # # event = Event(*data)
    # # print event
    # # generate_figure_for_one_week([event], week, device)
    #
    # week = datetime(2015, 7, 19, 0, 0, 0)
    # device = 'Tecan 1'
    # events = []
    # for data in cur.fetchall():
    #     event = Event(*data)
    #     if event.beginning_of_week == week and event.device == device:
    #         events.append(event)
    #
    # generate_figure_for_one_week(events, week, device)
    #
    # con.commit()
    # cur.close()


    import sqlite3
    from event import Event

    con = sqlite3.connect('event_log.db', detect_types=sqlite3.PARSE_DECLTYPES) # that 'detect_types' enables returning the datetime as a datetime
    con.text_factory = str
    cur = con.cursor()

    sqlite_query = 'SELECT device, start_time, end_time, event_type, event_notes FROM events'
    cur.execute(sqlite_query)

    events = []
    devices = []
    weeks = []
    for data in cur.fetchall():
        event = Event(*data)
        # function that returns event split across weeks and then days, then extend list with that
        events.append(event)
        devices.append(event.device)
        weeks.append(event.beginning_of_week)

    build_figures(events, devices, weeks)

    con.commit()
    cur.close()