import random # Pour les tirages aleatoires
import sys # Pour quitter proprement
import pygame # Le module Pygame
import pygame.freetype # Pour afficher du texte
import math

pygame.init() # initialisation de Pygame


# Taille de la fenetre
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Casse Briques")

# Pour limiter le nombre d'images par seconde
clock=pygame.time.Clock()

BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
FOND=(14,54,84)
DEFAITE=(155,32,32)
DEBUT=(9,122,73)
VICTOIRE=(93,12,146)
STAGE=(205,17,17)
RAYON_BALLE = 10
XMIN, YMIN = 0, 0
XMAX, YMAX = width, height


font = pygame.font.SysFont(None,25)
font2 = pygame.font.SysFont(None,35)
