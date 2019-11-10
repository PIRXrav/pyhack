#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Core
"""
from random import randint


class Core:
    """
    Cette classe contient tout le coeur du jeu
        * les données
        * l' update
    """
    # définition du plateau
    _XMAX = 200
    _YMAX = 200
    _USER = '@'
    _BLOK = '#'
    _NOTH = ' '

    #définition du personnage
    _POSX = 0
    _POSY = 0

    def __init__(self):
        """
        Initialisation
        """
        self.plateau = [[self._NOTH for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        self.pos_x = self._POSX
        self.pos_y = self._POSY

    def generatePlateau(self):
        """
        Genere les salles du jeu <=> initialise tab
        """
        for _ in range(1000):
            self.plateau[randint(0, self._XMAX-1)][randint(0, self._YMAX-1)] = '#'

    def update(self, event_array):
        """
        Met le jeu à jour fc(tous les events)
        """
        from pynput.keyboard import Key

        # position desire (componsation des fleches opposées)
        new_pos_x = self.pos_x + int(Key.right in event_array) - int(Key.left in event_array)
        new_pos_y = self.pos_y + int(Key.up in event_array) - int(Key.down in event_array)

        self.plateau[self.pos_x][self.pos_y] = ' '

        # Tests de collision (Diagonales)
        if self.plateau[new_pos_x][self.pos_y] != '#':
            #premier chemin libre en x
            if self.plateau[new_pos_x][new_pos_y] != '#':
                #deuxieme chemin libre en y
                self.pos_x, self.pos_y = new_pos_x, new_pos_y
            else:
                #deuxieme chemin bloque en y
                self.pos_x, self.pos_y = new_pos_x, self.pos_y
        elif self.plateau[self.pos_x][new_pos_y] != '#':
            #premier chemin libre en y
            if self.plateau[new_pos_x][new_pos_y] != '#':
                #deuxieme chemin libre en x
                self.pos_x, self.pos_y = new_pos_x, new_pos_y
            else:
                #deuxieme chemin bloque en x
                self.pos_x, self.pos_y = self.pos_x, new_pos_y
        else:
            # Aucun chemin libre
            # Do nothind
            pass

        self.plateau[self.pos_x][self.pos_y] = '@'
