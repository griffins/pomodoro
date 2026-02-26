from termcolor import colored


# cycle time settings
def set_time():
    td = input("Enter time for cycles as HH:MM:SS or [Enter] to use default: >")
    if td == '':
        td = "00:25:00"
        print("Using default: " + td)
        return td
    else:
        task_duration = td.split(':')
        try:
            for i in [0, 1, 2]:     # check if all 3 fields are present h:m:s
                task_duration[i] = int(task_duration[i])
            return td
        except:
            print(colored('The Input wasnt Valid!', 'red'))
            set_time()


# short break settings
def short_break_settings():
    short_break = input("Enter time for short break as HH:MM:SS or [Enter] to use default: >")
    if short_break == '':
        short_break = "00:05:00"
        print("Using default: " + short_break)
        return short_break
    else:
        sb = short_break.split(':')
        try:
            for i in [0, 1, 2]:  # check if all 3 fields are present h:m:s
                sb[i] = int(sb[i])
            return short_break
        except:
            print(colored('The Input wasnt Valid!', 'red'))
            short_break_settings()


# long break settings
def long_break_settings():
    long_break = input("Enter time for long break as HH:MM:SS or [Enter] to use default: >")
    if long_break == '':
        long_break = "00:15:00"
        print("Using default: " + long_break)
        return long_break
    else:
        lb = long_break.split(':')
        try:
            for i in [0, 1, 2]:  # check if all 3 fields are present h:m:s
                lb[i] = int(lb[i])
            return long_break
        except:
            print(colored('The Input wasnt Valid!', 'red'))
            long_break_settings()


# sound setting
def sound_settings():
    n = input("Enter 1 for Sound on or 0 for off or [Enter] to use default: >")
    if n == '':
        sound = True
        print("Using default: " + str(sound))
        return sound
    else:
        if n == '0':
            sound = False
            return sound
        elif n == '1':
            sound = True
            return sound
        else:
            print(colored('The Input wasnt Valid!', 'red'))
            sound_settings()
        return sound


# total task length
def task_length_settings():
    task_length = input("Enter total time for task as HH:MM:SS or [Enter] to use default: >")
    if task_length == '':
        task_length = "01:00:00"
        print("Using default: " + task_length)
        return task_length
    else:
        tl = task_length.split(':')
        try:
            for i in [0, 1, 2]:  # check if all 3 fields are present h:m:s
                tl[i] = int(tl[i])
            return task_length
        except:
            print(colored('The Input wasnt Valid!', 'red'))
            task_length_settings()
