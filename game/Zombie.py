import pygame
import glob
from .Bullet import Bullet

class Zombie(pygame.sprite.Sprite):
    def __init__(self, location, category, z_range, z_power, zombie_damage, zombie_shoot, *groups):
        super(Zombie, self).__init__(*groups)
        self.ani = None
        self.ani_pos = 0
        self.ani_max = 0
        self.image = None
        self.rect = None
        self.direction = 1
        self.category = category
        self.z_range = z_range.split()
        self.catch = False
        self.z_power = int(z_power)
        self.damage = zombie_damage
        self.can_shoot = zombie_shoot
        self.category = category
        self.ani_speed_init = 0
        self.height = 0
        self.width = 0
        # validating zombie sprites
        if self.category == "shoot":
            self.ani = glob.glob("sprites\\zombie\\shoot\\s*.png")
            self.height = 100
            self.width = 50
            self.ani_speed_init = 5
        elif self.category == "simple":
            self.ani = glob.glob("sprites\\zombie\\simple\\s*.png")
            self.height = 100
            self.width = 50
            self.ani_speed_init = 5
        elif self.category == "wolf":
            self.ani = glob.glob("sprites\\zombie\\wolf\\s*.png")
            self.height = 60
            self.width = 70
            self.ani_speed_init = 8
        elif self.category == "skeleton":
            self.ani = glob.glob("sprites\\zombie\\skeleton\\s*.png")
            self.height = 60
            self.width = 40
            self.ani_speed_init = 8
        elif self.category == "ghost":
            self.ani = glob.glob("sprites\\zombie\\ghost\\s*.png")
            self.height = 40
            self.width = 40
            self.ani_speed_init = 8
        elif self.category == "dragon":
            self.ani = glob.glob("sprites\\zombie\\fly\\dragon\\s*.png")
            self.height = 100
            self.width = 100
            self.ani_speed_init = 10
        elif self.category == "eagle":
            self.ani = glob.glob("sprites\\zombie\\fly\\eagle\\s*.png")
            self.height = 100
            self.width = 50
            self.ani_speed_init = 10
        self.ani_speed = self.ani_speed_init
        self.ani.sort()
        self.ani_max = len(self.ani) - 1
        self.image = pygame.transform.scale(pygame.image.load(self.ani[0]), (self.width, self.height))
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.now_shoot = 0
        self.gun_cooldown = 0
        self.bullet = None

    def update(self, dt, game, event):

        if self.category == "shoot" and self.now_shoot == 0:
            self.ani = glob.glob("sprites\\zombie\\shoot\\s*.png")
            self.ani_max = len(self.ani) - 1
        if int(self.z_range[0]) <= game.player.rect.x <= int(self.z_range[1]):
            self.catch = True
            if (int(self.rect.x) > game.player.rect.x):
                self.direction = -1
            else:
                self.direction = 1
        else:
            self.catch = False

        if self.can_shoot == "true" and self.catch == False:
            self.rect.x += self.direction * 100 * dt
            self.now_shoot = 0
        elif self.can_shoot == "true" and self.catch == True:
            self.rect.x = self.rect.x
            self.now_shoot = 1
        else:
            self.rect.x += self.direction * 100 * dt

        ## shoot towards player
        if self.now_shoot == 1 and not self.gun_cooldown:
            if self.direction > 0:
                self.bullet = Bullet(self.rect.midright, 1, "zombie", game.sprites)
            else:
                self.bullet = Bullet(self.rect.midleft, -1, "zombie", game.sprites)
                # set the amount of time until the player can shoot again
            self.gun_cooldown += 1
        self.gun_cooldown = max(0, self.gun_cooldown - dt)

        # check all repeat triggers in the map to see whether this zombie has
        # touched one
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'repeat'):
            # reverse movement direction; make sure to move the enemy out of the
            # collision so it doesn't collide again immediately next update
            if self.direction > 0:
                self.rect.right = cell.left
            else:
                self.rect.left = cell.right
            self.direction *= -1
            break

        # animating zombie
        if self.now_shoot == 0:
            self.ani_speed -= 1
            if self.ani_speed == 0:
                if self.direction == 1:
                    self.image = pygame.transform.flip(
                        pygame.transform.scale(pygame.image.load(self.ani[self.ani_pos]), (self.width, self.height)),
                        True, False)
                elif self.direction == -1:
                    self.image = pygame.transform.scale(pygame.image.load(self.ani[self.ani_pos]),
                                                        (self.width, self.height))
                self.ani_speed = self.ani_speed_init
                if self.ani_pos > self.ani_max - 1:
                    self.ani_pos = 0
                else:
                    self.ani_pos += 1
        elif self.now_shoot == 1 and self.category == "shoot":
            self.ani = glob.glob("sprites\\zombie\\shoot\\attack.png")
            if self.direction == 1:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(pygame.image.load(self.ani[0]), (self.width, self.height)), True, False)
            elif self.direction == -1:
                self.image = pygame.transform.scale(pygame.image.load(self.ani[0]), (self.width, self.height))
            self.ani_pos = 0

        # check for collision with the player; on collision mark the flag on the
        # player to indicate game over (a health level could be decremented here
        # instead)
        if game.player.bullet != None and self.rect.colliderect(game.player.bullet.rect):
            self.z_power -= 1
            game.player.bullet = None
            if (self.z_power == 0):
                self.kill()
                game.player.zombie_kill += 1

        ## if we collide with zombie
        if self.rect.colliderect(game.player.rect):
            if self.can_shoot == "false":
                game.player.strength -= self.damage

        ## decrease players life if bullet hits him
        if self.bullet != None and game.player.rect.colliderect(self.bullet.rect):
            self.bullet.kill()
            self.bullet = None
            game.player.strength -= self.damage

