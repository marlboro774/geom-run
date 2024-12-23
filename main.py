import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Run")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 50)

FPS = 60
clock = pygame.time.Clock()

PLAYER_SIZE = 30
player_x = 100
player_y = HEIGHT - PLAYER_SIZE - 10
player_speed_y = 0
player_jump = -15
gravity = 1
player_on_ground = True

OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 50
obstacles = []
global obstacle_speed
obstacle_speed = 5
obstacle_spawn_timer = 0
SPAWN_DELAY = 1500

background_speed = 2
background_x = 0

BONUS_SIZE = 20
bonuses = []
BONUS_SPAWN_DELAY = 2000
bonus_spawn_timer = 0
bonus_score = 100

score = 0
font = pygame.font.Font(None, 36)

pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)


def main():
    global player_x, player_y, player_speed_y, player_on_ground, obstacle_spawn_timer, bonus_spawn_timer, score, obstacles, bonuses, background_x, obstacle_speed

    running = True
    while running:
        screen.fill(WHITE)

        background_x -= background_speed
        if background_x <= -WIDTH:
            background_x = 0
        pygame.draw.rect(screen, GREEN, (background_x, HEIGHT - 50, WIDTH, 50))
        pygame.draw.rect(screen, GREEN, (background_x + WIDTH, HEIGHT - 50, WIDTH, 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and player_on_ground:
            player_speed_y = player_jump
            player_on_ground = False

        player_speed_y += gravity
        player_y += player_speed_y

        if player_y >= HEIGHT - PLAYER_SIZE - 10:
            player_y = HEIGHT - PLAYER_SIZE - 10
            player_speed_y = 0
            player_on_ground = True

        obstacle_spawn_timer += clock.get_time()
        if obstacle_spawn_timer > SPAWN_DELAY:
            obstacle_spawn_timer = 0
            obstacles.append(pygame.Rect(WIDTH, HEIGHT - OBSTACLE_HEIGHT - 10, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

        for obstacle in obstacles:
            obstacle.x -= obstacle_speed

        obstacles = [obstacle for obstacle in obstacles if obstacle.x + OBSTACLE_WIDTH > 0]

        bonus_spawn_timer += clock.get_time()
        if bonus_spawn_timer > BONUS_SPAWN_DELAY:
            bonus_spawn_timer = 0
            bonuses.append(pygame.Rect(random.randint(WIDTH, WIDTH + 200), random.randint(50, HEIGHT - 100), BONUS_SIZE,
                                       BONUS_SIZE))

        for bonus in bonuses:
            bonus.x -= obstacle_speed

        bonuses = [bonus for bonus in bonuses if bonus.x + BONUS_SIZE > 0]

        player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                running = False

        for bonus in bonuses[:]:
            if player_rect.colliderect(bonus):
                bonuses.remove(bonus)
                score += bonus_score

        if score % 500 == 0:
            obstacle_speed += 0.1

        score += 1

        pygame.draw.rect(screen, BLUE, player_rect)

        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)

        for bonus in bonuses:
            pygame.draw.rect(screen, YELLOW, bonus)

        score_text = font.render(f"Score: {score // 10}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    game_over()


def game_over():
    screen.fill(WHITE)
    game_over_text = font.render("Game Over!", True, BLACK)
    score_text = font.render(f"Final Score: {score // 10}", True, BLACK)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
