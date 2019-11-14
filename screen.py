#!/usr/bin/env python3
"""
Définie la classe Screen
"""

import curses
import time

from random import choice

class Screen:
    """
    Class Screen
    Permet d'afficher des elements a l'écran
    init > update > del
    """

    def __init__(self):
        """
        Initialise l'affichage
        """
        self.stdscr = curses.initscr()

        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        # curses.noecho()
        # curses.cbreak()
        # keypad mode
        # self.stdscr.keypad(1)

        # curses.curs_set(0)  # Invisible

        # Start colors in curses
        """
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.start_color()
        """

        # curses.start_color()

        # Clear and refresh the screen for a blank canvas
        # self.stdscr.clear()
        # self.stdscr.idcok(False)

    def __del__(self):
        """
        Remet la console dans l'état initial
        """
        self.stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    def update(self, tab, pos_x, pos_y):
        """
        Actualise l'écran
        """
        height, width = self.stdscr.getmaxyx()
        height -= 1

        size_tab_x = len(tab)
        size_tab_y = len(tab[0])

        putc = lambda x, y, c: \
               self.stdscr.addstr(height - y -1, x, c.encode('UTF-8'))

        for scr_y in range(height):
            for scr_x in range(width):
                tab_x = scr_x + pos_x - width//2
                tab_y = scr_y + pos_y - height//2

                if 0 <= tab_x < size_tab_x and 0 <= tab_y < size_tab_y:
                    char = tab[tab_x][tab_y]
                    putc(scr_x, scr_y, char)
                else:
                    putc(scr_x, scr_y, ' ')

        # putc(0, 0, '@({},{})'.format(pos_x, pos_y))

        self.stdscr.refresh()
        self.stdscr.erase()


def main():
    """
    TU
    """
    try:
        data = [[choice([' ', '#']) for _ in range(500)] for _ in range(500)]
        screen = Screen()

        pos_x, pos_y = 0, 0
        while True:
            screen.update(data, pos_x, pos_y)
            time.sleep(0.1)

    finally:
        # Attrape erreur
        screen.__del__()


if __name__ == "__main__":
    main()
