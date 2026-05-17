import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y

        self.speed = 500
        self.radius = 5
        self.damage = 1
        dx = target_x - x
        dy = target_y - y

        dist = math.hypot(dx, dy)

        if dist != 0:
            dx /= dist
            dy /= dist

        self.dx = dx
        self.dy = dy

    def update(self, dt):
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt

    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        pygame.draw.circle(
            screen,
            (255, 220, 100),
            (int(screen_x), int(screen_y)),
            self.radius
        )