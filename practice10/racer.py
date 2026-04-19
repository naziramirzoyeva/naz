import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

# настройка экрана
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)

# colors
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (255, 0, 0)

# фон
background = pygame.image.load("practice10/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# sound
pygame.mixer.music.load("practice10/background.wav")
pygame.mixer.music.play(-1)

crash_sound = pygame.mixer.Sound("practice10/crash.wav")


# player основной
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("practice10/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


# enemy 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("practice10/enemy.png")
        self.rect = self.image.get_rect()
        self.reset()

    def move(self):
        self.rect.move_ip(0, 6)

        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, WIDTH - 40), 0)


# coin
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("practice10/coin.png")
        self.image = pygame.transform.scale(self.image, (30, 30))  # уменьшили монетку
        self.rect = self.image.get_rect()
        self.reset()

    def move(self):
        self.rect.move_ip(0, 5)

        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, WIDTH - 40), 0)


# objects
player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

all_sprites.add(player, enemy, coin)
enemies.add(enemy)
coins.add(coin)

coin_count = 0
game_over = False


# gameloop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        player.move()
        enemy.move()
        coin.move()

        # collision with enemy
        if pygame.sprite.spritecollideany(player, enemies):
            crash_sound.play()
            game_over = True

        # collision with coin
        hits = pygame.sprite.spritecollide(player, coins, False)
        for c in hits:
            coin_count += 1
            c.reset()

    # рисуем фон
    screen.blit(background, (0, 0))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # score
    text = font.render(f"Coins: {coin_count}", True, YELLOW)
    screen.blit(text, (250, 10))

    if game_over:
        over = font.render("GAME OVER", True, RED)
        screen.blit(over, (120, 280))

    pygame.display.update()
    clock.tick(60)