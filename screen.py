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

from itertools import chain
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
        return Vect(W, H)

    def update(self, chars):
        """
        Actualise l'écran
        chars : generateur de caractères ordonnés
        """
        for char in chain('\033[0;0H', chars):
            self.my_print(char) # <=> print(char, end='', flush=False)
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
