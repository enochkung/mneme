import os
import time
from typing import Union

import numpy as np
import pygame

from cartograph import Cartograph, CtgScript
from gameConstants import ColourConstants, DimensionConstants
from mneme import Mneme
from utils import center_screen_conversion, mouse_time_diff, mouse_time_diff_now


class PyGameDisplay:
    def __init__(self):
        self.mneme = None
        self.main_scr = None
        self.surface = None
        self.aux_menus = None
        self.ctg = None
        self.runloop = True
        self.clock = pygame.time.Clock()
        self.mouse_up = True
        self.key_up = True
        self.mouse_up_time = time.time()
        self.mouse_down_time = time.time()
        self.key_down_time = time.time()

    def run_main(self):
        self.setup_pygame()
        self.setup_mneme()
        self.setup_cartograph()
        self.run_loop()

    def run_loop(self):
        while self.runloop:
            for event in pygame.event.get():
                self.event_reader(event)
            pygame.display.update()
        # Update diagram
        pygame.display.flip()

    def event_reader(self, event) -> None:
        if event.type == pygame.QUIT:
            self.runloop = False
        if event.type == pygame.KEYDOWN:
            self.run_action_by_key(event)
        if event.type == pygame.MOUSEBUTTONUP:
            self.run_action_mouse_up(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.run_action_mouse_down(event)
        if event.type == pygame.MOUSEMOTION:
            self.run_action_mouse_motion(event)

    def run_action_by_key(self, event):
        if event.key == pygame.K_q:
            self.runloop = False
        if event.key == pygame.K_n:
            self.new_script_rect_placement()
            self.ctg.create_new_script()
            self.main_scr.fill(ColourConstants.BACKGROUND)
            self.ctg.set_grid()
            self.ctg.display_objects()
        if event.key == pygame.K_r:
            self.refresh_mneme_ctg()
        if event.key == pygame.K_DELETE and isinstance(self.ctg.selected_obj, CtgScript):
            del self.ctg.ctgScripts[self.ctg.selected_obj.mneScript.script_name]
            self.ctg.reset_selected_obj()
            self.screen_scripts_update()

    def run_action_mouse_up(self, event):
        """
        1. If nothing selected and obj is not None, then select object
        :param event:
        :return:
        """
        pos = pygame.mouse.get_pos()
        obj = self.ctg.get_object_from_mouse_pos(pos, screen_pos=True)
        mouse_up_time = time.time()

        if self.ctg.selected_obj is None and obj is not None:
            self.ctg.select_obj(pos, screen_pos=True)
            self.ctg.highlight_object(hover=False)

        elif self.ctg.selected_obj is not None:
            if obj == self.ctg.selected_obj and mouse_time_diff(mouse_up_time, self.mouse_up_time) < 400:
                self.ctg.draw_input_text(object=self.ctg.selected_obj)
            elif obj == self.ctg.selected_obj and mouse_time_diff(mouse_up_time, self.mouse_down_time) < 200:
                self.ctg.reset_selected_obj()

        self.mouse_up_time = mouse_up_time
        self.mouse_up = True

    def run_action_mouse_down(self, event):
        """
        1. If nothing is selected, then just register mouse down.
        2. If something is selected and clicked something else, then reset selected obj.
        :param event:
        :return:
        """

        if self.ctg.selected_obj is not None:
            pos = pygame.mouse.get_pos()
            obj = self.ctg.get_object_from_mouse_pos(pos, screen_pos=True)
            time_mark = time.time()
            if (obj is not None and obj != self.ctg.selected_obj) or obj is None:
                self.ctg.reset_selected_obj()
            else:
                print(mouse_time_diff(time_mark, self.mouse_up_time))
        self.mouse_down_time = time.time()
        self.mouse_up = False

    def run_action_mouse_motion(self, event):
        """
        1. If mouse is down and selected obj exist then drag
        2. Check hover
        :param event:
        :return:
        """
        pos = pygame.mouse.get_pos()
        obj = self.ctg.get_object_from_mouse_pos(pos, screen_pos=True)
        if not self.mouse_up and self.ctg.selected_obj is None and \
                mouse_time_diff(time.time(), self.mouse_down_time) > 20 and obj is not None:
            self.ctg.select_obj(pos, screen_pos=True)
            self.ctg.highlight_object(hover=False)

        if self.mouse_up:
            self.check_hover(pos, obj)
            return
        if not self.mouse_up and self.ctg.selected_obj is not None:
            self.move_obj()

    def check_hover(self, pos, obj):
        if obj is None:
            if self.ctg.hovered_obj is not None:
                self.ctg.reset_hovered_obj()
            return
        self.ctg.hover_obj(pos, screen_pos=True)
        self.ctg.highlight_object(hover=True)

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

    def move_obj(self):
        pos = pygame.mouse.get_pos()
        self.ctg.selected_obj.set_center(
            np.array(center_screen_conversion(pos)) - np.array(self.ctg.selected_obj.relative_pos)
        )
        self.main_scr.fill(ColourConstants.BACKGROUND)
        self.ctg.set_grid()
        self.ctg.display_objects()

    def new_script_rect_placement(self):
        set_new_script = True
        self.ctg.potential_obj = None
        while set_new_script:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    self.ctg.ctgPotentialScripts = list()
                    self.ctg.potential_obj = None
                    set_new_script = False
                    break
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_up_time = time.time()
                    self.mouse_up = True
                    set_new_script = False
                    break
                if event.type == pygame.MOUSEMOTION and self.ctg.potential_obj is not None:
                    self.move_potential_script(self.ctg.potential_obj)
                if self.ctg.potential_obj is None:
                    self.create_potential_script()
            pygame.display.update()

    def create_potential_script(self):
        return self.ctg.create_potential_script()

    def move_potential_script(self, potential_script):
        pos = pygame.mouse.get_pos()
        potential_script.set_center(
            np.array(center_screen_conversion(pos)) - np.array(potential_script.relative_pos)
        )
        self.main_scr.fill(ColourConstants.BACKGROUND)
        self.ctg.set_grid()
        self.ctg.display_objects()

    def refresh_mneme_ctg(self):
        self.setup_mneme()
        self.setup_cartograph()

    def screen_scripts_update(self):
        self.main_scr.fill(ColourConstants.BACKGROUND)
        self.ctg.set_grid()
        self.ctg.display_objects()


if __name__ == '__main__':
    PyGameDisplay().run_main()
