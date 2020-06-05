import pygame
import tmx
from .Zombie import Zombie
from .Gun import Gun
from .Player import Player
from .Health import Health
from .Spike import Spike
from .Boss import Boss

class Game(object):
    def intro(self, screen):
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 20)
        white = (255, 255, 255)
        black = (0, 0, 0)
        screen.fill(white)
        text1 = font.render("Controls :", 1, black)
        text2 = font.render("1. Use arrow keys to move the player.", 1, black)
        text3 = font.render("2. Press spacebar to jump.", 1, black)
        text4 = font.render("3. Press b key to fire bullets.", 1, black)
        screen.blit(text1, (300, 15))
        screen.blit(text2, (300, 30))
        screen.blit(text3, (300, 50))
        screen.blit(text4, (300, 70))
        blue = (0, 0, 255)
        ask = font.render("Press p to play else q to quit.", 1, blue)
        screen.blit(ask, (300, 100))
        pygame.display.flip()
        global event
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        return 1
                    elif event.key == pygame.K_q:
                        return 0
            clock.tick(5)

    def decision(self, screen, value):
        clock = pygame.time.Clock()
        white = (255, 255, 255)
        green = (0, 255, 0)
        red = (255, 0, 0)
        blue = (0, 0, 255)
        font = pygame.font.Font(None, 20)
        black = (0, 0, 0)
        screen.fill(white)
        if value == "dead":
            text = font.render("You are Killed.", 1, red)
            screen.blit(text, (300, 15))
        elif value == "you win":
            text = font.render("You Killed the final Boss. Congratulations.", 1, green)
            screen.blit(text, (300, 15))
        ask = font.render("Press p to play again else q to quit the game.", 1, blue)
        screen.blit(ask, (300, 100))
        pygame.display.flip()
        while 1:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return 0
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_p:
                        return 1
                    elif e.key == pygame.K_q:
                        return 0
            clock.tick(5)

    def main(self, screen, level):
        clock = pygame.time.Clock()
        self.level = level
        if self.level == 1:
            filename = "layer1.tmx"
        elif self.level == 2:
            filename = "layer2.tmx"
        elif self.level == 3:
            filename = "layer3.tmx"
        background = pygame.image.load('background.png')
        self.tilemap = tmx.load(filename, screen.get_size())
        self.sprites = tmx.SpriteLayer()
        self.tilemap.layers.append(self.sprites)
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        self.guns = tmx.SpriteLayer()
        self.tilemap.layers.append(self.guns)
        self.screen = screen
        self.zombie_count = 0

        # add an enemy for each "enemy" trigger in the map
        for gun in self.tilemap.layers['triggers'].find('guns'):
            Gun((gun.px, gun.py), self.guns)

        self.zombies = tmx.SpriteLayer()
        self.tilemap.layers.append(self.zombies)

        for zombie in self.tilemap.layers['triggers'].find('zombie'):
            category = zombie["zombie"]
            zombie_range = zombie["range"]
            zombie_power = int(zombie["power"])
            zombie_damage = float(zombie["damage"])
            zombie_shoot = zombie["can_shoot"]
            Zombie((zombie.px, zombie.py), category, zombie_range, zombie_power, zombie_damage, zombie_shoot,
                   self.zombies)
            self.zombie_count += 1

        self.spikes = tmx.SpriteLayer()
        self.tilemap.layers.append(self.spikes)
        for spike in self.tilemap.layers['triggers'].find('spike'):
            spike_width = spike["width"]
            spike_damage = float(spike["damage"])
            spike_type = spike["spike"]
            Spike((spike.px, spike.py), spike_width, spike_damage, spike_type, self.spikes)

        self.health = tmx.SpriteLayer()
        self.tilemap.layers.append(self.health)
        for life in self.tilemap.layers['triggers'].find('life'):
            life_val = float(life["val"])
            Health((life.px, life.py), life_val, self.health)

        self.bosses = tmx.SpriteLayer()
        self.tilemap.layers.append(self.bosses)

        for boss in self.tilemap.layers['triggers'].find('boss'):
            category = boss["boss"]
            zombie_range = boss["range"]
            zombie_power = int(boss["power"])
            zombie_damage = float(boss["damage"])
            zombie_shoot = boss["can_shoot"]
            boss_object = Boss((boss.px, boss.py), category, zombie_range, zombie_power, zombie_damage, zombie_shoot,
                               self.bosses)
        # sounds
        self.jump = pygame.mixer.Sound('sounds\\jump.wav')
        self.shoot = pygame.mixer.Sound('sounds\\shoot.wav')
        self.boss_shoot = pygame.mixer.Sound('sounds\\boss_shoot.wav')
        global event
        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    return "quit"
            dt = clock.tick(30)
            self.tilemap.update(dt / 1000., self, event)
            screen.blit(background, (0, 0))
            self.tilemap.draw(screen)
            self.player.draw_strength(screen)
            z_count = self.zombie_count - self.player.zombie_kill
            self.player.draw_progress(screen, self.level, z_count)
            if self.level == 3:
                boss_object.boss_health(screen)
                if boss_object.boss_kill == 1:
                    return "you win"
            pygame.display.flip()
            if self.player.level_end == 1:
                return "next_level"

            if self.player.is_dead:
                return "dead"
