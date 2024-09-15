import pygame
import random
import math

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

NUM_BOIDS = 500
BOID_SIZE = 5
MAX_SPEED = 4
MAX_FORCE = 0.05
NEIGHBOR_RADIUS = 50
SEPARATION_RADIUS = 25

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 50, 255)

def vector_magnitude(vec):
    return math.sqrt(vec[0]**2 + vec[1]**2)

def normalize_vector(vec):
    mag = vector_magnitude(vec)
    if mag == 0:
        return [0, 0]
    return [vec[0] / mag, vec[1] / mag]

def limit_vector(vec, max_value):
    if vector_magnitude(vec) > max_value:
        vec = normalize_vector(vec)
        vec[0] *= max_value
        vec[1] *= max_value
    return vec


class Boid:
    def __init__(self):
        self.position = [random.uniform(0, width), random.uniform(0, height)]
        self.velocity = [random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED)]
        self.acceleration = [0, 0]

    def update(self):
        self.velocity[0] += self.acceleration[0]
        self.velocity[1] += self.acceleration[1]
        
        self.velocity = limit_vector(self.velocity, MAX_SPEED)
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.acceleration = [0, 0]

        if self.position[0] < 0: self.position[0] = width
        if self.position[0] > width: self.position[0] = 0
        if self.position[1] < 0: self.position[1] = height
        if self.position[1] > height: self.position[1] = 0

    def apply_force(self, force):
        self.acceleration[0] += force[0]
        self.acceleration[1] += force[1]

    def flock(self, boids):
        sep = self.separation(boids)
        ali = self.alignment(boids)
        coh = self.cohesion(boids)

        sep = [sep[0] * 1.5, sep[1] * 1.5]

        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

    def separation(self, boids):
        steer = [0, 0]
        total = 0
        for other in boids:
            dist = math.sqrt((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2)
            if 0 < dist < SEPARATION_RADIUS:
                diff = [self.position[0] - other.position[0], self.position[1] - other.position[1]]
                diff = normalize_vector(diff)
                diff[0] /= dist
                diff[1] /= dist
                steer[0] += diff[0]
                steer[1] += diff[1]
                total += 1
        if total > 0:
            steer[0] /= total
            steer[1] /= total
        if vector_magnitude(steer) > 0:
            steer = normalize_vector(steer)
            steer[0] *= MAX_SPEED
            steer[1] *= MAX_SPEED
            steer[0] -= self.velocity[0]
            steer[1] -= self.velocity[1]
            steer = limit_vector(steer, MAX_FORCE)
        return steer

    def alignment(self, boids):
        avg_velocity = [0, 0]
        total = 0
        for other in boids:
            dist = math.sqrt((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2)
            if 0 < dist < NEIGHBOR_RADIUS:
                avg_velocity[0] += other.velocity[0]
                avg_velocity[1] += other.velocity[1]
                total += 1
        if total > 0:
            avg_velocity[0] /= total
            avg_velocity[1] /= total
            avg_velocity = normalize_vector(avg_velocity)
            avg_velocity[0] *= MAX_SPEED
            avg_velocity[1] *= MAX_SPEED
            steer = [avg_velocity[0] - self.velocity[0], avg_velocity[1] - self.velocity[1]]
            return limit_vector(steer, MAX_FORCE)
        return [0, 0]

    def cohesion(self, boids):
        center_of_mass = [0, 0]
        total = 0
        for other in boids:
            dist = math.sqrt((self.position[0] - other.position[0]) ** 2 + (self.position[1] - other.position[1]) ** 2)
            if 0 < dist < NEIGHBOR_RADIUS:
                center_of_mass[0] += other.position[0]
                center_of_mass[1] += other.position[1]
                total += 1
        if total > 0:
            center_of_mass[0] /= total
            center_of_mass[1] /= total
            return self.seek(center_of_mass)
        return [0, 0]

    def seek(self, target):
        desired = [target[0] - self.position[0], target[1] - self.position[1]]
        desired = normalize_vector(desired)
        desired[0] *= MAX_SPEED
        desired[1] *= MAX_SPEED
        steer = [desired[0] - self.velocity[0], desired[1] - self.velocity[1]]
        return limit_vector(steer, MAX_FORCE)

    def draw(self):
        pygame.draw.circle(screen, BLUE, (int(self.position[0]), int(self.position[1])), BOID_SIZE)

# Main Loop
boids = [Boid() for _ in range(NUM_BOIDS)]

running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for boid in boids:
        boid.flock(boids)
        boid.update()
        boid.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
