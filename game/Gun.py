import pygame

class Gun(pygame.sprite.Sprite):
    image = pygame.image.load('gun_icon.png')

    def __init__(self, location, *groups):
        super(Gun, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.direction = 1

    def update(self, dt, game, event):
        if self.rect.colliderect(game.player.rect):
            self.kill()
            game.player.can_shoot = True