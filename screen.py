#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Screen
"""

# http://nicofo.tuxfamily.org/index.php?post/2007/01/10/19-mouvement-du-curseur-dans-le-terminal
# https://rosettacode.org/wiki/Terminal_control/Preserve_screen#Python

import sys
import termios
import os

from vect import Vect

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
        # Sauvegarde du terminal
        self.my_fd = sys.stdin.fileno()
        self.old = termios.tcgetattr(self.my_fd)

        # Désactivation echo stdin
        new = termios.tcgetattr(self.my_fd)
        new[3] = new[3] & ~termios.ECHO  # lflags
        termios.tcsetattr(self.my_fd, termios.TCSADRAIN, new)
        # Lancement ecran second + Désactivation curseur
        print("\033[?1049h\033[H" + "\033[?25l", end="")
        sys.stdout.flush()
        # Bufferisarion de stdout
        self._BUFFER_SIZE = 500*500
        sys.stdout = open(sys.stdout.fileno(), "w", self._BUFFER_SIZE)

    def __del__(self):
        """
        Remet la console dans l'état initial
        """
        # Remise de l'état initial console
        termios.tcsetattr(self.my_fd, termios.TCSADRAIN, self.old)
        # Fermeture ecran second + Activation curseur
        print("\033[?1049l" + "\033[?25h", end="")


    def update(self, render_tab, pos):
        """
        Actualise l'écran
        """

        def sprint(car):
            """ print sans \r\n et flush """
            print(car, end='', flush=False)

        def screen_size():
            """ Taille de l'écran """
            # bof ...
            H, W = map(int, os.popen('stty size', 'r').read().split())
            assert H * W <= self._BUFFER_SIZE
            return Vect(W, H)

        def g_pos(scr_size):
            """
            Retourne un générateur sur tous les position de l'écran
            dans l'ordre d'affichage
            """
            for scr_y in range(scr_size.y, 0, -1):
                for scr_x in range(scr_size.x):
                    yield Vect(scr_x, scr_y)

        def set_cursor_pos(pos=Vect(0, 0)):
            """ positionne le curseur dans l'écran """
            print('\033[{};{}H'.format(pos.x, pos.y), end='')


        scr_size = screen_size()
        tab_xy_max = Vect(len(render_tab), len(render_tab[0]))

        set_cursor_pos()
        for scr in g_pos(scr_size):
            tab_xy = scr + pos - scr_size // 2
            if pos == tab_xy:
                sprint("@")
            elif Vect(0, 0) <= tab_xy < tab_xy_max:
                char = render_tab[tab_xy.x][tab_xy.y]
                sprint(char)
            else:
                sprint(' ')
        sys.stdout.flush()


def main():
    """
    TU
    """
    import time
    from random import choice

    try:
        data = [[choice([' ', '.']) for _ in range(500)] for _ in range(500)]
        screen = Screen()

        pos = Vect(10, 5)
        while True:
            screen.update(data, pos)
            time.sleep(0.1)

    finally:
        # Pour avoir les erreures à la fin du programme
        del screen


if __name__ == "__main__":
    main()
