"""
Course: CSE 251 
Lesson: L09 Prove Part 2
File:   prove_part_2.py
Author: <Add name here>

Purpose: Part 2 of prove 9, finding the path to the end of a maze using recursion.

Instructions:
- Do not create classes for this assignment, just functions.
- Do not use any other Python modules other than the ones included.
- You MUST use recursive threading to find the end of the maze.
- Each thread MUST have a different color than the previous thread:
    - Use get_color() to get the color for each thread; you will eventually have duplicated colors.
    - Keep using the same color for each branch that a thread is exploring.
    - When you hit an intersection spin off new threads for each option and give them their own colors.

This code is not interested in tracking the path to the end position. Once you have completed this
program however, describe how you could alter the program to display the found path to the exit
position:

What would be your strategy?

I am going to copy my code down from part 1 first off, get rid the pathing stuff. Then I
am going to start threads for each move possible.

Why would it work?

If there are 3 moves, create 2 other 
threads with different colors and have those do there thing. When a thread reaches a dead
end instead of backtracking, kill the thread. This will essentially do the same thing as part 1
except with concurrent paths.

"""

import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 files
from cse251 import *

SCREEN_SIZE = 700
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)
SLOW_SPEED = 100
FAST_SPEED = 0

# Globals
current_color_index = 0
thread_count = 0
stop = False
lock = threading.Lock()
speed = SLOW_SPEED

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


# TODO: Add any function(s) you need, if any, here.


def solve_find_end(maze):
    """ Finds the end position using threads. Nothing is returned. """
    global stop
    stop = False
    row, col = maze.get_start_pos()

    def solve(row, col, color):
        global stop

        if stop:
            return

        maze.move(row, col, color)

        if maze.at_end(row, col):
            with lock:
                stop = True
            return

        possible_moves = maze.get_possible_moves(row, col)

        if len(possible_moves) > 1:
            threads = []
            first_move = possible_moves[0]
            remaining_moves = possible_moves[1:]

            # Create new threads for other moves
            for move in remaining_moves:
                if maze.can_move_here(move[0], move[1]) and not stop:
                    thread_color = get_color()
                    thread = threading.Thread(target=solve, args=(move[0], move[1], thread_color))
                    threads.append(thread)
                    thread.start()

            next_row, next_col = first_move
            if maze.can_move_here(next_row, next_col) and not stop:
                solve(next_row, next_col, color)

            for thread in threads:
                thread.join()

        elif len(possible_moves) == 1:
            if maze.can_move_here(possible_moves[0][0], possible_moves[0][1]) and not stop:
                solve(possible_moves[0][0], possible_moves[0][1], color)

    solve(row, col, get_color())


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count
    global speed

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('1'):
                speed = SLOW_SPEED
            elif key == ord('2'):
                speed = FAST_SPEED
            elif key == ord('q'):
                exit()
            elif key != ord('p'):
                done = True
        else:
            done = True


def find_ends(log):
    """ Do not change this function """

    files = (
        ('very-small.bmp', True),
        ('very-small-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False),
        ('large-squares.bmp', False),
        ('large-open.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        filename = f'./mazes/{filename}'
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)


if __name__ == "__main__":
    main()