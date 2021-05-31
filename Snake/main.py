from typing import Tuple
import pygame as pg
import random as rnd
import time
from dataclasses import dataclass

from pygame.constants import KEYDOWN, K_DOWN, K_LEFT, K_RIGHT, K_SPACE, K_UP
pg.init()

# * Configurations
columns, rows = 30, 25
width = 700
distance = width // columns  # * distance = 25
height = distance * rows
isRunning = True
speed = 100
snakePos = [15, 5]
snakeBody = [[15, 5], [16, 5], [17, 5]]
rankRate = 10

score = 0
# * Grid has [0] and length is columns * rows
grid = [0] * columns * rows

# * Load Images
pictures = []
for n in range(8):
    pictures.append(pg.transform.scale(
        pg.image.load(f'./assets/T_{n}.gif'), (distance, distance)))


@dataclass
class Snake():
    snake: list

    def init(self):
        for x, y in (self.snake):
            xLength = x * distance
            yLength = y * distance
            screen.blit(pictures[2], (xLength, yLength))

    def update(self, x, y):
        snakePos[0] += x
        snakePos[1] += y
        self.snake.insert(0, list(snakePos))
        self.snake.pop()

    def check(self):
        count = 0
        for b in self.snake[2:]:
            if self.snake[0][0] == b[0] and self.snake[0][1] == b[1]:
                count += 1
        if self.snake[0][0] > (columns - 1) or self.snake[0][0] < 0 or self.snake[0][1] < 0 or self.snake[0][1] > (rows - 1):
            count += 1

        if count > 0:
            snakePos[0] = 15
            snakePos[1] = 5
            self.snake = [[15, 5], [16, 5], [17, 5]]
            return False
        return True

    def rotate(self, direction):
        if direction == "UP":
            self.update(0, -1)
        if direction == "DOWN":
            self.update(0, 1)
        if direction == "RIGHT":
            self.update(1, 0)
        if direction == "LEFT":
            self.update(-1, 0)


snake = Snake(snakeBody)

# * Main loop
screen = pg.display.set_mode([width, height])
pg.display.set_caption('Tetris Game')


# * Userevent
RUN = pg.USEREVENT + 1
pg.time.set_timer(
    RUN, speed // int((score // rankRate * 0.7 + 1)))

CREATE_APPLE = pg.USEREVENT + 2
pg.time.set_timer(CREATE_APPLE, speed)


# TODO: Create random an apple
appleExist = True
appleLocation = [rnd.randint(1, columns - 1), rnd.randint(1, rows - 1)]
snake.snake.insert(0, list(appleLocation))
snake.snake.insert(0, list(appleLocation))
snake.snake.pop()
snake.snake.pop()

direction = "RIGHT"
isPlaying = True
while isRunning:
    # pg.time.delay(200)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            isRunning = False
        if event.type == RUN:
            if direction == "RIGHT":
                snake.update(1, 0)
            if direction == "LEFT":
                snake.update(-1, 0)
            if direction == "UP":
                snake.update(0, -1)
            if direction == "DOWN":
                snake.update(0, 1)
        if event.type == KEYDOWN:
            if event.key == K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == K_RIGHT and direction != "LEFT":
                direction = "RIGHT"
            if event.key == K_SPACE:
                if not isPlaying:
                    isPlaying = True
                    score = 0
                    direction = "RIGHT"

    # TODO: Check the first location of the snake has the same apple
    if snakePos[0] == appleLocation[0] and snakePos[1] == appleLocation[1]:
        snake.snake.insert(0, list(appleLocation))
        score += 1
        appleExist = False

    screen.fill((40, 40, 40))
    if appleExist == False:
        appleLocation = [rnd.randint(1, columns - 1), rnd.randint(1, rows - 1)]

    appleExist = True
    check = True

    if isPlaying:
        snake.init()
        scoreLabel = pg.font.SysFont('consolas', 30).render(
            f'Score: {score:,}', False, (255, 255, 255))
        rankLabel = pg.font.SysFont('consolas', 20).render(
            f'level: {score // rankRate + 1}', False, (255, 255, 255))

        screen.blit(scoreLabel, (10, 5))
        screen.blit(rankLabel, (10, 40))
        screen.blit(pictures[3], (appleLocation[0] *
                                  distance, appleLocation[1] * distance))
        check = snake.check()
        if check == False:
            isPlaying = False

    else:
        # * Show texts when game over
        gameOverLabel = pg.font.SysFont('consolas', 50).render(
            f'GAME OVER', False, (255, 255, 255))
        overScoreLabel = pg.font.SysFont('consolas', 30).render(
            f'Score: {score:,}', False, (255, 255, 255))

        screen.blit(gameOverLabel, (width // 2 -
                                    gameOverLabel.get_width() // 2, 50))
        screen.blit(overScoreLabel, (width // 2 -
                                     scoreLabel.get_width() // 2, 120))

    pg.display.flip()

pg.quit()
