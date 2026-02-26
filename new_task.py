import time
import datetime
import config
import countdown_timer
import sql_file
import tone
from termcolor import cprint, colored


def cycle(tasks_length, tasks_time):
    if countdown_timer.time_in_sec(tasks_length) < countdown_timer.time_in_sec(tasks_time):
        no_of_cycles = 1
    else:
        no_of_cycles = countdown_timer.time_in_sec(
            tasks_length) // countdown_timer.time_in_sec(tasks_time)
    return no_of_cycles


def new_task(task_name):
    x = input("Press [Enter] to begin the countdown with default settings or 1 to configure!\n")
    if x == "1":
        print(colored('Configuring options for timer :', 'yellow'))
        tasks_length = config.task_length_settings()
        task_time = config.set_time()
        short_break = config.short_break_settings()
        long_break = config.long_break_settings()
        sound = config.sound_settings()
    elif x == '':
        print(colored('Using default settings :', 'yellow'))
        tasks_length = "00:01:00"
        task_time = "00:00:15"
        short_break = "00:00:05"
        long_break = "00:00:08"
        sound = True
    else:
        print(colored('Invalid input!', 'red'))
        print(colored('Choosing default settings :', 'yellow'))
        tasks_length = "00:01:00"
        task_time = "00:00:15"
        short_break = "00:00:05"
        long_break = "00:00:08"
        sound = True

    t = time.time()
    time_stamp = str(datetime.datetime.fromtimestamp(t).strftime('%Y:%m:%d'))

    # take input for task length
    print(colored('Total time       :   ', 'magenta') + str(tasks_length))
    print(colored('Task cycle time  :   ', 'magenta') + task_time)

    # no. of cycles
    cycles = cycle(tasks_length, task_time)
    print(colored('No. of cycles    :   ', 'magenta') + str(cycles + 1))

    print(colored('Short break      :   ', 'magenta') + short_break)
    print(colored('Long break       :   ', 'magenta') + long_break)
    print(colored('Sound            :   ', 'magenta') + str(sound))

    sql_file.input_data(task_name, time_stamp, tasks_length,
                        cycles + 1, short_break, long_break, sound)

    x = 0
    break_status = ''
    while cycles > x:
        count = 3
        while count > 0 and cycles > x:
            x += 1
            status = countdown_timer.countdown(task_time, task_name)
            if sound == True:
                tone.tone1()
            countdown_timer.countdown(short_break, "short break")
            tone.tone2()
            count -= 1
            x += 1
        countdown_timer.countdown(task_time, task_name)
        if sound == True:
            tone.tone1()
        countdown_timer.countdown(long_break, "long break")
        tone.tone2()

        x += 1
