import numpy
import pygame
import random

pygame.init()
GAME_WIDTH = 25
GAME_HIEGHT = 25
SQUARE_SIZE = 20
SPEED = 10
START_LENGHT = 1
LINE_SIZE = 1
SNAKE_COLOUR = (0, 0, 0)
FOOD_COLOUR = (200, 0, 0)
GRID_COLOUR = (0, 100, 0)
SCREEN_COLOUR = (255, 255, 230)
FONT = pygame.font.SysFont("momospace", 35)


def draw_square(screen, colour, square):
    pygame.draw.rect(screen, colour, square)


def food_init(width, height):
    food_start_x = random.randint(int(width / 4), int(3 * width / 4))
    food_start_y = random.randint(int(height / 4), int(3 * height / 4))
    return [food_start_x, food_start_y]


def food_set(width, height):
    food_x = random.randint(0, width - 1)
    food_y = random.randint(0, height - 1)
    return [food_x, food_y]


def snake_init(width, height):
    snake_start_x = random.randint(int(width / 4), int(3 * width / 4))
    snake_start_y = random.randint(int(height / 4), int(3 * height / 4))
    if snake_start_x < width / 2:
        if snake_start_y < height / 2:
            direction = random.randint(0, 1)
        else:
            direction = random.randint(1, 2)
    else:
        if snake_start_y < height / 2:
            direction = random.randint(2, 3)
        else:
            direction = random.randint(3, 4)
    return [snake_start_x, snake_start_y], direction


screen = pygame.display.set_mode(
    [GAME_WIDTH * (SQUARE_SIZE + LINE_SIZE) + LINE_SIZE, GAME_HIEGHT * (SQUARE_SIZE + LINE_SIZE) + 2 * SQUARE_SIZE])
Backing_Grid = pygame.Rect(0, 0, GAME_WIDTH * (SQUARE_SIZE + LINE_SIZE) + LINE_SIZE,
                           GAME_WIDTH * (SQUARE_SIZE + LINE_SIZE) + LINE_SIZE)

Game_Array = numpy.zeros((GAME_WIDTH, GAME_HIEGHT))

screen.fill(SCREEN_COLOUR)
pygame.draw.rect(screen, GRID_COLOUR, Backing_Grid)
clock = pygame.time.Clock()

Food_Location = food_init(GAME_WIDTH, GAME_HIEGHT)
Snake_Head, direction = snake_init(GAME_WIDTH, GAME_HIEGHT)
Snake_Length = START_LENGHT

while Food_Location == Snake_Head:
    Snake_Head, direction = snake_init(GAME_WIDTH, GAME_HIEGHT)

Game_Array[Food_Location[0], Food_Location[1]] = -1
Game_Array[Snake_Head[0], Snake_Head[1]] = 1

Game_Over = False
Ate = False
Score = 0

while not Game_Over:
    # Close Button Click?

    screen.fill(SCREEN_COLOUR)
    pygame.draw.rect(screen, GRID_COLOUR, Backing_Grid)
    for ii in range(GAME_WIDTH):
        for jj in range(GAME_HIEGHT):
            if Game_Array[ii, jj] > 0:
                square = pygame.Rect(ii * SQUARE_SIZE + (ii + 1) * LINE_SIZE, jj * SQUARE_SIZE + (jj + 1) * LINE_SIZE,
                                     SQUARE_SIZE, SQUARE_SIZE)
                draw_square(screen, SNAKE_COLOUR, square)
            elif Game_Array[ii, jj] < 0:
                square = pygame.Rect(ii * SQUARE_SIZE + (ii + 1) * LINE_SIZE, jj * SQUARE_SIZE + (jj + 1) * LINE_SIZE,
                                     SQUARE_SIZE, SQUARE_SIZE)
                draw_square(screen, FOOD_COLOUR, square)
            else:
                square = pygame.Rect(ii * SQUARE_SIZE + (ii + 1) * LINE_SIZE, jj * SQUARE_SIZE + (jj + 1) * LINE_SIZE,
                                     SQUARE_SIZE, SQUARE_SIZE)
                draw_square(screen, SCREEN_COLOUR, square)

    text = "Score: " + str(Score)
    label = FONT.render(text, 1, SNAKE_COLOUR)
    screen.blit(label, (GAME_WIDTH * (SQUARE_SIZE + LINE_SIZE) + LINE_SIZE - 150,
                        GAME_HIEGHT * (SQUARE_SIZE + LINE_SIZE) + 2 * SQUARE_SIZE - 25))

    pygame.display.update()

    clock.tick(SPEED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game_Over = True
            print(Score)
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not direction == 0:
                    direction = 3
            if event.key == pygame.K_RIGHT:
                if not direction == 3:
                    direction = 0
            if event.key == pygame.K_UP:
                if not direction == 1:
                    direction = 2
            if event.key == pygame.K_DOWN:
                if not direction == 2:
                    direction = 1

    if direction == 0:
        Snake_Head[0] += 1
    elif direction == 1:
        Snake_Head[1] += 1
    elif direction == 2:
        Snake_Head[1] -= 1
    else:
        Snake_Head[0] -= 1

    if Snake_Head[0] > GAME_WIDTH - 1 or Snake_Head[0] < 0 or Snake_Head[1] > GAME_HIEGHT - 1 or Snake_Head[1] < 0:
        Game_Over = True
        break
    if Game_Array[Snake_Head[0], Snake_Head[1]] > 0:
        Game_Over = True
        print(Score)
        break

    if Snake_Head == Food_Location:
        Snake_Length += 1
        Ate = True
        Score += 1

    if Ate:
        Food_Location = food_set(GAME_WIDTH, GAME_HIEGHT)
        while Game_Array[Food_Location[0], Food_Location[1]] > 0:
            Food_Location = food_set(GAME_WIDTH, GAME_HIEGHT)
        Game_Array[Food_Location[0], Food_Location[1]] = -1

    if not Ate:
        with numpy.nditer(Game_Array, op_flags=['readwrite']) as it:
            for x in it:
                if x > 0:
                    x -= 1
    Ate = False

    Game_Array[Snake_Head[0], Snake_Head[1]] = Snake_Length

    clock.tick(SPEED)
