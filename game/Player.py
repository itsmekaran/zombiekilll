import pygame
import glob
from .Bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.resting = True
        self.dy = 0
        self.is_dead = False
        self.direction = 1
        self.can_shoot = False
        ## animating images
        self.ani_speed_init = 1
        self.ani_speed = self.ani_speed_init
        self.ani = glob.glob("sprites\\run\s*.png")
        self.ani.sort()
        self.ani_pos = 0
        self.ani_max = len(self.ani) - 1
        self.image = pygame.transform.scale(pygame.image.load(self.ani[0]), (50, 90))
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.sit = 0
        # time since the player last shot
        self.gun_cooldown = 0
        self.bullet = None
        self.strength = 250
        self.gun_cooldown = 0
        self.level_end = 0
        self.zombie_kill = 0

    ### User's Life
    def draw_strength(self, screen):
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
        label = font.render("Life :", 1, color)
        screen.blit(label, (10, 15))
        pygame.draw.rect(screen, color, (45, 10, self.strength, 20))

    ### User's Progress
    def draw_progress(self, screen, level, zombie_count):
        font = pygame.font.Font(None, 20)
        if level == 1 or level == 2:
            if level == 1:
                progress = (float(3100 - self.rect.x) / 3100) * 100
            elif level == 2:
                progress = (float(6336 - self.rect.x) / 6336) * 100
            progress = 100 - int(progress)
            if progress > 100:
                progress = 100
            if progress >= 90:
                color = (0, 255, 0)
            elif progress >= 30:
                color = (255, 255, 0)
            else:
                color = (255, 0, 0)
            label = font.render("Progress :" + str(progress) + " %", 1, color)
            screen.blit(label, (300, 15))
            green_color = (0, 255, 255)
            label_level = font.render("Level :" + str(level), 1, green_color)
            screen.blit(label_level, (500, 15))
            label_level = font.render("Zombies Left :" + str(zombie_count), 1, green_color)
            screen.blit(label_level, (600, 15))
        elif level == 3:
            green_color = (0, 255, 255)
            label_level = font.render("Level :" + str(level), 1, green_color)
            screen.blit(label_level, (500, 15))

    def update(self, dt, game, event):
        last = self.rect.copy()
        # check strength
        if self.strength <= 0:
            self.is_dead = True
            self.kill()
        # handle
        if self.resting == False and self.can_shoot == False:
            self.ani = glob.glob("sprites\\jump\s*.png")
            self.ani_speed_init = 4
        elif self.can_shoot == False:
            self.ani = glob.glob("sprites\\run\s*.png")
            self.ani_speed_init = 1
        elif self.can_shoot == True and self.resting == True:
            self.ani = glob.glob("sprites\\shoot\s*.png")
            self.ani_speed_init = 1
        if event.type == pygame.KEYUP and self.resting == True:
            if event.key == pygame.K_LEFT and self.sit == 0:
                self.image = pygame.transform.scale(pygame.image.load(self.ani[0]), (50, 90))
            elif event.key == pygame.K_RIGHT and self.sit == 0:
                self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.ani[0]), (50, 90)),
                                                   True, False)

        key = pygame.key.get_pressed()
        ## validating sit
        if not key[pygame.K_DOWN] and self.sit == 1:
            if self.direction == 1:
                self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.ani[0]), (50, 90)),
                                                   True, False)
            elif self.direction == -1:
                self.image = pygame.transform.scale(pygame.image.load(self.ani[0]), (50, 90))
            self.rect = pygame.rect.Rect((self.rect.x, self.rect.y), self.image.get_size())
            self.sit = 0

        if key[pygame.K_LEFT] and self.sit == 0:
            self.rect.x -= 300 * dt
            self.direction = -1
            ##animated movement
            self.ani_speed -= 1
            if self.ani_speed == 0:
                self.image = pygame.transform.scale(pygame.image.load(self.ani[self.ani_pos]), (50, 90))
                self.ani_speed = self.ani_speed_init
                if self.ani_pos >= self.ani_max:
                    self.ani_pos = 0
                else:
                    self.ani_pos += 1

        if key[pygame.K_RIGHT] and self.sit == 0:
            self.rect.x += 300 * dt
            self.direction = 1
            ##animated movement
            self.ani_speed -= 1
            if self.ani_speed == 0:
                self.image = pygame.transform.flip(
                    pygame.transform.scale(pygame.image.load(self.ani[self.ani_pos]), (50, 90)), True, False)
                self.ani_speed = self.ani_speed_init
                if self.ani_pos >= self.ani_max:
                    self.ani_pos = 0
                else:
                    self.ani_pos += 1

        # handle the player shooting key
        if key[pygame.K_b] and not self.gun_cooldown and self.can_shoot == True:
            # create a bullet at an appropriate position (the side of the player
            # sprite) and travelling in the correct direction
            if self.direction > 0:
                self.bullet = Bullet(self.rect.midright, 1, "man", game.sprites)
            else:
                self.bullet = Bullet(self.rect.midleft, -1, "man", game.sprites)
            # set the amount of time until the player can shoot again
            self.gun_cooldown += 0.5
            game.shoot.play()

        # decrement the time since the player last shot to a minimum of 0 (so
        # boolean checks work)
        self.gun_cooldown = max(0, self.gun_cooldown - dt)

        # sitting
        if key[pygame.K_DOWN] and self.sit == 0 and self.resting == True:
            if self.can_shoot == True:
                self.ani = glob.glob("sprites\\run\\a2.png")
            else:
                self.ani = glob.glob("sprites\\run\\a1.png")
            if self.direction == 1:
                self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.ani[0]), (50, 52)),
                                                   True, False)
            elif self.direction == -1:
                self.image = pygame.transform.scale(pygame.image.load(self.ani[0]), (50, 52))

            self.sit = 1
            self.rect = pygame.rect.Rect((last.x, last.y + 50), self.image.get_size())

        # jumping
        key = pygame.key.get_pressed()
        if self.resting and key[pygame.K_SPACE] and self.sit == 0:
            game.jump.play()
            self.dy = -450

        self.dy = min(400, self.dy + 40)
        self.rect.y += self.dy * dt

        new = self.rect
        self.resting = False

        # lookup tilemap triggers
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            blockers = cell['blockers']
            if blockers != "end":
                if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                    new.right = cell.left
                if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                    new.left = cell.right
                if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                    self.resting = True
                    new.bottom = cell.top
                    self.dy = 0
                if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                    new.top = cell.bottom
                    self.dy = 0
            elif blockers == "end" and self.zombie_kill == game.zombie_count:
                self.level_end = 1
        game.tilemap.set_focus(new.x, new.y)
