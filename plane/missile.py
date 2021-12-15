import pygame.sprite

# constructor in the class helps to initialize value when using class to create object
class Missile(pygame.sprite.Sprite):
    def __init__(self, window_width, x, y):
        super(Missile, self).__init__()
        self.window_width = window_width
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(
            center=(x, y)
        )
        self.speed = 20

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.right > self.window_width:
            self.kill()
