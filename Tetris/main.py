import pygame as pg
import random as rnd
import time
from dataclasses import dataclass

pg.init()
width, columns, rows = 400, 15, 30
distance = width // columns
height = distance * rows
speed = 500
score = 0
rank = 1
heightLimit = 15
rateUpRank = 500


# Srore for test
scoreTest = 100

# * Grid has [0] and length is columns * rows
grid = [0] * columns * rows

# * Load Images
pictures = []
for n in range(8):
    pictures.append(pg.transform.scale(
        pg.image.load(f'./assets/T_{n}.gif'), (distance, distance)))


# * Main loop
screen = pg.display.set_mode([width, height])
pg.display.set_caption('Tetris Game')


# TODO: Actions
tetrominio_down = pg.USEREVENT + 1
speed_up = pg.USEREVENT + 2

pg.time.set_timer(tetrominio_down, speed)
pg.time.set_timer(speed_up, speed)


# TODO: Set Tetrominoes
tetrominoes = [
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # * O
    [0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # * I
    [0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0, 0, 0, 0],  # * L
    [0, 0, 4, 0, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # * J
    [0, 5, 5, 0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # * S
    [6, 6, 0, 0, 0, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # * Z
    [0, 0, 0, 0, 7, 7, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0]]  # * T


# TODO: Create a class with it's functions
@dataclass
class tetrominio():
    tetro: list
    rows: int = 0
    columns: int = 5  # * Ratio

    def show(self):
        for n, color in enumerate(self.tetro):
            if color > 0:
                # * n = 0 ~ 15, columns = 5, if n > columns, so rows more than 2, else rows is 1
                x = (n % 4 + self.columns) * distance
                y = (n // 4 + self.rows) * distance

                # * Pictures[color] = Pictures[2] = T_2.gif with set position => Show
                screen.blit(pictures[color], (x, y))

    def update(self, r, c):
        if self.check(self.rows + r, self.columns + c):
            self.rows += r
            self.columns += c
            return True
        return False

    def rotation(self):
        clone = self.tetro.copy()
        for n, color in enumerate(clone):
            self.tetro[(2 - (n % 4)) * 4 + (n // 4)] = color

        if not self.check(self.rows, self.columns):
            self.tetro = clone.copy()

    def check(self, r, c):
        for n, color in enumerate(self.tetro):
            if color > 0:
                rs = r + n // 4
                cs = c + n % 4
                if cs < 0 or rs >= rows or cs >= columns or grid[rs * columns + cs] > 0:
                    return False
        return True


# * Create a object
char = tetrominio(rnd.choice(tetrominoes))


# TODO: Fixed Object and create new Object
def ObjectOnGrid():
    for n, color in enumerate(char.tetro):
        if color > 0:
            # * Calculate the position of grid and set it's value to color value [ 1 ~ 6]
            grid[(char.rows + n // 4) * columns +
                 (char.columns + n % 4)] = color


# TODO: Delete Row
def DeleteRow():
    for row in range(rows):
        for column in range(columns):
            if grid[row * columns + column] == 0:
                break
        else:
            # * After deleted, The grid is missing 16 columns
            del grid[row * columns: row * columns + column]
            grid[0:0] = [0] * columns
            return 100
    return scoreTest


# TODO: Check height
def CheckHeight():
    count = 0
    for n in range(heightLimit):
        for column in range(columns):
            if (grid[n * columns + column]) > 0:
                count = 1
    return count


# * Main loop
status = True
isRunning = True
while status:
    pg.time.delay(100)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            status = False
        if event.type == tetrominio_down:
            if not char.update(1, 0):
                if isRunning:
                    ObjectOnGrid()
                if CheckHeight() == 1:
                    isRunning = False
                    print("Full")

                char = tetrominio(rnd.choice(tetrominoes))
                score += DeleteRow()

        if event.type == speed_up:
            if score % rateUpRank == 0 and score != 0:
                speed = int(speed * 0.9)
                pg.time.set_timer(tetrominio_down, speed)
                rank = score // rateUpRank + 1

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                char.update(0, -1)
            if event.key == pg.K_RIGHT:
                char.update(0, 1)
            if event.key == pg.K_DOWN:
                for n in range(2):
                    char.update(1, 0)
            if event.key == pg.K_UP:
                char.rotation()
            if event.key == pg.K_SPACE:
                if not isRunning:
                    grid = [0] * rows * columns
                    score = 0
                    rank = 1
                    isRunning = True

    # * Fill Color background
    screen.fill((128, 128, 128))

    # * Show Char
    if isRunning:
        char.show()

    # * Show Score and Rank
    scoreLabel = pg.font.SysFont('consolas', 30).render(
        f'Score: {score:,}', False, (255, 255, 255))
    rankLabel = pg.font.SysFont('consolas', 20).render(
        f'level: {rank}', False, (255, 255, 255))

    # * Show texts when game over
    gameOverLabel = pg.font.SysFont('consolas', 50).render(
        f'GAME OVER', False, (255, 255, 255))

    overScoreLabel = pg.font.SysFont('consolas', 30).render(
        f'Score: {score:,}', False, (255, 255, 255))

    # screen.blit(scoreLabel, (width // 2 - scoreLabel.get_width() // 2, 5))
    # screen.blit(rankLabel, (width // 2 - scoreLabel.get_width() // 2, 55))
    if isRunning:
        screen.blit(scoreLabel, (10, 5))
        screen.blit(rankLabel, (10, 40))
    else:
        screen.blit(gameOverLabel, (width // 2 -
                                    gameOverLabel.get_width() // 2, 100))

        screen.blit(overScoreLabel, (width // 2 -
                                     overScoreLabel.get_width() // 2, 170))
    for n, color in enumerate(grid):
        if color > 0:
            # * n = 19, columns = 15, if n > columns, so rows more than 2, else rows is 1
            x = n % columns * distance
            y = n // columns * distance

            # * Pictures[color] = Pictures[2] = T_2.gif with set position
            screen.blit(pictures[color], (x, y))

    # * Fill Box color
    pg.display.flip()

pg.quit()
