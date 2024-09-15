import pygame
import sys
import random
import math

pygame.init()

width, height = 800, 600
MAX_SPEED = 5

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
        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        self.position += self.velocity
        self.acceleration = pygame.Vector2(0, 0)

    def apply_force(self, x, y):
        force = pygame.Vector2(x, y)
        self.acceleration = self.acceleration + (force / self.mass)

    def seek(self, x, y):
        d = pygame.Vector2(x, y) - self.position
        d = d.normalize() * 0.1
        seeking_force = d
        self.apply_force(seeking_force.x, seeking_force.y)

    def coherence(self, agents):
        total = pygame.Vector2(0, 0)
        count = 0
        for agent in agents:
            if agent != self:
                total += agent.position
                count += 1
        
        if count > 0:   
            center_of_mass = total/count
            d = center_of_mass - self.position
            if d.length() > 0:
                coherence_force = d.normalize() * 0.05
                self.apply_force(coherence_force.x, coherence_force.y)


    def seperation(self, agents):
        d = pygame.Vector2(0, 0)
        for agent in agents:
            dist = math.sqrt((self.position.x - agent.position.x)**2 + (self.position.y - agent.position.y)**2)
            
            if dist < 25:
                d += self.position - agent.position
        
        seperation_force = d * 0.01

        self.apply_force(seperation_force.x, seperation_force.y)


    def alignment(self, agents):
        v = pygame.Vector2(0, 0)
        for agent in agents:
            if agent != self:
                v += agent.velocity

        v /= len(agents) - 1
        alignment_f = v * 0.1
        self.apply_force(alignment_f.x, alignment_f.y)



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

    #mouse_x, mouse_y = pygame.mouse.get_pos()

    for agent in agents:
        #agent.seek(mouse_x, mouse_y)
        #agent.alignment(agents)
        agent.coherence(agents)
        agent.update()
        agent.draw(screen)
        agent.seperation(agents)

    pygame.display.flip()
    clock.tick(60)
