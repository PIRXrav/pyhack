#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Core
"""
from initvillage import Village
from vect import Vect

from entity import Player, Bullet

class Core:
    """
    Cette classe contient tout le coeur du jeu
        * les données
        * l' update
    """
    # définition du plateau
    _XMAX = 300
    _YMAX = 300
    _NB_ROOMS = 5

    def __init__(self):
        """
        Initialisation
        """
        # Matrice de collision onvention : True = libre; False = bloqué
        self.plateau = [[False for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        # Matrice de rendu
        self.rendertab = [[' ' for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        # Matrice de vision True = VIsible. False = invisible
        self.mat_view = [[False for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        # Position @
        self.player = Player(0, 0)
        self.bullets = []

        self.cpt = 0

    def generate(self):
        """
        Genere les salles du jeu <=> initialise tab
        """
        village = Village(self._XMAX, self._YMAX, self._NB_ROOMS)
        village.generate()

        self.player.pos = village.rooms[0].p[0] + village.rooms[0].size // 2

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

        self.cpt += 1

        from pynput.keyboard import Key
        # position desire (componsation des fleches opposées)
        depl = Vect(int(Key.right in events) - int(Key.left in events),
                    int(Key.up in events) - int(Key.down in events))

        # Mise a jour du personnage
        # Shoot ?
        self.player.update(self.plateau, depl)
        if Key.space in events and self.cpt >10:
            self.cpt = 0
            self.bullets.append(self.player.shoot())


        # Mise a jout de la cartograpgie
        for pos in self.player.g_case_visible(self.plateau):
            self.mat_view[pos.x][pos.y] = True

        for i in range(len(self.bullets)-1, -1, -1):
            res = self.bullets[i].update(self.plateau)
            if not res:
                self.bullets.pop(i)


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
            for scr_y in range(scr_size.y-1, 0, -1):
                for scr_x in range(scr_size.x):
                    yield Vect(scr_x, scr_y)

        tab_xy_max = Vect(self._XMAX, self._YMAX)

        for scr in g_pos(scr_size):
            tab_xy = scr + self.player.pos - scr_size // 2

            if Vect(0, 0) <= tab_xy < tab_xy_max:
                # Dans ecran
                if self.mat_view[tab_xy.x][tab_xy.y]:
                    # Visible
                    if tab_xy == self.player.pos:
                        # Position joueur
                        yield self.player.char
                    elif sum((tab_xy == bult.pos) for bult in self.bullets):
                         yield '*'
                    else:
                        # Terrain
                        yield self.rendertab[tab_xy.x][tab_xy.y]
                else:
                    yield ' '
            else:
                yield ' '

        for char in "{},{}".format(self.player.pos, self.bullets):
            yield char
