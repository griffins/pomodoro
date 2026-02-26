import pygame
import os
from termcolor import colored


# func to convert time to seconds
def time_in_sec(time):
    # time in hh:mm:ss
    total_time = time.split(':')

    try:  # check/get all 3 fields if present hh:mm:ss
        for i in [0, 1, 2]:
            total_time[i] = int(total_time[i])
    except:
        print(colored('The Input wasnt Valid!', 'red'))
        quit()

    # convert time to seconds
    # [2] is sec + [1] min*60 + [0] hrs*60*60
    time_in_seconds = (total_time[2]) + (total_time[1]
                                         * 60) + (total_time[0] * (60 * 60))
    return time_in_seconds


def countdown(time, title):
    pygame.init()
    timer_width = 280
    timer_height = 120
    timer_dsp = pygame.display.set_mode((timer_width, timer_height))
    pygame.display.set_caption("Pomodoro: " + title)
    font = pygame.font.SysFont('monospace', 15)

    total_time_in_seconds = time_in_sec(time)

    # formatting countdown output
    def countdown_time(time):
        hours = time // (60 ** 2)
        minutes = (time // 60) % 60
        seconds = time % 60
        return "%i H, %i Min and %i Sec" % (hours, minutes, seconds)

    # running the Timer
    while total_time_in_seconds > 0:
        if total_time_in_seconds <= 30:
            timer_dsp.fill((255, 4.25 * total_time_in_seconds,
                            4.25 * total_time_in_seconds))
        else:
            timer_dsp.fill((255, 255, 255))
        string = countdown_time(total_time_in_seconds)
        font_position = (
            (0.5 * timer_width) - (0.5 * font.size(string)[0]),
            (0.5 * timer_height) - (0.5 * font.size(string)[1])
        )
        rendered_font = font.render(string, 1, (0, 0, 0))
        timer_dsp.blit(rendered_font, font_position)
        pygame.display.flip()
        pygame.time.wait(1000)
        total_time_in_seconds -= 1

    pygame.quit()
