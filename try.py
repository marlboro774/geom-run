import pygame
import sys
import random
import pytmx

pygame.init()

WIDTH, HEIGHT = 800, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Run")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 50)
GREEN = (50, 255, 50)

FPS = 60
clock = pygame.time.Clock()

PLAYER_SIZE = 30
PLAYER_SPEED_X = 5  # Скорость движения игрока вправо
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

tmx_data = pytmx.load_pygame("level1.tmx")
TILE_SIZE = tmx_data.tilewidth


class GameProcess:
    def __init__(self):
        self.player_x = WIDTH // 3
        self.player_y = HEIGHT - PLAYER_SIZE - 10
        self.player_speed_x = PLAYER_SPEED_X
        self.player_speed_y = 0
        self.player_jump = -20
        self.gravity = 1
        self.player_on_ground = True

        self.obstacles = []
        self.bonuses = []
        self.obstacle_speed = 5

        self.obstacle_spawn_timer = 0
        self.bonus_spawn_timer = 0

        self.score = 0

        self.camera_x = 0

    def reset_game(self):
        self.__init__()

    def draw_map(self, surface):
        for layer in tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x * TILE_SIZE - self.camera_x, y * TILE_SIZE))

    def main(self):
        pygame.mixer.music.load(game_music)
        pygame.mixer.music.play(-1)

        running = True
        while running:
            screen.fill(WHITE)

            self.draw_map(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] and self.player_on_ground:
                self.player_speed_y = self.player_jump
                self.player_on_ground = False

            self.camera_x += self.player_speed_x

            self.player_speed_y += self.gravity
            self.player_y += self.player_speed_y

            if self.player_y >= HEIGHT - PLAYER_SIZE:
                self.player_y = HEIGHT - PLAYER_SIZE
                self.player_speed_y = 0
                self.player_on_ground = True

            pygame.draw.rect(screen, BLUE, (self.player_x, self.player_y, PLAYER_SIZE, PLAYER_SIZE))

            # Отрисовка счета
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
