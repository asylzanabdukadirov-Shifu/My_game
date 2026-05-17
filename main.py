import pygame
import sys
import random
import math
import json
import os
from player import Player
from enemy import Enemy
from bullet import Bullet
from entity import Entity
# --- настройки ---
WIDTH = 800
HEIGHT = 600
FPS = 60
MENU = 0
PLAYING = 1
GAME_OVER = 2
# --- инициализация ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magic Survival Clone")
clock = pygame.time.Clock()
bg = pygame.image.load("assets/ground.png").convert()
tile_size = bg.get_width()

# --- игрок ---
player = Player(0, 0)
score = 0
highscore = 0
game_state = MENU
enemies = []
bullets = []
spawn_timer = 0
spawn_delay = 2000
game_time = 0
shoot_timer = 0
fire_rate = 500
font = pygame.font.SysFont(None, 36)
# --- основной цикл ---
running = True
def get_nearest_enemy():
    if len(enemies) == 0:
        return None

    nearest = enemies[0]
    nearest_dist = math.hypot(
        player.x - nearest.x,
        player.y - nearest.y
    )

    for enemy in enemies:
        dist = math.hypot(
            player.x - enemy.x,
            player.y - enemy.y
        )

        if dist < nearest_dist:
            nearest = enemy
            nearest_dist = dist

    return nearest
def spawn_enemy():
    angle = random.uniform(0, math.pi * 2)
    distance = random.randint(500, 700)

    x = player.x + math.cos(angle) * distance
    y = player.y + math.sin(angle) * distance

    enemies.append(Enemy(x, y))
while running:

    dt = clock.tick(FPS) / 1000  # delta time

    # --- события ---
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if game_state == GAME_OVER:

                if event.key == pygame.K_r:
                    player = Player(0, 0)

                    enemies.clear()
                    bullets.clear()

                    score = 0
                    spawn_timer = 0

                    player.hp = player.max_hp

                    game_state = PLAYING
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if game_state == MENU:

                if event.key == pygame.K_SPACE:
                    game_state = PLAYING

    # --- логика ---

    player.update(dt)
    game_time += dt
    spawn_timer += dt * 1000
    spawn_delay = max(300, 2000 - game_time * 20)
    shoot_timer += dt * 1000
    if spawn_timer >= spawn_delay:
        spawn_enemy()
        spawn_timer = 0
    if shoot_timer >= fire_rate:
        nearest = get_nearest_enemy()

        if nearest:
            bullets.append(
                Bullet(
                    player.x,
                    player.y,
                    nearest.x,
                    nearest.y
                )
            )

        shoot_timer = 0
    for enemy in enemies:
        enemy.update(dt, player)
    for bullet in bullets:
        bullet.update(dt)
    for bullet in bullets[:]:
        for enemy in enemies[:]:

            dist = math.hypot(
                bullet.x - enemy.x,
                bullet.y - enemy.y
            )

            if dist < bullet.radius + enemy.size:

                enemy.hp -= bullet.damage

                if bullet in bullets:
                    bullets.remove(bullet)

                if enemy.hp <= 0:
                    enemies.remove(enemy)
                    score += 1
                    highscore = 0

                    if os.path.exists("highscore.json"):

                        try:
                            with open("highscore.json", "r") as file:
                                data = json.load(file)
                                highscore = data["highscore"]

                        except:
                            highscore = 0
                break
    # --- камера ---
    camera_x = player.x - WIDTH // 2
    camera_y = player.y - HEIGHT // 2

    # --- отрисовка ---
    screen.fill((2, 2, 3))
    if game_state == GAME_OVER:
        game_over_text = font.render(
            "GAME OVER",
            True,
            (255, 80, 80)
        )

        score_text = font.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            (180, 180, 180)
        )

        screen.blit(game_over_text, (280, 220))
        screen.blit(score_text, (320, 280))
        screen.blit(restart_text, (230, 340))

        pygame.display.flip()
        continue
    if game_state == MENU:
        title = font.render(
            "Magic Survival Clone",
            True,
            (255, 255, 255)
        )

        start_text = font.render(
            "Press SPACE to start",
            True,
            (180, 180, 180)
        )

        screen.blit(title, (250, 250))
        screen.blit(start_text, (260, 320))

        pygame.display.flip()
        continue
    start_x = int(camera_x // tile_size) * tile_size
    start_y = int(camera_y // tile_size) * tile_size

    for x in range(start_x, start_x + WIDTH + tile_size, tile_size):
        for y in range(start_y, start_y + HEIGHT + tile_size, tile_size):
            screen.blit(bg, (x - camera_x, y - camera_y))
    pygame.draw.rect(screen, (60, 60, 60), (20, 20, 81, 20))
    pygame.draw.rect(
        screen,
        (80, 220, 100),
        (20, 20, int(200 * (player.hp / player.max_hp)), 20)
    )
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    highscore_text = font.render(
        f"Highscore: {highscore}",
        True,
        (255, 255, 100)
    )

    screen.blit(highscore_text, (20, 80))
    screen.blit(score_text, (20, 50))
    # игрок (в центре)
    for enemy in enemies:
        enemy.draw(screen, camera_x, camera_y)
    for bullet in bullets:
        bullet.draw(screen, camera_x, camera_y)
    player.draw(screen)
    if player.hp <= 0:

        if score > highscore:

            highscore = score

            try:
                with open("highscore.json", "w") as file:

                    json.dump(
                        {"highscore": highscore},
                        file
                    )

                print("highscore saved")

            except Exception as e:
                print("save error:", e)

        game_state = GAME_OVER
    pygame.display.set_caption(f"FPS: {int(clock.get_fps())}")
    pygame.display.flip()

# --- выход ---
pygame.quit()
sys.exit()