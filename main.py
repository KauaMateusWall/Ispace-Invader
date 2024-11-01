import sys
import pygame
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
INIMIGO_VIDA = 100
INIMIGO2_VIDA = 100
DANO_BALA = 100
DANO_BALA_INIMIGO = 50
player_vida = 300  # Vida inicial do jogador

class Bala:
    def __init__(self, rect, speed, damage):
        self.rect = rect
        self.speed = speed
        self.damage = damage

class Inimigo:
    def __init__(self, rect, speed, vida, use_bala2=False):
        self.rect = rect
        self.speed = speed
        self.direction = 1
        self.last_shot = get_ticks()
        self.vida = vida
        self.use_bala2 = use_bala2  # Flag para identificar bala2

    def move(self):
        # Movimento horizontal com limitação de bordas
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= width:
            self.direction *= -1
            self.rect.y += 20  # Adiciona movimento vertical ao colidir com as bordas
            if self.rect.y >= limite_altura:
                self.rect.y = limite_altura  # Limita a altura máxima

    def shoot(self):
        current_time = get_ticks()
        if current_time - self.last_shot > SHOT_INTERVAL:
            self.last_shot = current_time
            speed = [0, 10]
            return Bala(pygame.Rect(self.rect.centerx, self.rect.bottom, BALA_WIDTH, BALA_HEIGHT), speed, DANO_BALA_INIMIGO)
        return None

# Inicializar a tela
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()
limite_altura = height * 0.8

# Configurar player
rect = pygame.Rect(width // 2 - PLAYER_WIDTH // 2, height - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
player_delay = [PLAYER_DELAY, 0]

# Carregar imagens e sons
pygame.mixer.music.load(r'sons\musicaFundo.mp3')
pygame.mixer.music.play(-1)

fundo = pygame.image.load(r'imagens\fundo.jpg')
fundo = pygame.transform.scale(fundo, (width, height))
player = pygame.image.load(r"imagens\player.png")
inimigo_img = pygame.image.load(r"imagens\inimigo.png")
bala_img = pygame.image.load(r"imagens\bala.png")
bala2_img = pygame.image.load(r"imagens\bala2.png")
inimigo2_img = pygame.image.load(r"imagens\inimigo2.png")

# Listas para armazenar balas e inimigos
Balas = []
Inimigos = []
Inimigos2 = []
Balas_inimigos = []
Balas_inimigos2 = []

# Criar inimigos com vida
for i in range(6):
    inimigo = Inimigo(pygame.Rect(randint(0, width - INIMIGO_WIDTH), randint(50, 200), INIMIGO_WIDTH, INIMIGO_HEIGHT), ENEMY_SPEED, INIMIGO_VIDA)
    Inimigos.append(inimigo)

clock = pygame.time.Clock()

# Função para desenhar o HUD na tela
def desenhar_hud(screen, vida, pontos):
    font = pygame.font.SysFont(None, 36)
    vida_text = font.render(f'Vida: {vida}', True, (255, 255, 255))
    pontos_text = font.render(f'Pontos: {pontos}', True, (255, 255, 255))
    screen.blit(vida_text, (10, 10))
    screen.blit(pontos_text, (10, 50))

# Função para atualizar e desenhar balas
def atualizar_e_desenhar_balas(balas, screen, bala_img, velocidade_y, jogador=None):
    for bala in balas[:]:
        bala.rect.y += velocidade_y
        screen.blit(bala_img, bala.rect)
        if bala.rect.top > height or bala.rect.bottom < 0:
            balas.remove(bala)
        elif jogador and bala.rect.colliderect(jogador):
            global player_vida
            player_vida -= bala.damage
            balas.remove(bala)
            if player_vida <= 0:
                sys.exit()

# Variável para armazenar a pontuação
pontos = 0

# Variável para controlar o spawn de inimigos2
tempo_ultimo_spawn_inimigo2 = get_ticks()
INTERVALO_SPAWN_INIMIGO2 = 2000  # intervalo de 2 segundos entre spawn de novos inimigos2

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
        bala = Bala(pygame.Rect(rect.centerx, rect.centery, BALA_WIDTH, BALA_HEIGHT), [0, -10], DANO_BALA)
        Balas.append(bala)
        player_delay[1] = PLAYER_DELAY
    elif player_delay[1] > 0:
        player_delay[1] -= 1

    # Desenhar o fundo e o player
    screen.blit(fundo, (0, 0))
    screen.blit(player, rect)

    # Atualizar balas do jogador
    atualizar_e_desenhar_balas(Balas, screen, bala_img, -10)

    # Verificar colisão de balas com inimigos
    for bala in Balas[:]:
        # Colisão com inimigos tipo 1
        idInimigo = bala.rect.collidelist([inimigo.rect for inimigo in Inimigos])
        if idInimigo != -1:
            inimigo = Inimigos[idInimigo]
            inimigo.vida -= DANO_BALA
            if inimigo.vida <= 0:
                Inimigos.pop(idInimigo)
                pontos += 10
            Balas.remove(bala)

        # Colisão com inimigos tipo 2
        idInimigo2 = bala.rect.collidelist([inimigo2.rect for inimigo2 in Inimigos2])
        if idInimigo2 != -1:
            inimigo2 = Inimigos2[idInimigo2]
            inimigo2.vida -= DANO_BALA
            if inimigo2.vida <= 0:
                Inimigos2.pop(idInimigo2)
                pontos += 15
            Balas.remove(bala)

    # Movimentar inimigos e verificar tiros
    for inimigo in Inimigos:
        inimigo.move()
        screen.blit(inimigo_img, inimigo.rect)
        nova_bala_inimigo = inimigo.shoot()
        if nova_bala_inimigo:
            Balas_inimigos.append(nova_bala_inimigo)

    # Adicionar inimigos2 somente quando restarem 5 ou menos inimigos do tipo 1
    if len(Inimigos) <= 5 and len(Inimigos2) < 5:
        if get_ticks() - tempo_ultimo_spawn_inimigo2 > INTERVALO_SPAWN_INIMIGO2:
            novo_inimigo2 = Inimigo(
                pygame.Rect(randint(0, width - INIMIGO_WIDTH), randint(50, 200), INIMIGO_WIDTH, INIMIGO_HEIGHT),
                20,
                INIMIGO2_VIDA
            )
            Inimigos2.append(novo_inimigo2)
            tempo_ultimo_spawn_inimigo2 = get_ticks()

    for inimigo in Inimigos2:
        inimigo.move()
        screen.blit(inimigo2_img, inimigo.rect)
        nova_bala_inimigo2 = inimigo.shoot()
        if nova_bala_inimigo2:
            Balas_inimigos2.append(nova_bala_inimigo2)

    # Atualizar balas de inimigos tipo 1 e verificar colisão com o jogador
    atualizar_e_desenhar_balas(Balas_inimigos, screen, bala_img, 10, jogador=rect)

    # Atualizar balas de inimigos tipo 2 e verificar colisão com o jogador
    atualizar_e_desenhar_balas(Balas_inimigos2, screen, bala2_img, 10, jogador=rect)

    # Atualizar HUD
    desenhar_hud(screen, player_vida, pontos)

    pygame.display.flip()
    clock.tick(60)
