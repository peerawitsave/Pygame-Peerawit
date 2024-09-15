import pygame
import sys
import random


pygame.init()


width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame Agent')


RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Agent:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = 1

    def update(self):
        self.velocity += self.acceleration
        self.position += self.velocity
        self.acceleration *= 0

    def apply_force(self, force):
        self.acceleration += force / self.mass

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.position.x), int(self.position.y)), 10)

agents = []
for i in range(100):
    agents.append( Agent(random.uniform(0, width), random.uniform(0, height)))


clock = pygame.time.Clock()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    screen.fill(BLACK)


    for agent in agents:
        agent.update()
        agent.draw(screen)

    pygame.display.flip()

    clock.tick(60)
