#!/usr/bin/env python3
"""
Définie la classe Screen
"""

import time
import sys
import termios
import os

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
        # Configuration console
        self.my_fd = sys.stdin.fileno()
        self.old = termios.tcgetattr(self.my_fd)
        new = termios.tcgetattr(self.my_fd)
        new[3] = new[3] & ~termios.ECHO          # lflags
        termios.tcsetattr(self.my_fd, termios.TCSADRAIN, new)

        # Lancement ecran second
        print("\033[?1049h\033[H", end="")
        sys.stdout.flush()

        # Bufferisarion de stdout
        self._BUFFER_SIZE = 500*500
        sys.stdout = open(sys.stdout.fileno(), "w", self._BUFFER_SIZE)

    def __del__(self):
        """
        Remet la console dans l'état initial
        """
        # Etat console
        termios.tcsetattr(self.my_fd, termios.TCSADRAIN, self.old)
        # Ecran
        print("\033[?1049l", end="")

    def update(self, tab, pos_x, pos_y):
        """
        Actualise l'écran
        """

        def sprint(car):
            """
            a
            """
            print(car, end='', flush=False)

        height, width = map(int, os.popen('stty size', 'r').read().split())
        assert height * width <= self._BUFFER_SIZE

        size_tab_x = len(tab)
        size_tab_y = len(tab[0])

        for scr_y in range(height, 0, -1):
            for scr_x in range(width):

                tab_x = scr_x + pos_x - width//2
                tab_y = scr_y + pos_y - height//2

                if 0 <= tab_x < size_tab_x and 0 <= tab_y < size_tab_y:
                    char = tab[tab_x][tab_y]
                    sprint(char)
                else:
                    sprint(' ')

        sys.stdout.flush()



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
