#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe entity
Permet de modeliser le personnage et des monstre
"""

from vect import Vect

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
        self.hp = 100

        self.name = "Boby"

        self.char = '@'


        # weapon
        self.dammage = 10
        self.weapon = "Gun n°5"
        self.nb_bullet = 1
        self.shoot_tempo = 3

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
        """
        Mise a jour de la position et de la direction en fonction des events
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

class Bullet:
    """
    Classe Player :
    """
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
        # TODO : style
        return '*'

    def __str__(self):
        return "(*:{})".format(self.pos)

def main():
    """
    Test unitaire
    """
    SIZE_Y = 25
    SIZE_X = 100
    screen = [[' ' for _ in range(SIZE_Y)] for _ in range(SIZE_X)]


if __name__ == '__main__':
    main()
