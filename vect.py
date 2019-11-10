#!/usr/bin/env python3
# pylint: disable=C0103
"""
Définie la classe Vect
"""
from random import randint
from math import sqrt

class Vect():
    """
    Un simple vecteur 2D sur ZZ
    """
    def __init__(self, x=0, y=0):
        """ v = (x, y) """
        self.x, self.y = x, y

    def __add__(self, other):
        """
        Retourne la somme de deux vecteurs
        Exemple : v = v_self + v_other
        """
        return Vect(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """
        Retourne la diff de deux vecteurs
        Exemple : v = v_self + v_other
        """
        return Vect(self.x - other.x, self.y - other.y)

    def __and__(self, v):
        """
        Applique un masque(=fc(v)) à self
        """
        return Vect(self.x if v.x else 0, self.y if v.y else 0)

    def __floordiv__(self, v):
        """
        division entière sur les somposantes
        """
        return Vect(self.x // v, self.y // v)

    def __le__(self, v):
        """
        compare deux vecteurs : v1 <= v2
        Retourne vrai si la propriete est vraie sur x et y
        """
        return self.x <= v.x and self.y <= v.y

    def __lt__(self, v):
        """
        compare deux vecteurs : v1 < v2
        Retourne vrai si la propriete est vraie sur x et y
        """
        return self.x < v.x and self.y < v.y

    def __ge__(self, v):
        """
        compare deux vecteurs : v1 >= v2
        Retourne vrai si la propriete est vraie sur x et y
        """
        return self.x >= v.x and self.y >= v.y

    def __gt__(self, v):
        """
        compare deux vecteurs : v1 > v2
        Retourne vrai si la propriete est vraie sur x et y
        """
        return self.x > v.x and self.y > v.y

    def __eq__(self, v):
        """
        compare deux vecteurs : v1 == v2
        Retourne vrai si la propriete est vraie sur x et y
        """
        return self.x == v.x and self.y == v.y

    def __ne__(self, v):
        """
        compare deux vecteurs : v1 != v2
        Retourne vrai si la propriete est vraie sur x ou y
        """
        return self.x != v.x or self.y != v.y


    def dirrectionTo(self, p2):
        """
        Retourne le deplacement à réaliser pour passe de p1 à p2
        """
        # Retourne la variation des valeurs normalisé à 1
        myCmp = lambda v1, v2: int(v1 > v2) - int(v1 < v2)
        return Vect(myCmp(p2.x, self.x), myCmp(p2.y, self.y))

    def quadrant(self, p2):
        """
        Détermination de quadrant
        """
        #
        #            \ (0,1) /
        #             +-----+       (X2)
        #             |\   /|
        #             | \ / |
        #      (-1,0) | (X1) | (1,0)
        #             | / \ |
        #             |/   \|
        #             +-----+
        #            / (0,-1)\
        #
        depl = self.dirrectionTo(p2)
        return  depl & Vect(depl.x >= depl.y, depl.x < depl.y)

    def __or__(self, v):
        """
        Retourne un vecteur aléatoire entre self et v
        Exemple : V = v1 | v2
        """
        return Vect(randint(self.x, v.x), randint(self.y, v.y))

    def distanceSquare(self, other):
        """
        Retourne la norme² de la différence de deux vecteurs
        """
        delta = self - other
        return delta.x ** 2 + delta.y ** 2

    def distance(self, other):
        """
        Retourne la norme de la différence de deux vecteurs
        """
        return sqrt(self.distanceSquare(other))

    def __str__(self):
        """
        str(point) => "(x, y)"
        """
        return "({},{})".format(self.x, self.y)

def tu():
    """
    Test unitaire
    """
    # Affectation
    v = Vect(1, 2)
    assert v.x == 1
    assert v.y == 2

    # Comparaison et masquage
    assert Vect(0, 0) < Vect(1, 1)
    assert Vect(1, 1) == Vect(1, 1)
    assert Vect(33, 0) == Vect(33, 44) & Vect(True, False)
    assert Vect(10, 30) == Vect(5, 10) + Vect(5, 30) - Vect(0, 10)

    # Random
    v0 = Vect(0, 0)
    v10 = Vect(10, 10)
    for _ in range(100):
        vr = v0 | v10
        assert 0 <= vr.x <= 10 and 0 <= vr.y <= 11

    # Str
    print(v0, "<=", vr, "<=", v10)
    print("OK")
if __name__ == '__main__':
    tu()
