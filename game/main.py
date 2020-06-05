import pygame
from game.Game import Game

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Zombie Kill')
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)
    ## set initial level
    running = Game().intro(screen)
    level = 1
    ret_val = None
    while running:
        ret_val = Game().main(screen, level)
        if ret_val == "next_level":
            level += 1
        if ret_val == "dead" or ret_val == "you win":
            running = Game().decision(screen, ret_val)
            level = 1
    pygame.quit()
    quit()
