import pygame
import sys
import math
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pygame Agent')

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

font = pygame.font.SysFont(None, 36)

num_agents = 5
agents = []
agent_radius = 10
speed = 1

num_green_agents = 3
green_agents = []

target_radius = 15
target = pygame.Rect(width // 2, height // 2, target_radius * 2, target_radius * 2)

score = 0

for i in range(num_agents):
    x = random.randint(agent_radius, width - agent_radius)
    y = random.randint(agent_radius, height - agent_radius)
    agents.append(pygame.Rect(x, y, agent_radius * 2, agent_radius * 2))

for i in range(num_green_agents):
    x = random.randint(agent_radius, width - agent_radius)
    y = random.randint(agent_radius, height - agent_radius)
    green_agents.append(pygame.Rect(x, y, agent_radius * 2, agent_radius * 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            target.x, target.y = event.pos

    screen.fill(black)
    pygame.draw.ellipse(screen, blue, target)

    for agent in agents:
        dx, dy = target.centerx - agent.centerx, target.centery - agent.centery
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist
        agent.x += dx * speed
        agent.y += dy * speed
        pygame.draw.ellipse(screen, red, agent)

    for green_agent in green_agents:
        pygame.draw.ellipse(screen, green, green_agent)
        if target.colliderect(green_agent):
            score += 1
            green_agent.x = random.randint(agent_radius, width - agent_radius)
            green_agent.y = random.randint(agent_radius, height - agent_radius)

    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (width - 150, 10))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
