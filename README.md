# POMODORO TIMER
### bc-11-pomodoro

##pomodoro timer??

Well if you google pomodoro you will come across tomatoes so whoever called it pomodoro missed out on a chance to call it Tomato timer
Podomoro timer allows you to schedule your tasks and break. It divides tasks to cycles, short breaks and long breaks.
Cycles by default are of 25 minutes, Short breaks 5 minutes (come after every cycle), Long breaks 15 minutes (come after 4 cycle). 
All times can be edited

## Installation

To run the app install and initialize virtual environment.

	clone repository
	`git clone https://github.com/sirjmkitavi/bc-11-pomodoro`

	cd into the directory
	`cd bc-11-pomodoro`

	Run uv add to install requirements
	`uv sync

Uses cvlc - command line vlc (comes with vlc player) to run play the alrm tones and pygame to display countdown timer

## Usage

Run Pomodoro timer `python pomodoro.py -i`
commands include:

     pomodoro start <task-title> to create new task for the timer 
     `pomodoro start presentations` 
     
     pomodoro config short_break to modify the short break time 
     `pomodoro config short_break`

     pomodoro config long_break to modify the break time
     `pomodoro config long_break`

     pomodoro config sound to modify sound settings
     `pomodoro config sound`

     pomodoro list <date> to list tasks of certain day
     `pomodoro list 2016:11:09`

     pomodoro list_all to list all tasks in database
     `pomodoro list_all`

     pomodoro delete_all to delete all tasks in database
     `pomodoro delete_all`


### To do List

	Working on `pomodoro stop`
     and `pomodoro run` to run currently configured apps from database

### Issues

Python Module `pygame` has support issues in latest MACs, still working on how to solve that. Suggestions are welcome.