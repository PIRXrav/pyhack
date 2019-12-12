#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Core
"""
from itertools import chain

from initvillage import Village
from vect import Vect

from entity import *

class Core:
    """
    Cette classe contient tout le coeur du jeu
        * les données
        * l' update
    """
    # définition du plateau
    _XMAX = 100
    _YMAX = 100
    _NB_ROOMS = 20

    RULE_VISION = True

    def __init__(self):
        """
        Initialisation
        """
        # Matrice de collision onvention : True = libre; False = bloqué
        self.plateau = [[False for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        # Matrice de vision True = VIsible. False = invisible
        self.mat_view = [[False for _ in range(self._YMAX)] for _ in range(self._XMAX)]

        # Matrice d'affichage du village
        self.rendertab = [[' ' for _ in range(self._YMAX)] for _ in range(self._XMAX)]

        # Position @
        self.player = Player(0, 0)
        self.bullets = []
        self.monsters = []

        self.cpt = 0

        self.buffer_window = [[None for _ in range(500)] for _ in range(500)]


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

        # AJout ennemies par rooms
        for room in village.rooms:
            self.monsters.append(Monster(room.newRandomPointInRoom(), Vect(0, 0), 0))

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
        self.player.update(self.plateau, depl)
        # Shoot ?
        if Key.space in events and self.cpt >= 3:
            self.cpt = 0
            self.bullets.append(self.player.shoot())
        # Mise a jout de la cartograpgie
        for pos in self.player.g_case_visible(self.plateau):
            self.mat_view[pos.x][pos.y] = True

        # Monster
        if self.cpt % 2 == 0:
            for monster in self.monsters:
                monster.update(self.plateau, self.player.pos)
                if monster.pos == self.player.pos:
                    self.player.hp -= 1



        # Mise à jour des armes
        for i in range(len(self.bullets)-1, -1, -1):
            if not self.bullets[i].update(self.plateau):
                self.bullets.pop(i)

        # Mise a jour des ennemies

    def render(self, scr_size, g_scr_pos):
        """
        retoure un génerateur des caractères à affiche
        suivant l'ordre d'affichage
        fc(vision, rendu, objets)
        """

        scr2mat = lambda scr_pos: scr_pos + self.player.pos - scr_size // 2
        mat2scr = lambda mat_pos: mat_pos - self.player.pos + scr_size // 2
        isScrPosInScr = lambda scr_pos: Vect(0, 0) <= scr_pos < scr_size

        # Rendu du fond
        for scr in g_scr_pos:
            mat_pos = scr2mat(scr)
            if Vect(0, 0) <= mat_pos < Vect(self._XMAX, self._YMAX):
                # Dans ecran
                if self.mat_view[mat_pos.x][mat_pos.y] or self.RULE_VISION:
                    # Visible
                    self.buffer_window[scr.x][scr.y] = self.rendertab[mat_pos.x][mat_pos.y]
                else:
                    self.buffer_window[scr.x][scr.y] = ' '
            else:
                self.buffer_window[scr.x][scr.y] = ' '


        # A star DEBUG
        #for monster in self.monsters:
        #    for pos in monster.path:
        #        scr_pos = mat2scr(pos)
        #        if isScrPosInScr(scr_pos):
        #            self.buffer_window[scr_pos.x][scr_pos.y] = '.'

        # Rendu des entitées
        for entity in chain(self.bullets, self.monsters):
            scr_pos = mat2scr(entity.pos)
            if isScrPosInScr(scr_pos) and self.mat_view[entity.pos.x][entity.pos.y] or self.RULE_VISION:
                self.buffer_window[scr_pos.x][scr_pos.y] = entity.render()



        # Rendu du joueur
        scr_pos = mat2scr(self.player.pos)
        self.buffer_window[scr_pos.x][scr_pos.y] = self.player.render()

        # Text
        top_bar = "{}".format("Town : Koku <> Not safe place ")
        for i, char in enumerate(top_bar):
            self.buffer_window[i][scr_size.y - 1] = char
        decoration = ['|', '/', '-', '\\']
        bot_bat1 = "Position : {} | Heal : {} | Dmg : {} | Bullets {} | Monsters : {}".format(self.player.pos, self.player.hp, 1, len(self.bullets), len(self.monsters))
        bot_bat2 = "[{}] Level : 0 | Gold : 0 ".format(decoration[self.cpt % 4])
        for i, char in enumerate(bot_bat1):
            self.buffer_window[i][1] = char
        for i, char in enumerate(bot_bat2):
            self.buffer_window[i][2] = char
        # Bousolle
        for y, str in enumerate(["   N   ", "   ^   ", "W<-o->E", "   v   ", "   S   "]):
            for x, char in enumerate(str):
                self.buffer_window[scr_size.x - 7 + x][5 - y] = char



        return self.buffer_window
