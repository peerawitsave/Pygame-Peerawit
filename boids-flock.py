import pygame
import random
import math


pygame.init()
width, height = 1920, 1080
screen = pygame.display.set.mode((width, height))
clock = pygame.time.Clock()

NUM_BOIDS = 50
BOID_SIZE = 5
MAX_SPEED = 4
MAX_FORCE = 0.05
NEIGHBOR_RADIUS = 50
SEPERATION_RADIUS = 25