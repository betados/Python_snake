import pygame
import random
import sys
from pygame.locals import *

DIR = {"up": (0, -1), "down": (0, 1), "right": (1, 0), "left": (-1, 0)}
RED = (255, 0, 0)
GREEN = (0, 255, 0)

N_CUADROS = 40
RAD = 6

def move_snake(snake):
    global keys
    if (snake["dir"] == "up" or snake["dir"] == "down") and K_LEFT in keys:
        snake["dir"] = "left"
    elif (snake["dir"] == "up" or snake["dir"] == "down") and K_RIGHT in keys:
        snake["dir"] = "right"
    elif (snake["dir"] == "left" or snake["dir"] == "right") and K_UP in keys:
        snake["dir"] = "up"
    elif (snake["dir"] == "left" or snake["dir"] == "right") and K_DOWN in keys:
        snake["dir"] = "down"
    snake["rings"].pop()
    x = snake["rings"][0][0] + 2 * RAD * DIR[snake["dir"]][0]
    y = snake["rings"][0][1] + 2 * RAD * DIR[snake["dir"]][1]
    snake["rings"].insert(0, (x, y))


def enlarge_snake(snake):
    x = snake["rings"][0][0] + 2 * RAD * DIR[snake["dir"]][0]
    y = snake["rings"][0][1] + 2 * RAD * DIR[snake["dir"]][1]
    snake["rings"].insert(0, (x, y))


def generate_food():
    x = random.randrange(1, N_CUADROS - 1)
    y = random.randrange(1, N_CUADROS - 1)
    return 2 * RAD *x, 2 * RAD *y


def check_food(snake):
    global food
    if snake["rings"][0] == food:
        enlarge_snake(snake)
        food = generate_food()


def draw(screen, snake, food):
    screen.blit(pygame.Surface(screen.get_size()), (0, 0))
    pygame.draw.rect(screen, RED, Rect(food, (2 * RAD, 2 * RAD)))
    for ring in snake["rings"]:
        pygame.draw.circle(screen, GREEN, (ring[0] + RAD, ring[1] + RAD), RAD)


def check_collisions(snake):
    head = snake["rings"][0]
    if head[0] < 0 or head[0] > N_CUADROS * 2 * RAD:
        return True
    if head[1] < 0 or head[1] > N_CUADROS * 2 * RAD:
        return True
    for ring in snake["rings"][1:]:
        if head == ring:
            return True

    return False


def game_over(screen):
    font = pygame.font.SysFont('Arial', RAD * 8, bold=True)
    text = font.render('Game Over', 0, RED)
    pos = (7*2*RAD, (N_CUADROS - 4)*RAD)
    screen.blit(text, pos)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((N_CUADROS*2 * RAD, N_CUADROS*2 * RAD))

snake = {"dir": "right", "rings":
        [(12*2 * RAD, 13*2 * RAD), (12*2 * RAD, 12*2 * RAD), (12*2 * RAD, 11*2 * RAD), (12*2 * RAD, 10*2 * RAD)]}
food = generate_food()

draw(screen, snake, food)
pygame.display.flip()

keys = []

while True:

    clock.tick(10)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        if event.type == KEYDOWN:
            keys.append(event.key)
        if event.type == KEYUP:
            keys.remove(event.key)

    check_food(snake)
    move_snake(snake)
    draw(screen, snake, food)
    if check_collisions(snake):
        game_over(screen)
        break
    pygame.display.flip()

pygame.display.flip()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
