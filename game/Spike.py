import pygame
import glob

class Spike(pygame.sprite.Sprite):
    def __init__(self, location, width, damage, spike_type, *groups):
        super(Spike, self).__init__(*groups)
        self.width = int(width)
        self.type = spike_type
        self.animation = 0
        self.ani_speed_init = 5
        self.ani_speed = self.ani_speed_init
        self.ani_pos = 0
        if self.type == "spike":
            # self.image = pygame.transform.scale(pygame.image.load('spike.png'),(self.width, 100))
            self.ani = glob.glob("spike.png")
        elif self.type == "lava":
            self.ani = glob.glob("sprites\\lava\\s*.png")
            self.animation = 1
        # self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.ani.sort()
        self.ani_max = len(self.ani) - 1
        self.image = pygame.transform.scale(pygame.image.load(self.ani[0]), (self.width, 100))
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.damage = damage

    def update(self, dt, game, event):
        if self.animation == 1:
            self.ani_speed -= 1
            if self.ani_speed == 0:
                self.image = pygame.transform.scale(pygame.image.load(self.ani[self.ani_pos]), (self.width, 100))
                self.ani_speed = self.ani_speed_init
            if self.ani_pos >= self.ani_max - 1:
                self.ani_pos = 0
            else:
                self.ani_pos += 1
        if self.rect.colliderect(game.player.rect):
            game.player.rect = game.player.rect
            game.player.strength -= self.damage

