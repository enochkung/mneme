import pygame

from cartograph import Cartograph
from gameConstants import ColourConstants
from mneme import Mneme
import os


if __name__ == '__main__':
    root_dir = os.getcwd() + '\\' + 'test_folder'
    mneme = Mneme()
    mneme.directory_reader(root_dir)
    mneme.object_log()

    # -------------- start game -----------------
    pygame.init()
    scr = pygame.display.set_mode((1500, 900))
    scr.fill(ColourConstants.BACKGROUND)
    pygame.display.set_caption('MnemeV1')

    ctg = Cartograph(scr, mneme)
    ctg.initialise_display_objects(mneme.scripts)

    # Create initial diagram

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                done = True
        pygame.display.update()
        # Update diagram

    pygame.display.flip()
