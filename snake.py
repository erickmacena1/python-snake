import pygame
import random
import time
from math import floor

pygame.init()

azul = (50, 100, 213)
laranja = (205, 102, 0)
verde = (0, 255, 0)
amarelo = (255, 255, 102)

dimensoes = (600, 600)

### Valores Iniciais ###

x = 300
y = 300

d = 20

move_direction = ''

lista_cobra = [[x, y]]

dx = 0
dy = 0

x_comida = round(random.randrange(0, 600 - d) / 20) * 20
y_comida = round(random.randrange(0, 600 - d) / 20) * 20

fonte = pygame.font.SysFont("hack", 35)

tela = pygame.display.set_mode((dimensoes))
pygame.display.set_caption("Snake da Kenzie")

tela.fill(azul)

clock = pygame.time.Clock()
lacos = 0

# tempo em segundos
start_time = time.time()

def desenha_cobra(lista_cobra):
    tela.fill(azul)
    for unidade in lista_cobra:
        pygame.draw.rect(tela, laranja, [unidade[0], unidade[1], d, d])


def mover_cobra(dx, dy, lista_cobra, move_direction):
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print('Moving from ' + str(move_direction))
                if move_direction != 'R':
                    move_direction = 'L'
                    dx = -d
                    dy = 0
                
                print('Moving to ' + str(move_direction))
            
            elif event.key == pygame.K_RIGHT:
                print('Moving tfrom ' + str(move_direction))
                if move_direction != 'L':
                    move_direction = 'R'
                    dx = d
                    dy = 0
                print('Moving to ' + str(move_direction))
            
            elif event.key == pygame.K_UP:
                if move_direction != 'D':
                    move_direction = 'U'
                    dx = 0
                    dy = -d

            elif event.key == pygame.K_DOWN:
                if move_direction != 'U':
                    move_direction = 'D'
                    dx = 0
                    dy = d

    x_novo = lista_cobra[-1][0] + dx
    y_novo = lista_cobra[-1][1] + dy

    lista_cobra.append([x_novo, y_novo])
    
    del lista_cobra[0]

    return dx, dy, lista_cobra, move_direction

def verifica_comida(dx, dy, x_comida, y_comida, lista_cobra):
    head = lista_cobra[-1]

    x_novo = head[0] + dx
    y_novo = head[1] + dy

    if head[0] == x_comida and head[1] == y_comida:
        lista_cobra.append([x_novo, y_novo])

        x_comida = round(random.randrange(0, 600 - d) / 20) * 20
        y_comida = round(random.randrange(0, 600 - d) / 20) * 20
    
    pygame.draw.rect(tela, verde, [x_comida, y_comida, d, d])

    return x_comida, y_comida, lista_cobra

def verifica_parede(lista_cobra):
    head = lista_cobra[-1]
    x = head[0]
    y = head[1]

    if x not in range(600) or y not in range(600):
        raise Exception

def verifica_mordeu_cobra(lista_cobra):
    head = lista_cobra[-1]
    corpo = lista_cobra.copy()

    del corpo[-1]

    for x,y in corpo:
        if x == head[0] and y == head[1]:
            raise Exception

def atualizar_pontos(lista_cobra):
    pts = str(len(lista_cobra))
    escore = fonte.render("Pontuação: " + pts, True, amarelo)
    tela.blit(escore, [0, 0])

def conta_tempo(current_time):
    final_time = round(current_time - start_time)
    final_time = [floor(final_time / 60), final_time % 60]

    texto_tempo = ''

    # Se final_time[0] for igual a 0, então é Falso
    if final_time[0] != 0:
        texto_tempo = f"{final_time[0]}:"
    
    final_time[1] = f"0{final_time[1]}"
    
    # Pego as 2 ultimas posições da string 
    final_time[1] = final_time[1][-2:]
    texto_tempo = 'Tempo: ' + texto_tempo + final_time[1]
    
    tempo_jogo = fonte.render(texto_tempo, True, amarelo)
    tela.blit(tempo_jogo, [600 - len(texto_tempo) * 15, 0])

while True:
    pygame.display.update()
    desenha_cobra(lista_cobra)
    x_comida, y_comida, lista_cobra = verifica_comida(dx, dy, x_comida, y_comida, lista_cobra)

    if lacos == len(lista_cobra):
        dx, dy, lista_cobra, move_direction = mover_cobra(dx, dy, lista_cobra, move_direction)
        verifica_parede(lista_cobra)
        verifica_mordeu_cobra(lista_cobra)

    atualizar_pontos(lista_cobra)
    conta_tempo(time.time())
    clock.tick(24)
    lacos = (lacos + 1) % (15 - len(lista_cobra) + 1)
    print("Laço: " + str(lacos))