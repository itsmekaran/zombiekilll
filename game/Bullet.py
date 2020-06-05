import pygame

class Bullet(pygame.sprite.Sprite):

    def __init__(self, location, direction, bullet_type, *groups):
        super(Bullet, self).__init__(*groups)
        self.direction = direction
        self.type = bullet_type
        if bullet_type == "man":
            if self.direction == -1:
                self.image = pygame.transform.flip(pygame.image.load('man_bullet.png'), True, False)
            else:
                self.image = pygame.image.load('man_bullet.png')
            self.lifespan = 1
        elif bullet_type == "zombie":
            self.image = pygame.image.load('zombie_bullet.png')
            self.lifespan = 1
        if bullet_type == "boss":
            if self.direction == -1:
                self.image = pygame.image.load('boss_bullet.png')
            else:
                self.image = pygame.transform.flip(pygame.image.load('boss_bullet.png'), True, False)
            self.lifespan = 10

        if self.type == "man" or self.type == "zombie":
            self.rect = pygame.rect.Rect((location[0], location[1] - 11), self.image.get_size())
        elif self.type == "boss":
            self.rect = pygame.rect.Rect((location[0], location[1] - 17), self.image.get_size())

    def update(self, dt, game, event):
        # decrement the lifespan of the bullet by the amount of time passed and
        # remove it from the game if its time runs out
        self.lifespan -= dt
        if self.lifespan < 0:
            self.kill()
            return

        # move the enemy by 400 pixels per second in the movement direction
        self.rect.x += self.direction * 400 * dt

        if self.type == "man":
            if pygame.sprite.spritecollide(self, game.zombies, False) or pygame.sprite.spritecollide(self, game.bosses,
                                                                                                     False):
                # game.explosion.play()
                # we also remove the bullet from the game or it will continue on
                # until its lifespan expires
                self.kill()

        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'blockers'):
            self.kill()
