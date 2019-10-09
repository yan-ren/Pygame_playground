import pygame, sys
import time

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
    x = WINDOW_WIDTH * 0.45
    y = WINDOW_HEIGHT * 0.8
    x_change = 0

    while not game_exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                    x_change = 0

        x += x_change

        if x < 0 or x > (WINDOW_WIDTH - car.get_rect().width):
            crash()
        # print(event)

        display.fill(WHITE)
        place_car(x, y)
        pygame.display.update()
        clock.tick(FPS)


game_loop()
pygame.quit()
sys.exit()