#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Core
"""
from village import Village
from vect import Vect


class Core:
    """
    Cette classe contient tout le coeur du jeu
        * les données
        * l' update
    """
    # définition du plateau
    _XMAX = 300
    _YMAX = 300
    _NB_ROOMS = 350

    def __init__(self):
        """
        Initialisation
        """
        # Convention : True = libre; False = bloqué
        self.plateau = [[False for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        self.rendertab = [[' ' for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        # Position @
        self.pos = Vect()

    def generate(self):
        """
        Genere les salles du jeu <=> initialise tab
        """
        village = Village(self._XMAX, self._YMAX, self._NB_ROOMS)
        village.generate()

        self.pos = village.rooms[0].p[0] + village.rooms[0].size // 2

        # COLLIDES
        for pos in village.g_xyCollide():
            self.plateau[pos.x][pos.y] = True

        # RENDER
        for pos, char in village.g_xyRender():
            self.rendertab[pos.x][pos.y] = char


    def update(self, events):
        """
        Met le jeu à jour fc(tous les events)
        """
        from pynput.keyboard import Key

        # position desire (componsation des fleches opposées)
        new_pos = self.pos + \
                  Vect(int(Key.right in events) - int(Key.left in events),
                       int(Key.up in events) - int(Key.down in events))

        # Tests de collision (Diagonales)
        if self.plateau[new_pos.x][self.pos.y]:
            #premier chemin libre en x
            if self.plateau[new_pos.x][new_pos.y]:
                #deuxieme chemin libre en y
                self.pos = new_pos
            else:
                #deuxieme chemin bloque en y
                self.pos.x = new_pos.x
        elif self.plateau[self.pos.x][new_pos.y]:
            #premier chemin libre en y
            if self.plateau[new_pos.x][new_pos.y]:
                #deuxieme chemin libre en x
                self.pos = new_pos
            else:
                #deuxieme chemin bloque en x
                self.pos.y = new_pos.y
        else:
            # Aucun chemin libre
            # Do nothind
            pass

        # self.rendertab[self.pos_x][self.pos_y] = '@'
