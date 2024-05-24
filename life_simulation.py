import pygame
import random
import math

# Initialize pygame and window
pygame.init()
window_size = 800
window = pygame.display.set_mode((window_size, window_size))

# Colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Parameters
NUM_ENTITIES = 50
FOOD_COUNT = 200
MAX_AGE = 500
REPRODUCTION_ENERGY = 50
MAX_ENERGY = 100
CLUSTER_RADIUS = 50
ATTACK_RADIUS = 30
REPRODUCE_PROBABILITY = 0.01

# Helper functions


def draw_entity(surface, x, y, color, size):
    pygame.draw.circle(surface, color, (int(x), int(y)), size)


def random_pos():
    return random.randint(0, window_size), random.randint(0, window_size)

# Entity and Food classes


class Entity:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.color = color
        self.energy = MAX_ENERGY // 2
        self.age = 0
        self.cluster = None

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > window_size:
            self.vx *= -1
        if self.y < 0 or self.y > window_size:
            self.vy *= -1

    def update(self):
        self.move()
        self.age += 1
        self.energy -= 0.1  # energy decreases over time
        if self.energy <= 0 or self.age > MAX_AGE:
            return False  # entity dies
        return True

    def eat(self, food):
        if self.energy < MAX_ENERGY:
            self.energy += 20

    def reproduce(self, entities):
        if self.energy > REPRODUCTION_ENERGY:
            self.energy /= 2
            x, y = self.x + \
                random.uniform(-10, 10), self.y + random.uniform(-10, 10)
            entities.append(Entity(x, y, self.color))

    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        draw_entity(surface, self.x, self.y, GREEN, 3)


# Create entities and food
entities = [Entity(*random_pos(), random.choice([YELLOW, RED, BLUE]))
            for _ in range(NUM_ENTITIES)]
food_sources = [Food(*random_pos()) for _ in range(FOOD_COUNT)]

# Main loop
run = True
while run:
    window.fill((0, 0, 0))

    # Update entities
    new_entities = []
    for entity in entities:
        if entity.update():
            new_entities.append(entity)
            # Check for reproduction
            if random.random() < REPRODUCE_PROBABILITY:
                entity.reproduce(new_entities)
        else:
            # Remove dead entity
            pass
    entities = new_entities

    # Assign clusters
    for entity in entities:
        cluster_members = [e for e in entities if e.color ==
                           entity.color and entity.distance(e) < CLUSTER_RADIUS]
        if cluster_members:
            avg_x = sum(e.x for e in cluster_members) / len(cluster_members)
            avg_y = sum(e.y for e in cluster_members) / len(cluster_members)
            entity.vx += (avg_x - entity.x) * 0.01
            entity.vy += (avg_y - entity.y) * 0.01

    # Check for eating
    for entity in entities:
        for food in food_sources[:]:  # Iterate over a copy of the list
            if entity.distance(food) < 10:
                entity.eat(food)
                food_sources.remove(food)
                break

    # Check for attacking
    for entity in entities:
        for other in entities:
            if entity.color != other.color and entity.distance(other) < ATTACK_RADIUS:
                if entity.energy > other.energy:
                    entity.energy += other.energy
                    other.energy = 0  # The other entity dies

    # Draw entities and food
    for entity in entities:
        draw_entity(window, entity.x, entity.y, entity.color, 5)
    for food in food_sources:
        food.draw(window)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                run = False

    pygame.display.flip()

pygame.quit()
exit()
