#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Core
"""
from itertools import chain, zip_longest
from random import randint

from pynput.keyboard import Key

from initvillage import Village
from vect import Vect
from entity import Player, Monster, Treasure, Door
import chars


class Core:
    """
    Cette classe contient tout le coeur du jeu
        * les données
        * l' update
    """
    # définition du mat_collide
    _XMAX = 200
    _YMAX = 150
    _NB_ROOMS = 20

    RULE_VISION = False

    GAME_STATE_RUN = True
    GAME_STATE_MENU = False

    def __init__(self):
        """
        Initialisation
        """
        # Matrice de collision onvention : True = libre; False = bloqué
        self.mat_collide = None
        # Matrice de vision True = VIsible. False = invisible
        self.mat_view = None
        # Matrice d'affichage du village
        self.mat_render = None
        # Entités
        self.player = Player()
        self.door = None
        self.bullets = None
        self.monsters = None
        self.treasure = None
        self.swords = None
        # COmpteur de update
        # TODO : Compteur dans les classes respectives
        self.cpt_bullet = None
        self.cpt_strike = None
        self.cpt_monster = None

        # Tableau d'affichage final
        self.buffer_window = [[None for _ in range(500)] for _ in range(500)]

        # Start !
        self.generate()

        self.game_state = self.GAME_STATE_RUN
        self.timer_state = 0

    def generate(self):
        """
        Genere les salles du jeu <=> initialise tab
        """
        # Generation du village
        village = Village(self._XMAX, self._YMAX, self._NB_ROOMS)
        village.generate()

        # Player dans la premiere salle
        self.player.level_up(village.rooms[0].center)
        self.door = Door(village.rooms[-1].center)
        # ======================== MATRICES =========================
        # Matrice de collision onvention : True = libre; False = bloqué
        self.mat_collide = [[False
                             for _ in range(self._YMAX)]
                            for _ in range(self._XMAX)]
        # Matrice de vision True = VIsible. False = invisible
        self.mat_view = [[False
                          for _ in range(self._YMAX)]
                         for _ in range(self._XMAX)]
        # Matrice d'affichage du village
        self.mat_render = [[' '
                            for _ in range(self._YMAX)]
                           for _ in range(self._XMAX)]
        # COLLIDES
        for pos in village.g_xyCollide():
            self.mat_collide[pos.x][pos.y] = True
        # RENDER
        for pos, char in village.g_xyRender():
            self.mat_render[pos.x][pos.y] = char

        # ======================== ENTITEES =========================
        # Ajout de coffres (2 max par room) | Monsters
        self.bullets = []
        self.monsters = []
        self.treasure = []
        self.swords = []
        for i, room in enumerate(village.rooms):
            if i != 0:
                self.monsters.append(Monster(room.newRandomPointInRoom(),
                                             1 + self.player.level // 3,
                                             1 + self.player.level))
            for _ in range(randint(0, 2)):
                self.treasure.append(Treasure(room.newRandomPointInRoom(),
                                              randint(1, 3)))
        # Cpt
        self.cpt_bullet = 0
        self.cpt_strike = 0
        self.cpt_monster = 0

        self.monster_life = self.monsters[0].health

    def update(self, events):
        """
        Met le jeu à jour fc(tous les events)
        """
        self.cpt_monster += 1
        self.cpt_bullet += 1
        self.cpt_strike += 1

        def get_user_depl(events):
            """
            retourne le vecteur de deplacement
            """
            # position desire (componsation des fleches opposées)
            return Vect(int(Key.right in events) - int(Key.left in events),
                        int(Key.up in events) - int(Key.down in events))

        def update_player():
            """
            Mise a jour du personnage
            """
            self.player.update(self.mat_collide, get_user_depl(events))
            # Shoot ? et assez de balles ?
            if Key.space in events and self.cpt_bullet >= 3 \
               and self.player.bullet:
                self.cpt_bullet = 0
                self.bullets.append(self.player.shoot())
            # Strike
            if Key.shift in events and self.cpt_strike >= 4:
                self.cpt_strike = 0
                self.swords.append(self.player.strike(self.mat_collide))
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
                    for i_monster in range(len(self.monsters)-1, -1, -1):
                        if self.bullets[i].pos \
                           == self.monsters[i_monster].pos \
                           or self.bullets[i].pos + self.bullets[i].direction \
                           == self.monsters[i_monster].pos:
                            self.monsters[i_monster].health -= \
                                self.bullets[i].dammage
                            self.monsters[i_monster].kill()
                            self.bullets.pop(i)
                            break

        def update_sword():
            """²
            Mise à jour de l'épée
            """
            for i in range(len(self.swords)-1, -1, -1):
                if self.swords[i].update(self.mat_collide, self.player.pos):
                    self.swords.pop(i)
                else:
                    for i_monster in range(len(self.monsters)-1, -1, -1):
                        if self.swords[i].pos == self.monsters[i_monster].pos:
                            self.monsters[i_monster].health -= \
                                self.swords[i].dammage
                            self.monsters[i_monster].kill()
                            break

        def update_monsters():
            """
            Mise à jour des monstres
            """
            if self.cpt_monster % 3 == 0:
                for i in range(len(self.monsters)-1, -1, -1):
                    if self.monsters[i].update(self.mat_collide,
                                               self.player.pos):
                        # Mort
                        self.monsters.pop(i)
                    else:
                        # Vivant, le monstre fait des dégats au joueur
                        if self.monsters[i].pos == self.player.pos \
                           and self.monsters[i].state != Monster.DECOMPOSITION:
                            self.player.hp -= 1

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
                    elif self.treasure[i].object == Treasure.STRENGH:
                        self.player.sword_damage += 1
                        self.treasure.pop(i)
                    elif self.treasure[i].object == Treasure.POWER:
                        self.player.gun_damage += 1
                        self.treasure.pop(i)

        self.timer_state += 1

        if Key.esc in events and self.timer_state >= 4:
            self.timer_state = 0
            self.game_state = not self.game_state

        if self.game_state == self.GAME_STATE_RUN:
            update_player()     # Actualise le depl / tirs / vision
            update_monsters()   # Actualise les monstres : enleve HP
            update_bullets()    # Actualise toutes les balles : kill monsters
            update_sword()      # Actualise le coup d'épee
            update_treasures()  # Actualise les coffres : <3 / Balles / $
            if self.player.pos == self.door.pos:
                self.generate()
            return self.player.hp >= 0  # Condition d'arret

        if self.game_state == self.GAME_STATE_MENU:
            return True

    def render(self, scr_size, g_scr_pos, os_info):
        """
        retoure un tableau des caractères à affiche
        suivant l'ordre d'affichage
        fc(vision, rendu, objets)
        """

        def render_run():
            """
            Render state = run
            """
            def scr2mat(scr_pos):
                return scr_pos + self.player.pos - scr_size // 2

            def mat2scr(mat_pos):
                return mat_pos - self.player.pos + scr_size // 2

            def isScrPosInScr(scr_pos):
                return Vect(0, 0) <= scr_pos < scr_size

            # Rendu du fond
            for scr in g_scr_pos:
                mat_pos = scr2mat(scr)
                # Dans matrice et Visible
                if Vect(0, 0) <= mat_pos < Vect(self._XMAX, self._YMAX) and \
                   (self.mat_view[mat_pos.x][mat_pos.y] or self.RULE_VISION):
                    self.buffer_window[scr.x][scr.y] = \
                        self.mat_render[mat_pos.x][mat_pos.y]
                else:
                    self.buffer_window[scr.x][scr.y] = ' '

            # Rendu des entitées
            for entity in chain(self.bullets,
                                self.swords,
                                self.monsters,
                                self.treasure,
                                [self.player],
                                [self.door]):
                scr_pos = mat2scr(entity.pos)
                if isScrPosInScr(scr_pos) \
                   and self.mat_view[entity.pos.x][entity.pos.y] \
                   or self.RULE_VISION:
                    self.buffer_window[scr_pos.x][scr_pos.y] = entity.render()

            # Rendu du joueur
            scr_pos = mat2scr(self.player.pos)
            self.buffer_window[scr_pos.x][scr_pos.y] = self.player.render()

            # Text
            top_bar = "Town : Koku <> ./ [***] " + os_info
            bot_bat1 = str(self.player) + " \
                       | Monsters : " + str(len(self.monsters))
            bot_bat2 = ("["
                        + str(chars.C_BAR_DECORATIONS[self.cpt_monster % 4])
                        + "]"
                        + "| Level : " + str(self.player.level)
                        + "| Gold : " + str(self.player.money)
                        + "| Sword : " + str(self.player.sword_damage)
                        + "| Gun : " + str(self.player.gun_damage)
                        + "| Monster lvl : " + str(self.monster_life))

            for i, ch in enumerate(zip_longest(top_bar,
                                               bot_bat1,
                                               bot_bat2,
                                               range(scr_size.x),
                                               fillvalue=' ')):
                self.buffer_window[i][scr_size.y - 1] = (ch[0])
                self.buffer_window[i][1] = (ch[1])
                self.buffer_window[i][2] = (ch[2])

            # Bousolle
            for y, string in enumerate(["   N   ",
                                        "   ^   ",
                                        "W<-o->E",
                                        "   v   ",
                                        "   S   "]):
                for x, char in enumerate(string):
                    self.buffer_window[scr_size.x - 7 + x][5 - y] = (char)

        def render_menu():
            """
            Render state = menu
            """
            # for scr in g_scr_pos:
            #    self.buffer_window[scr.x][scr.y] = ' '

            scr_center = scr_size // 2
            box_cote = Vect(scr_size.x // 4, scr_size.y // 8)
            for pos in scr_center.g_rect(box_cote):
                self.buffer_window[pos.x][pos.y] = chars.C_PAUSE_BORDER
            for pos in scr_center.g_rect_fill_no_border(box_cote):
                self.buffer_window[pos.x][pos.y] = chars.C_PAUSE_FILL

            for i, char in enumerate("texte"):
                self.buffer_window[scr_center.x - 3 + i][scr_center.y] = char

        if self.game_state == self.GAME_STATE_RUN:
            render_run()
        if self.game_state == self.GAME_STATE_MENU:
            render_run()
            render_menu()

        return self.buffer_window
