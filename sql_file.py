import sqlite3
import config
from prettytable import PrettyTable as table
from termcolor import colored


# function to create database
def create_table():
    conn = sqlite3.connect('pomodoro.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS Pomodoro (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        taskname TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        totaltime TEXT,
        cycles INT,
        shortb TEXT,
        longb TEXT,
        sound INT)
        ''')
    conn.commit()
    c.close()


# function to input data to table
def input_data(task_name, time_stamp, cycle_time, cycles, shortb, longb, sound):
    conn = sqlite3.connect('pomodoro.db')
    c = conn.cursor()
    c.execute("INSERT INTO Pomodoro (taskname , timestamp, totaltime, cycles, shortb, longb, sound) VALUES (?,?,?,?,?,?,?)",
              (task_name, time_stamp, cycle_time, cycles, shortb, longb, sound))
    conn.commit()
    c.close()


# function to delete all tasks
def delete_all_task():
    conn = sqlite3.connect('pomodoro.db')
    c = conn.cursor()
    c.execute("DELETE from Pomodoro")
    conn.commit()
    c.close()


# function to select tasks of certain day
def list_day(time_stamp):
    conn = sqlite3.connect('pomodoro.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Pomodoro WHERE timestamp = ?;", (time_stamp,))
    data = c.fetchall()
    print(colored('Tasks for: ' + time_stamp, 'yellow'))
    t = table(['Task id', 'Taskname', 'Date', 'Total time', 'Cycles'])
    for row in data:
        id = str(row[0])
        name = str(row[1])
        date = str(row[2])
        time = str(row[3])
        cycle = str(row[4])
        t.add_row([id, name, date, time, cycle])
    print(t)

    c.close()


# function to select all tasks
def list_all():
    conn = sqlite3.connect('pomodoro.db')
    c = conn.cursor()
    c.execute("""SELECT * FROM Pomodoro""")
    data = c.fetchall()
    print(colored('All Tasks', 'yellow'))
    t = table(['Task id', 'Taskname', 'Date', 'Total time', 'Cycles'])
    for row in data:
        id = str(row[0])
        name = str(row[1])
        date = str(row[2])
        time = str(row[3])
        cycle = str(row[4])
        t.add_row([id, name, date, time, cycle])
    print(t)


# config short break in db
def short_break_db():
    list_all()
    x = input("Enter task id of process to edit short break: >")
    y = config.short_break_settings()
    conn = sqlite3.connect('pomodoro.db')
    c = conn.cursor()
    c.execute("UPDATE Pomodoro SET shortb = ? WHERE id = ?", (y, x))
    conn.commit()
    c.close()


# config long break in db
def long_break_db():
    list_all()
    x = input("Enter task id of process to edit long break: >")
    y = config.long_break_settings()
    conn = sqlite3.connect('pomodoro.db')
    c = conn.cursor()
    c.execute("UPDATE Pomodoro SET longb = ? WHERE id = ?", (y, x))
    conn.commit()
    c.close()


# config sound in db
def sound_db():
    list_all()
    x = input("Enter task id of process to edit sound: >")
    y = config.sound_settings()
    conn = sqlite3.connect('pomodoro.db')
    c = conn.cursor()
    c.execute("UPDATE Pomodoro SET sound = ? WHERE id = ?", (y, x))
    conn.commit()
    c.close()
