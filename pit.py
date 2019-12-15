#!/usr/bin/env python3
# pylint: disable=C0103
# pylint: disable=W0312

"""
Définie la classe PIT
"""

import time

class Pit:
	"""
	PIT
	"""
	def __init__(self, period_ms, callback):
		"""
		Initialise un timer périodique
		periode_ms : le temps entre deux callbacks
		callback : la fonction de callback
		pour Stop le PIT, elle doit retourner 0
		"""
		self.run = 0
		self.overflow = 0
		self.period_ms = period_ms
		self.callback = callback

	def runner(self):
		"""
		run
		"""
		init_time = time.time()

		consigne = 0
		erreur = 0
		mesure = -self.period_ms

		self.run = 1
		while self.run:
			########### Begin User code ###########
			mstr = "ERR = {} | UC = {}%".\
					 format(round(erreur, 1), round(erreur * 1 / self.period_ms * 100, 1))
			if not self.callback(mstr):
				self.stop()
				return True
			########### End User code ###########
			mesure = time.time() - init_time
			erreur = mesure - consigne
			commande = self.period_ms - erreur
			if commande < 0: #Les fps sont limité par les performances
				commande = 0
				self.overflow += 1
			else:
				self.overflow = 0
			consigne = consigne + self.period_ms
			time.sleep(commande)

	def start(self):
		"""
		Lance le pit
		"""
		assert not self.run, "[PIT] start déja effectué"
		self.runner()

	def __bool__(self):
		"""
		Retourne si le pit est en fonctionnement
		"""
		return self.run

	def isAlive(self):
		"""
		Retournr si le pit est stable
		overflow != 0 <=> t_callbacl > t_period
		"""
		return self.overflow

	def stop(self):
		"""
		Stop le pit
		"""
		assert self.run, "[PIT] déja stoppé"
		self.run = 0

	def wait_stop(self):
		"""
		Attend la fin du thread
		"""
		while self.run:
			# do nothing
			pass
		return True


def func_test(args):
	""" TU """
	from random import random
	print(args)
	# Crash ?
	for _ in range(99999):
		_ = 3^80
	return random() > 0.01


def main():
	"""
	TU
	"""
	print("Hello world")
	pit1 = Pit(0.1, func_test)
	pit1.start()

if __name__ == '__main__':
	main()
