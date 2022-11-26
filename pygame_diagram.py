import numpy as np
import pygame

from cartograph import Cartograph
from gameConstants import ColourConstants
from mneme import Mneme
import os

from utils import center_screen_conversion

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
                continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                ctg.select_obj(pos)
            if event.type == pygame.MOUSEMOTION and ctg.selected_obj is not None:
                pos = pygame.mouse.get_pos()
                ctg.selected_obj.set_center(
                    np.array(center_screen_conversion(pos)) - np.array(ctg.selected_obj.relative_pos)
                )
                scr.fill(ColourConstants.BACKGROUND)
                ctg.set_grid()
                ctg.display_objects()
            if event.type == pygame.MOUSEBUTTONUP:
                ctg.selected_obj = None
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                scr.fill(ColourConstants.BACKGROUND)
                ctg.reset()
        pygame.display.update()
        # Update diagram

    pygame.display.flip()
