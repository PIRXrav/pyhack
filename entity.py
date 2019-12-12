#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe entity
Permet de modeliser le personnage et des monstre
"""

from vect import Vect
from astar import calc_path_astart
from random import randint, choice

class Entity:
    """
    Entity
    """
    def __init__(self):
        self.hp = 100
        self.weapon = "Gun n°5"
        # weapon
        self.nb_bullet = 1
        self.shoot_tempo = 3

class Player():
    """
    Classe Player :
    """
    def __init__(self, x, y):
        """
        Personnage
        """
        self.pos = Vect(x, y)
        self.direction = Vect(1, 0)
        self.distance_view = 5
        self.bullet = 10
        self.dammage = 10
        self.hp = 10
        # RENDER
        self.char = '@'
        self.money = 0

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
        return Bullet(self.pos, self.direction, self.dammage)

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
        return self.char

class Bullet:
    """
    Classe Bullet :
    """
    def __init__(self, pos, directions, dammage):
        """
        Personnage
        """
        self.pos = pos
        self.direction = directions
        self.dammage = dammage
        self.chars = ['>', '/', '^', '\\', '<', '/', 'v', '\\']

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
        return self.chars[int(self.direction.angle()/2/3.1415 * 8)]

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

    def __init__(self, pos, directions, dammage):
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
    HEART = 0
    BULLET = 1
    GOLD = 2
    CHARS = ['\u2665', '\u25B2', '$']

    def __init__(self, pos):
        """
        Trésor, peut contenir 3 types d'objet différents : des sous, des munitions et de la vie
        """
        self.pos = pos
        self.object = choice([self.HEART, self.BULLET, self.GOLD])     # 0 = vie, 1 = munition, 2 = argent

    def render(self):
        return self.CHARS[self.object]

def main():
    """
    Test unitaire
    """

if __name__ == '__main__':
    main()
