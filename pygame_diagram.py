import pygame

from cartograph import Cartograph
from mneme import Mneme
import os


if __name__ == '__main__':
    mneme = Mneme()
    directory = mneme.directory_reader()

    ctg = Cartograph()

    # -------------- start game -----------------
    pygame.init()
    scr = pygame.display.set_mode((600, 500))
    pygame.display.set_caption('MnemeV1')

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

    pygame.display.flip()
