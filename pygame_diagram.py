import numpy as np
import pygame

from cartograph import Cartograph
from gameConstants import ColourConstants, DimensionConstants
from mneme import Mneme
import os

from utils import center_screen_conversion


class PyGameDisplay:
    def __init__(self):
        self.mneme = None
        self.main_scr = None
        self.surface = None
        self.aux_menus = None
        self.ctg = None
        self.clock = pygame.time.Clock()
        self.mouse_up = True

    def run_main(self):
        self.setup_mneme()
        self.setup_pygame()
        self.setup_cartograph()
        self.run_loop()

    def run_loop(self):
        done = False
        while not done:
            for event in pygame.event.get():
                self.check_reset(event)
                done = self.check_quit(event)
                if done:
                    break
                self.check_mouse(event)

                # self.check_motion(event)
                # self.check_aux_menus(event)

                # self.check_highlight()

            pygame.display.update()
        # Update diagram
        pygame.display.flip()

    def setup_mneme(self):
        root_dir = os.getcwd() + '\\' + 'test_folder'
        self.mneme = Mneme()
        self.mneme.directory_reader(root_dir)
        self.mneme.object_log()

    def setup_pygame(self):
        pygame.init()
        self.main_scr = pygame.display.set_mode((DimensionConstants.WIN_WIDTH, DimensionConstants.WIN_HEIGHT),
                                                pygame.RESIZABLE)
        self.main_scr.fill(ColourConstants.BACKGROUND)
        pygame.display.set_caption('MnemeV1')

    def setup_cartograph(self):
        self.ctg = Cartograph(self.main_scr, self.mneme)
        self.ctg.initialise_display_objects(self.mneme.scripts)

    def check_reset(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.main_scr.fill(ColourConstants.BACKGROUND)
            self.ctg.reset()

    @staticmethod
    def check_quit(event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            return True
        return False

    def check_mouse(self, event):
        self.check_mouse_hover()
        if self.ctg.selected_obj is not None:
            self.check_mouse_selected(event)
            return
        self.check_mouse_unselected(event)

    def check_mouse_selected(self, event):
        """
        1. if click outside of selected, then selected becomes whatever is clicked
        2. if click inside of selected and drag mouse, then selected is drag and ends still selected
        3. otherwise, de-select
        :param event:
        :return:
        """

    def check_mouse_unselected(self, event):
        pass

    def check_mouse_hover(self):
        pos = pygame.mouse.get_pos()
        obj = self.ctg.get_object_from_mouse_pos(pos, screen_pos=True)
        if obj is not None:
            self.ctg.hover_obj(pos=pos, screen_pos=True)
            self.ctg.highlight_object(hover=True)
        if obj is None and self.ctg.hovered_obj is not None:
            self.ctg.unhighlight_object(hover=True)
            self.ctg.hovered_obj = None

    def check_motion(self, event):
        self.check_mouse_down(event)
        self.check_mouse_motion(event)
        self.check_mouse_up(event)

    def check_mouse_down(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.clock.tick() > 500:
                pos = pygame.mouse.get_pos()
                self.ctg.select_obj(pos)
            else:
                pos = pygame.mouse.get_pos()
                self.ctg.select_obj(pos)
                if self.ctg.selected_obj is not None and self.ctg.selected_obj.in_pos(center_screen_conversion(pos)):
                    self.ctg.draw_input_text(object=self.ctg.selected_obj)

    def check_mouse_motion(self, event):
        if event.type == pygame.MOUSEMOTION and self.ctg.selected_obj is not None:
            pos = pygame.mouse.get_pos()
            self.ctg.selected_obj.set_center(
                np.array(center_screen_conversion(pos)) - np.array(self.ctg.selected_obj.relative_pos)
            )
            self.main_scr.fill(ColourConstants.BACKGROUND)
            self.ctg.set_grid()
            self.ctg.display_objects()

    def check_mouse_up(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if self.ctg.selected_obj is not None:
                self.ctg.selected_obj = None

    def check_highlight(self):
        pos = pygame.mouse.get_pos()
        if self.ctg.selected_obj is not None and not self.ctg.selected_obj.in_pos(center_screen_conversion(pos)):
            self.ctg.unhighlight_object()
            self.ctg.selected_obj = None

        self.ctg.select_obj(pos)
        if self.ctg.selected_obj is not None:
            self.ctg.highlight_object()
            self.ctg.selected_obj = None

    def check_aux_menus(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h and not self.ctg.inputTextPressed:
            self.ctg.draw_input_text()


if __name__ == '__main__':
    PyGameDisplay().run_main()
