#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe entity
Permet de modeliser le personnage et des monstre
"""

from vect import Vect
from astar import calc_path_astart
from random import randint, choice

class Player():
    """
    Classe Player :
    """

    BULLET_MAX = 10
    HP_MAX = 10
    START_MONEY = 0
    CHAR = '@'

    def __init__(self, x, y):
        """
        Personnage
        """
        self.pos = Vect(x, y)
        self.direction = Vect(1, 0)
        self.distance_view = 7

        self.bullet = self.BULLET_MAX
        self.hp = self.HP_MAX
        self.money = self.START_MONEY

    def g_case_visible(self, mat_collide):
        """
        retourne sur toutes les cases visibles
        par self dans mat_collide
        """
        # Nb : prend les segments depuis un cercle et non un rect
        # n'est pas OK
        border = self.pos.g_rect(Vect(self.distance_view, self.distance_view))
        for bordure_pos in border:
            for pos in self.pos.g_bresenham_line(bordure_pos):
                if self.pos.distance(pos) >= self.distance_view:
                    break
                if not Vect(0, 0) <= pos < Vect(len(mat_collide), len(mat_collide[0])):
                    break
                if not mat_collide[pos.x][pos.y]:
                    yield pos
                    break
                yield pos

    def shoot(self):
        """
        Tire une nouvelle balle
        """
        self.bullet -= 1
        return Bullet(self.pos, self.direction, 42)

    def strike(self, mat_collide):
        """
        Donne un coup d'épée
        """
        return Sword(self.pos + self.direction)

    def add_money(self, value):
        """
        Ajoute des pièces au Player
        """
        assert value >= 0
        self.money += value
        return True

    def add_hp(self, value):
        """
        Ajoute des HP au Player
        """
        assert value >= 0
        if self.hp == self.HP_MAX:
            return False
        self.hp = min(self.hp + value, self.HP_MAX)
        return True

    def add_bullets(self, value):
        """
        Ajoute des balles au Player
        """
        assert value >= 0
        if self.bullet == self.BULLET_MAX:
            return False
        self.bullet = min(self.bullet + value, self.BULLET_MAX)
        return True

    def update(self, mat_collide, depl_vect):
        """
        Met à jour la position du personnage en fonction des evenements
        et de mat_collide
        """
        if depl_vect != Vect(0, 0):
            self.direction = depl_vect
            new_pos = self.pos + depl_vect
            # Tests de collision (Diagonales)
            if mat_collide[new_pos.x][self.pos.y]:
                # premier chemin libre en x
                if mat_collide[new_pos.x][new_pos.y]:
                    # deuxieme chemin libre en y
                    self.pos = new_pos
                else:
                    # deuxieme chemin bloque en y
                    self.pos.x = new_pos.x
            elif mat_collide[self.pos.x][new_pos.y]:
                # premier chemin libre en y
                if mat_collide[new_pos.x][new_pos.y]:
                    # deuxieme chemin libre en x
                    self.pos = new_pos
                else:
                    # deuxieme chemin bloque en x
                    self.pos.y = new_pos.y
            else:
                # Aucun chemin libre
                # Do nothind
                pass

    def render(self):
        """
        Retourne le char à afficher
        """
        return self.CHAR

    def __str__(self):
        """
        Retourne une chaine d'affichage
        """
        heal_str = '[{}]'.format('\u2665' * int(self.hp / self.HP_MAX * 10)
                                 + " "* (10-int(self.hp / self.HP_MAX * 10)))
        bullet_str = '[{}]'.format('|' * (self.bullet)
                                   + " " * (self.BULLET_MAX - self.bullet))

        return 'Position : {} | HP : {} | Bullets {}'.format(
            self.pos, heal_str, bullet_str
        )

class Bullet:
    """
    Classe Bullet :
    """
    CHARS = ['>', '/', '^', '\\', '<', '/', 'v', '\\']

    def __init__(self, pos, directions, dammage):
        """
        Personnage
        """
        self.pos = pos
        self.direction = directions
        self.dammage = dammage

    def update(self, mat_collide):
        """
        Met à jour la balle
        Retourne 1 si elle touche un obstacle
        """
        self.pos += self.direction
        return mat_collide[self.pos.x][self.pos.y]

    def render(self):
        """
        Retourne le char à afficher
        """
        return self.CHARS[int(self.direction.angle()/2/3.1415 * 8)]

    def __str__(self):
        return "(*:{})".format(self.pos)

class Monster:
    """
    Classe Bullet :
    """
    """
    Etat du personnage
    """
    IDLE = 0
    RUN = 1
    DECOMPOSITION = 2

    def __init__(self, pos, dammage):
        """
        Personnage
        """
        self.pos = pos
        self.dammage = dammage


        self.state = self.IDLE
        self.ttd = 8 # TIme to die
        self.chars = ["\033[33m" + 'X' + "\033[0m",
                      "\033[35m" + 'X' + "\033[0m",
                      'X']
        # TEMP
        # Le chemin du monstre au joueur
        self.path = []

    def update(self, mat_collide, player_pos):
        """
        Met à jour l'enemie
        """
        if self.state == self.IDLE or self.state == self.RUN:
            if self.pos.distance(player_pos) <= 10:
                self.state = self.RUN
            else:
                self.state = self.IDLE

            if self.state == self.RUN:
                self.path = calc_path_astart(mat_collide, self.pos, player_pos)
                if self.path != []:
                    self.pos = self.path[0]
            return False

        self.ttd -= 1
        return self.ttd == 0 # Mort

    def render(self):
        """
        Retourne le char à afficher
        """
        return self.chars[self.ttd % len(self.chars)]

    def kill(self):
        """
        Elimine le mechant
        """
        self.state = self.DECOMPOSITION

    def __str__(self):
        return "(*:{})".format(self.pos)


class Treasure:
    """
    Trésor, peut contenir 3 types d'objet différents :
        * des sous
        * des munitions
        * de la vie
    """
    HEART = 0
    BULLET = 1
    GOLD = 2
    CHARS = ['\u2665', '\u25B2', '$']

    def __init__(self, pos, value):
        """
        Init
        """
        self.pos = pos
        self.object = choice([self.HEART, self.BULLET, self.GOLD])
        self.value = value

    def render(self):
        """
        Render
        """
        return self.CHARS[self.object]

    def get_value(self):
        """
        Retourne la valeur du contenue du coffre
        """
        return self.value


class Sword:
    """
    coup d'épée venant du joueur
    """
    DELTA_POSS = list(Vect(0, 0).g_rect(Vect(1, 1)))
    CHARS_POSS = HARS = ['-', '/', '|', '\\', '-', '/', '|', '\\']

    def __init__(self, pos):

        self.pos = pos
        self.char = '\u25A0'
        self.cpt = len(self.DELTA_POSS)-1


    def update(self, mat_collide, player_pos):
        """
        Met à jour l'enemie
        """

        if self.cpt < 0:
            return True

        self.pos = player_pos + self.DELTA_POSS[self.cpt]
        self.cpt -= 1
        return False

    def render(self):
        """
        render
        """
        return self.CHARS_POSS[-self.cpt-1]

def main():
    """
    Test unitaire
    """

if __name__ == '__main__':
    main()
