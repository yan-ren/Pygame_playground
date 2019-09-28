import pygame, sys

# constant
FPS = 60
WHITE = (255, 255, 255)
# variables
window_width = 800
window_height = 600
crashed = False

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

        # print(event)

    display.fill(WHITE)
    place_car(window_width * 0.45, window_height * 0.8)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
