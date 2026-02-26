#!/usr/bin/python
"""
This example uses docopt with the built in cmd module to demonstrate an
interactive command application.

Usage:
    pomodoro start <task-title>
    pomodoro list <date>
    pomodoro list_all
    pomodoro config short_break | long_break | sound
    pomodoro clear
    pomodoro (-i | --interactive)
    pomodoro (-h | --help | --version)
    pomodoro exit

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.

Note:
    use interactive for best perfomance
"""
from new_task import new_task
from sql_file import list_day, list_all, short_break_db, long_break_db, sound_db, delete_all_task
from termcolor import cprint, colored
import sys
import os
import cmd
from docopt import docopt, DocoptExit
import datetime
import sqlite3
import time
from pyfiglet import Figlet, figlet_format
import countdown_timer
import pygame


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print(colored('Invalid Command!', 'red'))
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive(cmd.Cmd):
    f = Figlet(font='3d_diagonal')
    print(figlet_format("Tomato", font='3d_diagonal'))
    intro = 'Welcome to pomodoro timer!' \
            + ' (type help for a list of commands.)' + """
Usage:
    pomodoro start <task-title>
    pomodoro list <date>            eg. 2016:11:09
    pomodoro list_all
    pomodoro delete_all
    pomodoro config <command>       eg. short_break, long_break, sound
    pomodoro (-i | --interactive)
    pomodoro (-h | --help)
    pomodoro exit

Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""
    prompt = 'pomodoro '
    file = None

    def do_exit(self, arg):
        """Usage: exit"""
        print(colored('Good Bye!', 'red'))
        exit()

    @docopt_cmd
    def do_start(self, arg):
        """Usage: start <task-title>"""
        try:
            new_task(arg['<task-title>'])
        except KeyboardInterrupt:
            pygame.quit()
            print(colored('\nTask complete', 'yellow'))

    @docopt_cmd
    def do_list(self, arg):
        """Usage: list <date>"""
        list_day(arg['<date>'])

    @docopt_cmd
    def do_list_all(self, arg):
        """Usage: list_all"""
        list_all()

    @docopt_cmd
    def do_config(self, args):
        """Usage: config <command>"""
        if args['<command>'] == 'short_break':
            short_break_db()
        elif args['<command>'] == 'long_break':
            long_break_db()
        elif args['<command>'] == 'sound':
            sound_db()

    @docopt_cmd
    def do_delete_all(self):
        """Usage: delete_all"""
        delete_all_task()


opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    try:
        MyInteractive().cmdloop()
    except KeyboardInterrupt:
        print("\n")
