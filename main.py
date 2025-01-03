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
OBSTACLE_WIDTH = 30
OBSTACLE_HEIGHT = 50
BONUS_SIZE = 20
SPAWN_DELAY = 1500
BONUS_SPAWN_DELAY = 2000
BONUS_SCORE = 100
font = pygame.font.Font(None, 36)

pygame.mixer.init()
menu_music = "menu_music.mp3"
game_music = "background_music.mp3"
pygame.mixer.music.load(menu_music)
pygame.mixer.music.play(-1)

death_sound = pygame.mixer.Sound("death_sound.mp3")
bonus_sound = pygame.mixer.Sound("bonus_sound.mp3")


class GameProcess:
    def __init__(self):
        self.player_x = 100
        self.player_y = HEIGHT - PLAYER_SIZE - 10
        self.player_speed_y = 0
        self.player_jump = -10
        self.gravity = 1
        self.player_on_ground = True

        self.obstacles = []
        self.bonuses = []
        self.obstacle_speed = 5

        self.obstacle_spawn_timer = 0
        self.bonus_spawn_timer = 0

        self.background_x = 0
        self.background_speed = 2

        self.score = 0

    def reset_game(self):
        self.__init__()

    def main(self):
        pygame.mixer.music.load(game_music)
        pygame.mixer.music.play(-1)

        running = True
        while running:
            screen.fill(WHITE)

            self.background_x -= self.background_speed
            if self.background_x <= -WIDTH:
                self.background_x = 0
            pygame.draw.rect(screen, GREEN, (self.background_x, HEIGHT - 50, WIDTH, 50))
            pygame.draw.rect(screen, GREEN, (self.background_x + WIDTH, HEIGHT - 50, WIDTH, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.player_on_ground:
                self.player_speed_y = self.player_jump
                self.player_on_ground = False

            self.player_speed_y += self.gravity
            self.player_y += self.player_speed_y

            if self.player_y >= HEIGHT - PLAYER_SIZE - 10:
                self.player_y = HEIGHT - PLAYER_SIZE - 10
                self.player_speed_y = 0
                self.player_on_ground = True

            self.obstacle_spawn_timer += clock.get_time()
            if self.obstacle_spawn_timer > SPAWN_DELAY:
                self.obstacle_spawn_timer = 0
                self.obstacles.append(
                    pygame.Rect(WIDTH, HEIGHT - OBSTACLE_HEIGHT - 10, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

            for obstacle in self.obstacles:
                obstacle.x -= self.obstacle_speed

            self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.x + OBSTACLE_WIDTH > 0]

            self.bonus_spawn_timer += clock.get_time()
            if self.bonus_spawn_timer > BONUS_SPAWN_DELAY:
                self.bonus_spawn_timer = 0
                self.bonuses.append(
                    pygame.Rect(random.randint(WIDTH, WIDTH + 200), random.randint(50, HEIGHT - 100), BONUS_SIZE,
                                BONUS_SIZE))

            for bonus in self.bonuses:
                bonus.x -= self.obstacle_speed

            self.bonuses = [bonus for bonus in self.bonuses if bonus.x + BONUS_SIZE > 0]

            player_rect = pygame.Rect(self.player_x, self.player_y, PLAYER_SIZE, PLAYER_SIZE)
            for obstacle in self.obstacles:
                if player_rect.colliderect(obstacle):
                    death_sound.play()
                    running = False

            for bonus in self.bonuses[:]:
                if player_rect.colliderect(bonus):
                    bonus_sound.play()
                    self.bonuses.remove(bonus)
                    self.score += BONUS_SCORE

            if self.score % 500 == 0:
                self.obstacle_speed += 0.1

            self.score += 1

            pygame.draw.rect(screen, BLUE, player_rect)

            for obstacle in self.obstacles:
                # Отрисовка препятствия как треугольника
                pygame.draw.polygon(screen, RED, [
                    (obstacle.x, obstacle.y + OBSTACLE_HEIGHT),
                    (obstacle.x + OBSTACLE_WIDTH // 2, obstacle.y),
                    (obstacle.x + OBSTACLE_WIDTH, obstacle.y + OBSTACLE_HEIGHT)
                ])

            for bonus in self.bonuses:
                pygame.draw.rect(screen, YELLOW, bonus)

            score_text = font.render(f"Score: {self.score // 10}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

        self.game_over()

    def game_over(self):
        pygame.mixer.music.stop()
        screen.fill(WHITE)
        game_over_text = font.render("Game Over!", True, BLACK)
        score_text = font.render(f"Final Score: {self.score // 10}", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))

        button_center = (WIDTH // 2, HEIGHT // 2 + 50)
        button_radius = 30
        pygame.draw.circle(screen, GREEN, button_center, button_radius)
        button_text = font.render("R", True, BLACK)
        screen.blit(button_text,
                    (button_center[0] - button_text.get_width() // 2, button_center[1] - button_text.get_height() // 2))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if (mouse_x - button_center[0]) ** 2 + (mouse_y - button_center[1]) ** 2 <= button_radius ** 2:
                        waiting = False

        self.reset_game()
        pygame.mixer.music.load(game_music)
        pygame.mixer.music.play(-1)
        self.main()


class MainMenu:
    def __init__(self):
        self.play_button_center = (WIDTH // 2, HEIGHT // 2)
        self.play_button_radius = 50
        self.customize_button_center = (WIDTH // 2 - 100, HEIGHT // 2)
        self.customize_button_radius = 30

    def draw(self):
        screen.fill(WHITE)

        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Geometry Run", True, BLACK)
        screen.blit(title_text, (
            WIDTH // 2 - title_text.get_width() // 2,
            HEIGHT // 4 - title_text.get_height() // 2
        ))

        pygame.draw.circle(screen, GREEN, self.play_button_center, self.play_button_radius)
        pygame.draw.polygon(screen, BLACK, [
            (self.play_button_center[0] - 10, self.play_button_center[1] - 15),
            (self.play_button_center[0] - 10, self.play_button_center[1] + 15),
            (self.play_button_center[0] + 15, self.play_button_center[1])
        ])

        pygame.draw.circle(screen, BLUE, self.customize_button_center, self.customize_button_radius)
        pygame.draw.rect(screen, YELLOW, (
            self.customize_button_center[0] - 10,
            self.customize_button_center[1] - 10,
            20, 20
        ))
        smile = font.render(":)", True, BLACK)
        screen.blit(smile, (
            self.customize_button_center[0] - smile.get_width() // 2,
            self.customize_button_center[1] - smile.get_height() // 2
        ))

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (mouse_x - self.play_button_center[0]) ** 2 + (
                        mouse_y - self.play_button_center[1]) ** 2 <= self.play_button_radius ** 2:
                    return "play"
                if (mouse_x - self.customize_button_center[0]) ** 2 + (
                        mouse_y - self.customize_button_center[1]) ** 2 <= self.customize_button_radius ** 2:
                    return "customize"
        return None


if __name__ == "__main__":
    menu = MainMenu()
    game_process = GameProcess()
    while True:
        menu.draw()
        action = menu.handle_events()
        if action == "play":
            pygame.mixer.music.load(game_music)
            pygame.mixer.music.play(-1)
            game_process.reset_game()
            game_process.main()
        elif action == "customize":
            print("Ещё не готово.")
