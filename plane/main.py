import pygame

from enemy import Enemy
from missile import Missile
from plane import Plane

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
player = Plane(SCREEN_WIDTH, SCREEN_HEIGHT)
# Create a custom event for adding a new enemy
ADD_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_ENEMY, 125)

# bg = pygame.image.load("/Users/yan.ren/github.com/yan.ren/programming-class/python_demo_programs/pygame_examples/plane/sky.jpeg")

running = True
# Create groups to hold enemy sprites and all sprites
# - enemies group is used for collision detection and position updates
# - all_sprites group is used for rendering
enemies = pygame.sprite.Group()
missiles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Add a new enemy?
        if event.type == ADD_ENEMY:
            new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            new_missile = Missile(SCREEN_WIDTH, player.rect.centerx, player.rect.centery)
            missiles.add(new_missile)
            all_sprites.add(new_missile)


    # Fill the background with white
    screen.fill(BLACK)
    # Draw all_sprites group on screen
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    # Check if any enemies group have collided with the player
    # find any sprites in the group collide with given sprite
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # Check collision between missiles and enemies
    # Check two sprite groups enemies and missiles if any object between two collides
    for enemy in enemies:
        if pygame.sprite.spritecollideany(enemy, missiles):
            enemy.kill()


    player.update(pygame.key.get_pressed())
    # Update enemy position
    enemies.update()
    # Update missile position
    missiles.update()
    pygame.display.update()
    clock.tick(FPS)
