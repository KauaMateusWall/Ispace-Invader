import pygame
import sys
from random import randint

# Inicializar Pygame
pygame.init()

# Definir constantes
WIDTH, HEIGHT = 800, 600
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_STRENGTH = 10
ENEMY_SPEED = 2
SCROLL_THRESHOLD = 200  # Ponto a partir do qual o jogador "puxa" a tela

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Definir a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Clone")

# Definir o clock
clock = pygame.time.Clock()

# Classe do jogador (Mario)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))  # Representando Mario como um retângulo
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 150
        self.velocity_y = 0
        self.jumping = False
        self.world_shift = 0  # Para o deslocamento da tela

    def update(self):
        keys = pygame.key.get_pressed()

        # Movimentação horizontal
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Pulo
        if keys[pygame.K_SPACE] and not self.jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.jumping = True

        # Aplicar gravidade
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Colisão com o chão
        if self.rect.bottom >= HEIGHT - 100:
            self.rect.bottom = HEIGHT - 100
            self.jumping = False
            self.velocity_y = 0

        # Controle de rolagem da tela
        if self.rect.right > WIDTH - SCROLL_THRESHOLD:
            self.world_shift = PLAYER_SPEED
            self.rect.right = WIDTH - SCROLL_THRESHOLD
        elif self.rect.left < SCROLL_THRESHOLD:
            self.world_shift = -PLAYER_SPEED
            self.rect.left = SCROLL_THRESHOLD
        else:
            self.world_shift = 0

# Classe para inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))  # Inimigo é representado como um quadrado vermelho
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1

    def update(self):
        self.rect.x += self.direction * ENEMY_SPEED
        # Mudar direção ao bater nas bordas do movimento
        if self.rect.left <= 0 or self.rect.right >= WIDTH * 2:  # Fase maior
            self.direction *= -1

# Classe para plataformas
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Grupos de sprites
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Criar jogador (Mario)
player = Player()
all_sprites.add(player)

# Criar chão e plataformas
ground = Platform(0, HEIGHT - 100, WIDTH * 2, 100)  # Chão para fase maior
all_sprites.add(ground)
platforms.add(ground)

# Adicionar plataformas
platform1 = Platform(300, HEIGHT - 250, 150, 20)
all_sprites.add(platform1)
platforms.add(platform1)

platform2 = Platform(600, HEIGHT - 350, 150, 20)
all_sprites.add(platform2)
platforms.add(platform2)

# Adicionar inimigos
for i in range(5):
    enemy = Enemy(randint(400, 1500), HEIGHT - 140)  # Inimigos em posições aleatórias
    all_sprites.add(enemy)
    enemies.add(enemy)

# Loop principal do jogo
running = True
while running:
    clock.tick(60)

    # Checar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualizar sprites
    all_sprites.update()

    # Verificar colisões do jogador com plataformas
    hits = pygame.sprite.spritecollide(player, platforms, False)
    if hits:
        player.rect.y = hits[0].rect.top - player.rect.height
        player.jumping = False
        player.velocity_y = 0

    # Verificar colisões do jogador com inimigos
    if pygame.sprite.spritecollide(player, enemies, False):
        print("Você foi atingido por um inimigo!")
        running = False  # Encerra o jogo

    # Rolagem da tela
    for platform in platforms:
        platform.rect.x -= player.world_shift

    for enemy in enemies:
        enemy.rect.x -= player.world_shift

    # Desenhar tudo
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Atualizar a tela
    pygame.display.flip()

pygame.quit()
sys.exit()
