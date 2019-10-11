import pygame, sys
import time
import random

# constant
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# variables
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

pygame.init()
display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Race Car')
clock = pygame.time.Clock()
car = pygame.image.load('./img/car1.png').convert_alpha()


def draw_block(x, y, width, height, color):
    pygame.draw.rect(display, color,(x, y, width, height))


def place_car(x, y):
    display.blit(car, (x, y))


def crash():
    message_display('You Crashed!')


def message_display(msg):
    text_style = pygame.font.Font('freesansbold.ttf', 115)
    text_surf = text_style.render(msg, True, BLACK)
    text_rect = text_surf.get_rect()
    text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    display.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)

    # start game again
    game_loop()


def game_loop():
    game_exit = False
    car_x = WINDOW_WIDTH * 0.45
    car_y = WINDOW_HEIGHT * 0.8
    car_x_change = 0
    block_x = random.randint(0, WINDOW_WIDTH)
    block_y = -WINDOW_HEIGHT
    block_speed = 7
    block_width = 100
    block_height = 100

    while not game_exit:

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    car_x_change = -5
                elif event.key == pygame.K_RIGHT:
                    car_x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    car_x_change = 0

        # movement variable
        car_x += car_x_change
        block_y += block_speed

        # movement variable handling
        if car_x < 0 or car_x > (WINDOW_WIDTH - car.get_rect().width):
            crash()
            game_exit = True

        if car_y < block_y + block_height:
            if block_x < car_x < block_x + block_width or block_x < car_x + car.get_rect().width < block_x + block_width:
                crash()
                game_exit = True

        # print(event)
        if block_y > WINDOW_HEIGHT:
            block_y = -WINDOW_HEIGHT
            block_x = random.randint(0, WINDOW_WIDTH)

        # display
        display.fill(WHITE)
        place_car(car_x, car_y)
        draw_block(block_x, block_y, block_width, block_height, BLACK)
        pygame.display.update()

        # FPS
        clock.tick(FPS)


game_loop()
pygame.quit()
sys.exit()