import os
import subprocess


def tone1():
    subprocess.Popen(["cvlc", "end-alarm-tone.mp3", "--play-and-exit", "--quiet"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def tone2():
    subprocess.Popen(["cvlc", "start-alarm-tone.mp3", "--play-and-exit", "--quiet"],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
