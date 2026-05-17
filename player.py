import pygame
import math
from entity import Entity
class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 20)
        self.speed = 200
        self.max_hp = 100
        self.hp = 40
    def update(self, dt):
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            dx /= length
            dy /= length

        # движение
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

    def draw(self, screen):
        width, height = screen.get_size()
        pygame.draw.circle(screen, (100, 200, 255), (width // 2, height // 2), self.size)