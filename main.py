import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Geometry Run")
background_image = pygame.image.load('images/bg.png')


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

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()



class Player(pygame.sprite.Sprite):
    image = pygame.image.load('images/player.png')
    image1 = pygame.transform.scale(image, (70, 70))

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Player.image1
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.gravity = 0.2
        self.onGround = True
        self.died = False
        self.win = False
        self.rect = self.image.get_rect(center=pos)
        self.jump_amount = 10
        self.particles = []
        self.isjump = False
        self.player_x = 100
        self.player_y = HEIGHT - PLAYER_SIZE - 10
        self.player_speed_y = 20

    def jump(self):
        self.player_speed_y = self.jump_amount = 10
        self.onGround = False

    def update(self, event=None):
        if event and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.onGround:
            self.jump()
            print(event)
        elif event is None:
            self.player_speed_y += self.gravity
            self.rect.y += self.player_speed_y











class Bonus(pygame.sprite.Sprite):
    image = pygame.image.load('images/bonus.png')

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = Bonus.image
        self.rect = self.image.get_rect(topleft=pos)
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

class Obstacle(pygame.sprite.Sprite):
    image = pygame.image.load('images/spike.png')

    def __init__(self, pos):
        super().__init__(obstacles)
        self.image = Obstacle.image
        self.rect = self.image.get_rect(topleft=pos)
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, player):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, player):
            self.rect = self.rect.move(0, 1)
            death_sound.play()
            running = False





class GameProcess:
    def __init__(self):
        self.player = Player((150, 150))

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
            screen.blit(background_image, (0, 0))
            all_sprites.draw(screen)
            obstacles.draw(screen)

            self.background_x -= self.background_speed
            if self.background_x <= -WIDTH:
                self.background_x = 0
            pygame.draw.rect(screen, GREEN, (self.background_x, HEIGHT - 50, WIDTH, 50))
            pygame.draw.rect(screen, GREEN, (self.background_x + WIDTH, HEIGHT - 50, WIDTH, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                all_sprites.update(event)
            all_sprites.update()
            # if self.player.player_y >= HEIGHT - PLAYER_SIZE - 10:
            #     self.player.player_y = HEIGHT - PLAYER_SIZE - 10
            #     self.player.player_speed_y = 0
            #     self.player.onGround = True

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

            for obstacle in self.obstacles:
                obstacles.update(self.player)

            # for bonus in self.bonuses[:]:
            #     if player_rect.colliderect(bonus):
            #         bonus_sound.play()
            #         self.bonuses.remove(bonus)
            #         self.score += BONUS_SCORE

            if self.score % 500 == 0:
                self.obstacle_speed += 0.1

            self.score += 1

            for obstacle in self.obstacles:
                obstacle_image = pygame.image.load('images/spike.png')
                screen.blit(obstacle_image, (obstacle.x, obstacle.y))

            for bonus in self.bonuses:
                bonus_image = pygame.image.load('images/bonus.png') # БОНУСЫ
                bonus_image_resized = pygame.transform.scale(bonus_image, (40, 40))
                screen.blit(bonus_image_resized, bonus.topleft)

            score_text = font.render(f"Score: {self.score // 10}", True, BLACK)
            screen.blit(score_text, (10, 10))

            pygame.display.flip()
            clock.tick(FPS)

        self.game_over()

    def game_over(self):
        pygame.mixer.music.stop()
        screen.blit(background_image, (0, 0))
        game_over_text = font.render("Game Over!", True, WHITE)
        score_text = font.render(f"Final Score: {self.score // 10}", True, WHITE)
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
        screen.blit(background_image, (0, 0))

        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("Geometry Run", True, WHITE)
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
            self.customize_button_center[0] - 12,
            self.customize_button_center[1] - 12,
            25, 25
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
