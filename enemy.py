import pygame
import math
from entity import Entity
class Enemy:
    def __init__(self, x, y):
        super().__init__(x, y, 40)
        self.speed = 180
        self.hp = 5
        self.damage = 10
        self.attack_cooldown = 1
        self.attack_timer = 0
    def update(self, dt, player):
        dx = player.x - self.x
        dy = player.y - self.y
        self.attack_timer += dt
        dist = math.hypot(dx, dy)

        if dist != 0:
            dx /= dist
            dy /= dist

        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt
        if dist < self.size + player.size:

            if self.attack_timer >= self.attack_cooldown:
                player.hp -= self.damage
                self.attack_timer = 0
    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        pygame.draw.circle(screen, (200, 80, 80), (int(screen_x), int(screen_y)), self.size)