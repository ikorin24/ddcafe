#! /usr/bin/env python
# -*- using:utf-8 -*-

"""
ddcafe.py: joke program; playing Gochi-usa opening movie 'Daydream cafe'.
"""
from argparse import ArgumentParser
import time
import os
import json
import threading
import shutil
import curses
from os.path import dirname, abspath

__author__ = "ikorin24"
__copyright__ = "Copyright (c) 2018, ikorin24"
__version__ = '0.0.1'
__date__ = '2018/06/10'

def arg_parse():
    parser = ArgumentParser(usage='Usage: {0} [option]'.format(__file__),
                            description="You can play 'Daydraem cafe' on the terminal.",
                            add_help=True)
    parser.add_argument('-v', '--version', action='version', version='0.0.1')
    parser.add_argument('-s', '--speed',
                        type=float,
                        default=1.0,
                        required=False,
                        help='ratio of playing speed (range: 0.1 ~ 10.0, default: 1.0)')
    parser.add_argument('-d', '--data',
                        type=str,
                        default=os.path.join(dirname(abspath(__file__)), 'data/ddcafe.json'),
                        required=False,
                        help='movie source json data. (default movie is "daydream cafe")')
    parser.add_argument('-r', '--reverse', action='store_true', default=False, required=False,
                        help='reverse pixel color; black to white, white to black')
    return parser.parse_args()


def load_movie(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data['frames'], data['fps'], data['pixel_level'], data['width'], data['height']


def play(console):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    pixel_reverse = _args.reverse
    speed = max(min(_args.speed, 10.0), 0.1)
    frames, fps, pixel_level, width, height = load_movie(_args.data)
    term_size = shutil.get_terminal_size()
    col = max(term_size.columns, width * 2 + 1)
    row = max(term_size.lines, height + 1)
    try:
        if os.name != 'nt':
            # Windows does not have 'curses.resizeterm()'. Why ?
            curses.resizeterm(row, col)
            os.system('resize -s {} {}'.format(row, col))
        start = time.time()
        console.clear()
        while True:
            current = int((time.time() - start) * speed * fps)
            if current >= len(frames):
                break
            for y in range(len(frames[current])):
                # decode pixel data into text for a row line.
                if pixel_reverse:
                    line = ''.join(map(lambda n: pixel_level[len(pixel_level) - 1 - int(n.strip())],
                                       frames[current][y].split(',')))
                    console.addstr(y, 0, line, curses.color_pair(1))
                else:
                    line = ''.join(map(lambda n: pixel_level[int(n.strip())],
                                       frames[current][y].split(',')))
                    console.addstr(y, 0, line, curses.color_pair(0))
            # draw line below the picture
            pos = int((width * 2 - 2) * current / len(frames))
            console.addstr(height, 0, '|{}|'.format('-' * pos + ' ' * (width * 2 - 2 - pos)))
            console.refresh()
            time.sleep(0.04)
        console.clear()
    finally:
        if os.name != 'nt':
            # restore original window size
            os.system('resize -s {} {}'.format(term_size.lines, term_size.columns))


def main():
    global _args
    _args = arg_parse()
    curses.wrapper(play)


_args = None
if __name__ == '__main__':
    main()
