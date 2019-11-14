#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Core
"""
from random import randint
from village import Village
from vect import Vect

class Core:
    """
    Cette classe contient tout le coeur du jeu
        * les données
        * l' update
    """
    # définition du plateau
    _XMAX = 1000
    _YMAX = 1000
    _NB_ROOMS = 100

    def __init__(self):
        """
        Initialisation
        """
        self.plateau = [[1 for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        self.rendertab = [[' ' for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        self.pos_x = None
        self.pos_y = None

    def generate(self):
        """
        Genere les salles du jeu <=> initialise tab
        """
        village = Village(self._XMAX, self._YMAX, self._NB_ROOMS)
        village.generate()

        self.pos_x = village.rooms[0].p[0].x + 1
        self.pos_y = village.rooms[0].p[0].y + 1


        # COLLIDES
        for pos in village.g_xyCollide():
            self.plateau[pos.x][pos.y] = False

        # RENDER
        for pos, char in village.g_xyRender():
            self.rendertab[pos.x][pos.y] = char


    def update(self, event_array):
        """
        Met le jeu à jour fc(tous les events)
        """
        from pynput.keyboard import Key

        # position desire (componsation des fleches opposées)
        new_pos_x = self.pos_x + int(Key.right in event_array) - int(Key.left in event_array)
        new_pos_y = self.pos_y + int(Key.up in event_array) - int(Key.down in event_array)

        # self.renderTab[self.pos_x][self.pos_y] = ' '

        # Tests de collision (Diagonales)
        if self.plateau[new_pos_x][self.pos_y] != True:
            #premier chemin libre en x
            if self.plateau[new_pos_x][new_pos_y] != True:
                #deuxieme chemin libre en y
                self.pos_x, self.pos_y = new_pos_x, new_pos_y
            else:
                #deuxieme chemin bloque en y
                self.pos_x, self.pos_y = new_pos_x, self.pos_y
        elif self.plateau[self.pos_x][new_pos_y] != True:
            #premier chemin libre en y
            if self.plateau[new_pos_x][new_pos_y] != True:
                #deuxieme chemin libre en x
                self.pos_x, self.pos_y = new_pos_x, new_pos_y
            else:
                #deuxieme chemin bloque en x
                self.pos_x, self.pos_y = self.pos_x, new_pos_y
        else:
            # Aucun chemin libre
            # Do nothind
            pass

        self.rendertab[self.pos_x][self.pos_y] = '@'
