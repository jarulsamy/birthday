#!/usr/bin/env python3

import curses
import re
from collections import deque
from curses import wrapper
from time import sleep

# Happy Birthday Josh! ---------------------------------------------------------
CAKE = r'''
           ~                  ~
     *                   *                *       *
                  *               *
  ~       *                *         ~    *
              *       ~        *              *   ~
                  )         (         )              *
    *    ~     ) (_)   (   (_)   )   (_) (  *
           *  (_) # ) (_) ) # ( (_) ( # (_)       *
              _#.-#(_)-#-(_)#(_)-#-(_)#-.#_
  *         .' #  # #  #  # # #  #  # #  # `.   ~     *
           :   #    #  #  #   #  #  #    #   :
    ~      :.       #     #   #     #       .:      *
        *  | `-.__                     __.-' | *
           |      `````"""""""""""`````      |         *
     *     |         | ||\ |~)|~)\ /         |
           |         |~||~\|~ |~  |          |       ~
   ~   *   |                                 | *
           |      |~)||~)~|~| ||~\|\ \ /     |         *
   *    _.-|      |~)||~\ | |~|| /|~\ |      |-._
      .'   '.      ~            ~           .'   `.  *
      :      `-.__                     __.-'      :
       `.         `````"""""""""""`````         .'
         `-.._                             _..-'
              `````""""-----------""""`````
'''


def rot_left(s):
    return s[:1] + s[1:]


def rot_right(s):
    return s[1:] + s[:1]


def gen_cake_frames():
    left_buffer = []
    right_buffer = []
    non_background_chars = ("(", ")", "|", "#", "`", "-", ".", ":", "_", "'")
    split_pattern = re.compile(r"([" + "\\".join(non_background_chars) + "])")

    cake = []
    for line in CAKE.split("\n"):
        cake.append(f"     {line}     ")

    odd_row = 1
    for line in cake:
        if not any(c in line for c in non_background_chars):
            if odd_row % 3 == 0:
                left_buffer.append(rot_left(line))
                right_buffer.append(rot_right(line))
            else:
                left_buffer.append(rot_right(line))
                right_buffer.append(rot_left(line))
        else:
            segments = split_pattern.split(line)
            left_seg = segments[0]
            right_seg = segments[-1]
            middle_seg = "".join(segments[1:-1])

            if odd_row % 3 == 0:
                left_buffer.append(
                    rot_left(left_seg) + middle_seg + rot_left(right_seg)
                )
                right_buffer.append(
                    rot_right(left_seg) + middle_seg + rot_right(right_seg)
                )
            else:
                left_buffer.append(
                    rot_right(left_seg) + middle_seg + rot_right(right_seg)
                )
                right_buffer.append(
                    rot_left(left_seg) + middle_seg + rot_left(right_seg)
                )

        odd_row = odd_row + 1 if odd_row < 3 else 0

    cake = "\n".join(cake)
    left = "\n".join(left_buffer)
    right = "\n".join(right_buffer)

    return (left, right)


def main(stdscr):
    stdscr.clear()

    frames = gen_cake_frames()
    for _ in range(25):
        for frame in frames:
            try:
                stdscr.addstr(0, 0, frame)
            except curses.error:
                pass
            sleep(0.2)
            stdscr.refresh()


if __name__ == "__main__":
    wrapper(main)
