import pygame, sys

# constant
FPS = 60
WHITE = (255, 255, 255)
# variables
window_width = 800
window_height = 600
crashed = False
x = window_width * 0.45
y = window_height * 0.8
x_change = 0
y_change = 9

pygame.init()
display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Race Car')
clock = pygame.time.Clock()
car = pygame.image.load('./img/car1.png').convert_alpha()


def place_car(x, y):
    display.blit(car, (x, y))


while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            elif event.key == pygame.K_RIGHT:
                x_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                x_change = 0

    x += x_change
    # print(event)

    display.fill(WHITE)
    place_car(x, y)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
