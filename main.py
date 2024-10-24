import sys, pygame
from random import randint
from pygame.time import get_ticks  # Importando corretamente o método get_ticks

pygame.init()

player_delay = [100, 0]
speed = 15
enemy_speed = 10
shot_interval = 500


class Bala:
    rect: pygame.Rect
    speed: [int, int]
    damage: [int]

    def __init__(self, rect, speed, damage):
        self.rect = rect
        self.speed = speed
        self.damage = damage


class Inimigo:
    def __init__(self, rect, speed):
        self.rect = rect
        self.speed = speed
        self.direction = 1  # Direção inicial (1 = direita, -1 = esquerda)
        self.last_shot = get_ticks()  # Registrar o tempo do último tiro

    def move(self):
        # Movimentar o inimigo de um lado para o outro
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= width:
            self.direction *= -1  # Inverter a direção ao atingir a borda da tela

    def shoot(self):
        # Verificar o tempo e disparar se o intervalo tiver passado
        current_time = get_ticks()
        if current_time - self.last_shot > shot_interval:
            self.last_shot = current_time
            # Criar uma bala saindo do centro inferior do inimigo
            return Bala(pygame.Rect(self.rect.centerx, self.rect.bottom, 10, 10), [0, 10], 10)
        return None


# Definir a tela em modo fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Obter a largura e altura da tela
width, height = screen.get_size()

# Definir a posição inicial do player na parte inferior da tela
rect = pygame.rect.Rect(width - 1000, height - 150, 110, 110)

# Definir a altura máxima que o player pode se mover (40% da tela)
limite_altura = height * 0.8

clock = pygame.time.Clock()

# Carregar a música de fundo
pygame.mixer.music.load(r'C:\Users\05341106067\Downloads\musicaFundo.mp3')

# Reproduzir a música indefinidamente (-1 faz com que a música toque em loop)
pygame.mixer.music.play(-1)

# Carregar e redimensionar a imagem de fundo
fundo = pygame.image.load(r'C:\Users\05341106067\Downloads\FUNDO2.jpg')
fundo = pygame.transform.scale(fundo, (width, height))

player = pygame.image.load(r"C:\Users\05341106067\Downloads\player2.png")

inimigo_img = pygame.image.load(r"C:\Users\05341106067\Downloads\inimigo.png")

bala_img = pygame.image.load(r"C:\Users\05341106067\Downloads\bala2.png")

# Lista para armazenar balas disparadas
Balas = []

Inimigos = []
Balas_inimigos = []

for i in range(10):
    inimigo = Inimigo(pygame.Rect(randint(0, width - 100), randint(50, 200), 80, 80), enemy_speed)
    Inimigos.append(inimigo)

while True:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    # Movimentação horizontal
    if keys[pygame.K_RIGHT] and rect.right + speed <= width:
        rect.x += speed
    if keys[pygame.K_LEFT] and rect.left - speed >= 0:
        rect.x -= speed

    # Movimentação vertical com limite de 40% da altura
    if keys[pygame.K_UP] and rect.top - speed >= limite_altura:
        rect.y -= speed
    if keys[pygame.K_DOWN] and rect.bottom + speed <= height:
        rect.y += speed

    # Disparo de balas com a tecla ESPAÇO
    if keys[pygame.K_SPACE] and player_delay[1] <= 0:
        bala = Bala(pygame.Rect(rect.centerx, rect.centery, 50, 50), [0, -10], 0)
        Balas.append(bala)
        player_delay[1] = player_delay[0]
    elif player_delay[1] > 0:
        player_delay[1] -= 1

    # Desenhar o fundo e o player na tela
    screen.blit(fundo, (0, 0))
    screen.blit(player, rect)

    for bala in Balas[:]:
        bala.rect.y += bala.speed[1]  # Movimentar a bala verticalmente
        screen.blit(bala_img, bala.rect)  # Desenhar a bala usando a imagem

        # Remover a bala se ela sair da tela
        if bala.rect.bottom < 0:
            Balas.remove(bala)

        # Verificar colisões entre balas do jogador e inimigos
        for bala in Balas:
            bala.rect.y += bala.speed[1]  # Movimentar a bala verticalmente
            screen.blit(bala_img, bala.rect)  # Desenhar a bala usando a imagem
            idInimigo = bala.rect.collidelist(Inimigos)
            if idInimigo != -1:  # Colisão detectada
                Inimigos.pop(idInimigo)  # Remover o inimigo
                Balas.remove(bala)  # Remover a "bala

    for inimigo in Inimigos:
        inimigo.move()  # Movimentar o inimigo
        screen.blit(inimigo_img, inimigo.rect)  # Usando a imagem do player temporariamente como inimigo

        # Verificar se o inimigo deve atirar
        nova_bala_inimigo = inimigo.shoot()
        if nova_bala_inimigo:
            Balas_inimigos.append(nova_bala_inimigo)

        # Atualizar e desenhar balas dos inimigos
    for bala_inimigo in Balas_inimigos[:]:
        bala_inimigo.rect.y += bala_inimigo.speed[1]  # Movimentar a bala para baixo
        pygame.draw.rect(screen, (255, 0, 0), bala_inimigo.rect)  # Desenhar a bala dos inimigos
        if bala_inimigo.rect.top > height:
            Balas_inimigos.remove(bala_inimigo)  # Remover a bala se ela sair da tela
        # Verificar se a bala inimiga colide com o jogador
        if bala_inimigo.rect.colliderect(rect):
            sys.exit()  # Fechar o jogo se houver colisão

    pygame.display.flip()
    clock.tick(60)
