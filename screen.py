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
        self._my_fd = sys.stdin.fileno()
        self._old = termios.tcgetattr(self._my_fd)

        # Désactivation echo stdin
        new = termios.tcgetattr(self._my_fd)
        new[3] = new[3] & ~termios.ECHO  # lflags
        termios.tcsetattr(self._my_fd, termios.TCSADRAIN, new)
        # Lancement ecran second + Désactivation curseur
        print("\033[?1049h\033[H" + "\033[?25l", end="")
        sys.stdout.flush()
        # Bufferisarion de stdout
        self._BUFFER_SIZE = 500*500
        sys.stdout = open(sys.stdout.fileno(), "w", self._BUFFER_SIZE)

        # Méthodes d'édition
        self.my_print = sys.stdout.write
        self.my_flush = sys.stdout.flush

        # Taille de l'écran
        self.size = Vect(0, 0)

    def __del__(self):
        """
        Remet la console dans l'état initial
        """
        # Remise de l'état initial console
        termios.tcsetattr(self._my_fd, termios.TCSADRAIN, self._old)
        # Fermeture ecran second + Activation curseur
        print("\033[?1049l" + "\033[?25h", end="")

    def get_size(self):
        """
        Met a jour la taille de l'écran
        """
        # bof ...
        H, W = map(int, os.popen('stty size', 'r').read().split())
        assert H * W <= self._BUFFER_SIZE
        self.size = Vect(W, H)
        return self.size

    def g_pos(self):
        """
        Retourne un générateur sur tous les position de l'écran
        dans l'ordre d'affichage
        """
        for scr_y in range(self.size.y-1, 0, -1):
            for scr_x in range(self.size.x):
                yield Vect(scr_x, scr_y)

    def update(self, scr_tab):
        """
        Actualise l'écran
        """
        self.my_print('\033[0;0H')
        for scr_pos in self.g_pos():
            self.my_print(scr_tab[scr_pos.x][scr_pos.y])# <=> print(char, end='', flush=False)

        self.my_flush()




def main():
    """
    TU
    """
    import time
    from random import choice

    try:

        screen = Screen()

        while True:
            size = screen.get_size()
            screen.update(choice([' ', '.']) for _ in range(size.x * size.y))
            time.sleep(0.1)

    finally:
        # Pour avoir les erreures à la fin du programme
        del screen


if __name__ == "__main__":
    main()
