import pygame, sys

pygame.init()

display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Race Car')
clock = pygame.time.Clock()
crashed = False
FPS = 60

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()
