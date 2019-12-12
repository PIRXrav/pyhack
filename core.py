#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Core
"""
from itertools import chain
from random import randint

from pynput.keyboard import Key

from initvillage import Village
from vect import Vect
from entity import Player, Monster, Treasure

class Core:
    """
    Cette classe contient tout le coeur du jeu
        * les données
        * l' update
    """
    # définition du mat_collide
    _XMAX = 100
    _YMAX = 100
    _NB_ROOMS = 20

    RULE_VISION = True

    def __init__(self):
        """
        Initialisation
        """
        # Matrice de collision onvention : True = libre; False = bloqué
        self.mat_collide = [[False for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        # Matrice de vision True = VIsible. False = invisible
        self.mat_view = [[False for _ in range(self._YMAX)] for _ in range(self._XMAX)]
        # Matrice d'affichage du village
        self.mat_render = [[' ' for _ in range(self._YMAX)] for _ in range(self._XMAX)]

        # Entités
        self.player = Player(0, 0)
        self.bullets = []
        self.monsters = []
        self.treasure = []

        # COmpteur de update
        self.cpt = 0

        # Tableau d'affichage final
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
            self.mat_collide[pos.x][pos.y] = True

        # RENDER
        for pos, char in village.g_xyRender():
            self.mat_render[pos.x][pos.y] = char

        #Ajout de coffres (2 max par room) | Monsters
        for room in village.rooms:
            self.monsters.append(Monster(room.newRandomPointInRoom(), 1))
            for _ in range(randint(0, 2)):
                self.treasure.append(Treasure(room.newRandomPointInRoom(), 5))



    def update(self, events):
        """
        Met le jeu à jour fc(tous les events)
        """
        self.cpt += 1

        def get_user_depl(events):
            """
            retourne le vecteur de deplacement
            """
            # position desire (componsation des fleches opposées)
            return Vect(int(Key.right in events) - int(Key.left in events),
                        int(Key.up in events)    - int(Key.down in events))

        def update_player():
            """
            Mise a jour du personnage
            """
            self.player.update(self.mat_collide, get_user_depl(events))
            # Shoot ? et assez de balles ?
            if Key.space in events and self.cpt >= 3 and self.player.bullet:
                self.cpt = 0
                self.bullets.append(self.player.shoot())
            # Mise a jour de la cartograpgie
            for pos in self.player.g_case_visible(self.mat_collide):
                self.mat_view[pos.x][pos.y] = True

        def update_bullets():
            """
            Mise à jour des balles
            """
            for i in range(len(self.bullets)-1, -1, -1):
                if not self.bullets[i].update(self.mat_collide):
                    self.bullets.pop(i)
                else:
                    # TODO: BUG here ?
                    for i_monster in range(len(self.monsters)-1, -1, -1):
                        if self.bullets[i].pos == self.monsters[i_monster].pos:
                            self.monsters[i_monster].kill()
                            self.bullets.pop(i)
                            break

        def update_monsters():
            """
            Mise à jour des monstres
            """
            if self.cpt % 3 == 0:
                for i in range(len(self.monsters)-1, -1, -1):
                    if self.monsters[i].update(self.mat_collide, self.player.pos):
                        # Mort
                        self.monsters.pop(i)
                    else:
                        # Vivant
                        if self.monsters[i].pos == self.player.pos:
                            self.player.hp -= self.monsters[i].dammage

        def update_treasures():
            """
            Mise a jour des coffres
            """
            for i in range(len(self.treasure) - 1, -1, -1):
                if self.treasure[i].pos == self.player.pos:
                    if self.treasure[i].object == Treasure.HEART:
                        if self.player.add_hp(self.treasure[i].value):
                            self.treasure.pop(i)
                    elif self.treasure[i].object == Treasure.BULLET:
                        if self.player.add_bullets(self.treasure[i].value):
                            self.treasure.pop(i)
                    elif self.treasure[i].object == Treasure.GOLD:
                        self.player.add_money(self.treasure[i].value)
                        self.treasure.pop(i)

        update_player()     # Actualise le depl / tirs / vision
        update_bullets()    # Actualise toutes les balles : kill monsters
        update_monsters()   # Actualise les monstres : enleve HP
        update_treasures()  # Actualise les coffres : Ajoute <3 / Balles / $

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
            # Dans matrice et Visible
            if Vect(0, 0) <= mat_pos < Vect(self._XMAX, self._YMAX) and \
                (self.mat_view[mat_pos.x][mat_pos.y] or self.RULE_VISION):
                self.buffer_window[scr.x][scr.y] = self.mat_render[mat_pos.x][mat_pos.y]
            else:
                self.buffer_window[scr.x][scr.y] = ' '

        # Rendu des entitées
        for entity in chain(self.bullets,
                            self.monsters,
                            self.treasure,
                            [self.player]):
            scr_pos = mat2scr(entity.pos)
            if isScrPosInScr(scr_pos) \
                and self.mat_view[entity.pos.x][entity.pos.y] \
                or self.RULE_VISION:
                self.buffer_window[scr_pos.x][scr_pos.y] = entity.render()

        # Text
        top_bar = "{}".format("Town : Koku <> Not safe place ")
        for i, char in enumerate(top_bar):
            self.buffer_window[i][scr_size.y - 1] = char


        decoration = ['|', '/', '-', '\\']
        bot_bat1 = "{} | Monsters : {}".format(self.player, len(self.monsters))
        bot_bat2 = "[{}] Level : 0 | Gold : {} ".format(decoration[self.cpt % 4], self.player.money)

        for i, char in enumerate(bot_bat1):
            self.buffer_window[i][1] = char
        for i, char in enumerate(bot_bat2):
            self.buffer_window[i][2] = char
        # Bousolle
        for y, chars in enumerate(["   N   ", "   ^   ", "W<-o->E", "   v   ", "   S   "]):
            for x, char in enumerate(chars):
                self.buffer_window[scr_size.x - 7 + x][5 - y] = char



        return self.buffer_window
