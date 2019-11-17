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
    _NB_ROOMS = 150

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

    def render(self, scr_size):
        """
        retoure un génerateur des caractères à affiche
        suivant l'ordre d'affichage
        fc(vision, rendu, objets)
        """
        def g_pos(scr_size):
            """
            Retourne un générateur sur tous les position de l'écran
            dans l'ordre d'affichage
            """
            for scr_y in range(scr_size.y, 0, -1):
                for scr_x in range(scr_size.x):
                    yield Vect(scr_x, scr_y)

        tab_xy_max = Vect(self._XMAX, self._YMAX)

        for scr in g_pos(scr_size):
            tab_xy = scr + self.pos - scr_size // 2
            if self.pos == tab_xy:
                yield '@'
            elif Vect(0, 0) <= tab_xy < tab_xy_max:
                yield self.rendertab[tab_xy.x][tab_xy.y]
            else:
                yield ' '
