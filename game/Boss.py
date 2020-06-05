import pygame
import glob
from random import randint
from .Bullet import Bullet
from .Zombie import Zombie

class Boss(pygame.sprite.Sprite):
    def __init__(self, location, category, z_range, z_power, zombie_damage, zombie_shoot, *groups):
        super(Boss, self).__init__(*groups)
        self.ani_pos = 0
        self.direction = 1
        self.category = category
        self.pass_range = z_range
        self.z_range = z_range.split()
        self.catch = False
        self.strength = int(z_power)
        self.damage = zombie_damage
        self.can_shoot = zombie_shoot
        self.category = category
        self.ani = glob.glob("sprites\\boss\\walk\\s*.png")
        self.height = 150
        self.width = 100
        self.ani_speed_init = 5
        self.ani_speed = self.ani_speed_init
        self.ani.sort()
        self.ani_max = len(self.ani) - 1
        self.image = pygame.transform.scale(pygame.image.load(self.ani[0]), (self.width, self.height))
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.now_shoot = 0
        self.gun_cooldown = 0
        self.bullet = None
        self.clock1 = 0
        self.clock2 = 0
        self.dict = {1: 'simple', 2: "shoot", 3: "wolf", 4: "ghost", 5: "skeleton", 6: "eagle", 7: "dragon"}
        self.dict_len = len(self.dict)
        self.zombie_val = randint(1, 7)
        self.zombie_can_shoot = False
        self.boss_kill = 0
        self.dead = 0

    def boss_health(self, screen):
        color = None
        if self.strength >= 80:
            color = (0, 255, 0)
        elif self.strength >= 30:
            color = (255, 255, 0)
        else:
            color = (255, 0, 0)
        if self.strength <= 0:
            self.strength = 0
        font = pygame.font.Font(None, 20)
        label = font.render("Boss Life :", 1, color)
        screen.blit(label, (10, 40))
        pygame.draw.rect(screen, color, (95, 40, self.strength, 20))

    def update(self, dt, game, event):
        ## track player
        if (int(self.rect.x) > game.player.rect.x):
            self.direction = -1
        else:
            self.direction = 1
        if self.clock2 != 10 and self.strength > 0:
            self.ani = glob.glob("sprites\\boss\\walk\\s*.png")
            self.ani_max = len(self.ani) - 1
        if self.strength == 0 and self.dead == 0:
            self.ani = glob.glob("sprites\\boss\\dead\\s*.png")
            self.ani_max = len(self.ani) - 1
            self.ani_pos = 0
            self.ani_speed_init = 5
        self.clock1 += dt
        self.clock2 += dt
        if self.clock1 > 3 and self.strength > 0:
            if self.dict[self.zombie_val] == "simple":
                height = self.rect.y + 50
                self.zombie_can_shoot = "false"
            elif self.dict[self.zombie_val] == "shoot":
                height = self.rect.y + 50
                self.zombie_can_shoot = "true"
            elif self.dict[self.zombie_val] == "wolf" or self.dict[self.zombie_val] == "ghost" or self.dict[
                self.zombie_val] == "skeleton":
                height = self.rect.y + 90
                self.zombie_can_shoot = "false"
            elif self.dict[self.zombie_val] == "eagle" or self.dict[self.zombie_val] == "dragon":
                height = self.rect.y
                self.zombie_can_shoot = "false"
            Zombie((self.rect.x, height), self.dict[self.zombie_val], self.pass_range, 2, 1, self.zombie_can_shoot,
                   game.zombies)
            self.clock1 = 0
            self.zombie_val = randint(1, 7)

        if self.clock2 > 5 and self.strength > 0:
            self.ani = glob.glob("sprites\\boss\\shoot\\s0.png")
            if self.direction == 1:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(pygame.image.load(self.ani[0]), (self.width, self.height)), True, False)
            elif self.direction == -1:
                self.image = pygame.transform.scale(pygame.image.load(self.ani[0]), (self.width, self.height))
            if self.direction > 0:
                self.bullet = Bullet(self.rect.midright, 1, "boss", game.sprites)
            else:
                self.bullet = Bullet(self.rect.midleft, -1, "boss", game.sprites)
            self.ani_pos = 0
            self.clock2 = 0
            game.boss_shoot.play()
        self.rect.x += self.direction * 50 * dt

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
        if self.strength > 0:
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
        elif self.strength == 0:
            self.dead = 1
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
                    self.kill()
                    self.boss_kill = 1
                else:
                    self.ani_pos += 1

        # check for collision with the player; on collision mark the flag on the
        # player to indicate game over (a health level could be decremented here
        # instead)
        if game.player.bullet != None and self.rect.colliderect(game.player.bullet.rect):
            self.strength -= 10
            game.player.bullet = None
            if (self.strength == 0):
                self.strength = 0

        ## decrease players life if bullet hits him
        if self.bullet != None and game.player.rect.colliderect(self.bullet.rect):
            self.bullet.kill()
            self.bullet = None
            game.player.strength -= self.damage