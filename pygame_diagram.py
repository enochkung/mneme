import numpy as np
import pygame

from cartograph import Cartograph
from gameConstants import ColourConstants
from mneme import Mneme
import os

from utils import center_screen_conversion


class PyGameDisplay:
    def __init__(self):
        self.mneme = None
        self.scr = None
        self.ctg = None

    def run_main(self):
        self.setup_mneme()
        self.setup_pygame()
        self.setup_cartograph()
        self.run_loop()

    def setup_mneme(self):
        root_dir = os.getcwd() + '\\' + 'test_folder'
        self.mneme = Mneme()
        self.mneme.directory_reader(root_dir)
        self.mneme.object_log()

    def setup_pygame(self):
        pygame.init()
        self.scr = pygame.display.set_mode((1500, 900))
        self.scr.fill(ColourConstants.BACKGROUND)
        pygame.display.set_caption('MnemeV1')

    def setup_cartograph(self):
        self.ctg = Cartograph(self.scr, self.mneme)
        self.ctg.initialise_display_objects(self.mneme.scripts)

    def run_loop(self):
        done = False
        while not done:
            for event in pygame.event.get():
                done = self.check_quit(event)
                if done:
                    break
                self.check_mouse_down(event)
                self.check_mouse_motion(event)
                self.check_mouse_up(event)
                self.check_reset(event)
            pygame.display.update()
        # Update diagram
        pygame.display.flip()

    @staticmethod
    def check_quit(event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            return True
        return False

    def check_mouse_down(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            self.ctg.select_obj(pos)

    def check_mouse_motion(self, event):
        if event.type == pygame.MOUSEMOTION and self.ctg.selected_obj is not None:
            pos = pygame.mouse.get_pos()
            self.ctg.selected_obj.set_center(
                np.array(center_screen_conversion(pos)) - np.array(self.ctg.selected_obj.relative_pos)
            )
            self.scr.fill(ColourConstants.BACKGROUND)
            self.ctg.set_grid()
            self.ctg.display_objects()

    def check_mouse_up(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.ctg.selected_obj = None

    def check_reset(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.scr.fill(ColourConstants.BACKGROUND)
            self.ctg.reset()


if __name__ == '__main__':
    PyGameDisplay().run_main()
