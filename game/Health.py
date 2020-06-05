import pygame

class Health(pygame.sprite.Sprite):
    def __init__(self, location, value, *groups):
        super(Health, self).__init__(*groups)
        self.value = value
        self.image = pygame.transform.scale(pygame.image.load("life.png"), (40, 40))
        self.rect = pygame.rect.Rect(location, self.image.get_size())

    def update(self, dt, game, event):
        if self.rect.colliderect(game.player.rect):
            temp = (250 - game.player.strength)
            if temp <= self.value:
                game.player.strength = 250
            else:
                game.player.strength += self.value
            self.kill()
