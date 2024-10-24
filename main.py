import sys, pygame
from random import randint
from pygame.time import get_ticks

pygame.init()

# Definição de constantes
PLAYER_DELAY = 100
SPEED = 15
ENEMY_SPEED = 10
SHOT_INTERVAL = 500
BALA_WIDTH = 10
BALA_HEIGHT = 10
PLAYER_WIDTH = 110
PLAYER_HEIGHT = 110
INIMIGO_WIDTH = 80
INIMIGO_HEIGHT = 80

class Bala:
    def __init__(self, rect, speed, damage):
        self.rect = rect
        self.speed = speed
        self.damage = damage

class Inimigo:
    def __init__(self, rect, speed):
        self.rect = rect
        self.speed = speed
        self.direction = 1
        self.last_shot = get_ticks()

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= width:
            self.direction *= -1

    def shoot(self):
        current_time = get_ticks()
        if current_time - self.last_shot > SHOT_INTERVAL:
            self.last_shot = current_time
            return Bala(pygame.Rect(self.rect.centerx, self.rect.bottom, BALA_WIDTH, BALA_HEIGHT), [0, 10], 10)
        return None

# Inicializar a tela
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
limite_altura = height * 0.8

# Configurar player
rect = pygame.Rect(width - 1000, height - 150, PLAYER_WIDTH, PLAYER_HEIGHT)
player_delay = [PLAYER_DELAY, 0]

# Carregar imagens e sons
pygame.mixer.music.load('sons/musicafundo.mp3')
pygame.mixer.music.play(-1)

fundo = pygame.image.load("Imagens/fundo.jpg")
fundo = pygame.transform.scale(fundo, (width, height))
player = pygame.image.load("Imagens/player.png")
inimigo_img = pygame.image.load("Imagens/inimigo.png")
bala_img = pygame.image.load("Imagens/bala.png")

# Listas para armazenar balas e inimigos
Balas = []
Inimigos = []
Balas_inimigos = []

# Criar inimigos
for i in range(10):
    inimigo = Inimigo(pygame.Rect(randint(0, width - INIMIGO_WIDTH), randint(50, 200), INIMIGO_WIDTH, INIMIGO_HEIGHT), ENEMY_SPEED)
    Inimigos.append(inimigo)

clock = pygame.time.Clock()

# Loop principal do jogo
while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    # Movimentação do player
    if keys[pygame.K_RIGHT] and rect.right + SPEED <= width:
        rect.x += SPEED
    if keys[pygame.K_LEFT] and rect.left - SPEED >= 0:
        rect.x -= SPEED
    if keys[pygame.K_UP] and rect.top - SPEED >= limite_altura:
        rect.y -= SPEED
    if keys[pygame.K_DOWN] and rect.bottom + SPEED <= height:
        rect.y += SPEED

    # Disparo de balas com a tecla ESPAÇO
    if keys[pygame.K_SPACE] and player_delay[1] <= 0:
        bala = Bala(pygame.Rect(rect.centerx, rect.centery, BALA_WIDTH, BALA_HEIGHT), [0, -10], 0)
        Balas.append(bala)
        player_delay[1] = PLAYER_DELAY
    elif player_delay[1] > 0:
        player_delay[1] -= 1

    # Desenhar o fundo e o player
    screen.blit(fundo, (0, 0))
    screen.blit(player, rect)

    # Movimentar e desenhar balas
    for bala in Balas[:]:
        bala.rect.y += bala.speed[1]
        screen.blit(bala_img, bala.rect)
        if bala.rect.bottom < 0:
            Balas.remove(bala)

        # Verificar colisão de balas com inimigos
        idInimigo = bala.rect.collidelist([inimigo.rect for inimigo in Inimigos])
        if idInimigo != -1:
            Inimigos.pop(idInimigo)
            Balas.remove(bala)

    # Movimentar inimigos e verificar tiros
    for inimigo in Inimigos:
        inimigo.move()
        screen.blit(inimigo_img, inimigo.rect)
        nova_bala_inimigo = inimigo.shoot()
        if nova_bala_inimigo:
            Balas_inimigos.append(nova_bala_inimigo)

    # Movimentar e desenhar balas dos inimigos
    for bala_inimigo in Balas_inimigos[:]:
        bala_inimigo.rect.y += bala_inimigo.speed[1]
        screen.blit(bala_img, bala_inimigo.rect)
        if bala_inimigo.rect.top > height:
            Balas_inimigos.remove(bala_inimigo)
        if bala_inimigo.rect.colliderect(rect):
            sys.exit()  # Finaliza o jogo em caso de colisão

    pygame.display.flip()
    clock.tick(60)
