import os
import time
from typing import Union

import numpy as np
import pygame

from cartograph import Cartograph
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
        self.mouse_up_time = time.time()
        self.mouse_down_time = time.time()

    def run_main(self):
        self.setup_pygame()
        self.setup_mneme()
        self.setup_cartograph()
        self.run_loop_by_event()
        # self.run_loop()

    def run_loop_by_event(self):
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
            self.ctg.draw_input_text()
        if event.key == pygame.K_r:
            self.refresh_mneme_ctg()

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
            if obj is not None and obj != self.ctg.selected_obj:
                self.ctg.reset_selected_obj()
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

    # def run_loop(self):
    #     done = False
    #     while not done:
    #         for event in pygame.event.get():
    #             if event.type == pygame.KEYDOWN:
    #                 self.check_reset(event)
    #             done = self.check_quit(event)
    #             if done:
    #                 break
    #             self.check_mouse(event)
    #             self.check_key(event)
    #
    #         pygame.display.update()
    #     # Update diagram
    #     pygame.display.flip()

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

    # def check_reset(self, event):
    #     if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
    #         self.main_scr.fill(ColourConstants.BACKGROUND)
    #         self.ctg.reset()
    #
    # @staticmethod
    # def check_quit(event):
    #     if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
    #         return True
    #     return False
    #
    # def check_mouse(self, event):
    #     self.check_mouse_hover()
    #     if self.ctg.selected_obj is not None:
    #         self.check_mouse_selected(event)
    #     else:
    #         self.check_mouse_unselected(event)
    #     self.check_open_script(event)
    #
    # def check_key(self, event):
    #     if event.type != pygame.KEYDOWN:
    #         return
    #     if event.key == pygame.K_n:
    #         self.ctg.draw_input_text()
    #     if event.key == pygame.K_r:
    #         self.refresh_mneme_ctg()
    #
    # def check_mouse_selected(self, event):
    #     """
    #     1. if click outside of selected, then selected becomes whatever is clicked
    #     2. if click inside of selected and drag mouse, then selected is drag and ends still selected
    #     3. otherwise, de-select
    #     :param event:
    #     :return:
    #     """
    #     pos = pygame.mouse.get_pos()
    #     obj = self.ctg.get_object_from_mouse_pos(pos, screen_pos=True)
    #
    #     if event.type == pygame.MOUSEBUTTONUP:
    #         # if now and previous mouse up time is too close, then it was a double click
    #         # if now and previous mouse up time is too far apart, then it was single click
    #         time_diff = mouse_time_diff(time.time(), self.mouse_up_time)
    #         if time_diff > 500 > mouse_time_diff(time.time(), self.mouse_down_time):
    #             # simple single click case
    #             self.ctg.unhighlight_object(hover=False)
    #             self.ctg.reset_selected_obj()
    #             print('mouse up')
    #             if obj is not None:
    #                 self.ctg.select_obj(pos, screen_pos=True)
    #                 self.ctg.highlight_object(hover=False)
    #         self.mouse_up = True
    #         self.mouse_up = time.time()
    #     elif event.type == pygame.MOUSEMOTION and not self.mouse_up:
    #         self.move_obj(event)
    #     elif event.type == pygame.MOUSEBUTTONDOWN and self.mouse_up:
    #         print('another one')
    #     # if not self.mouse_up: #event.type == pygame.MOUSEBUTTONDOWN: # and self.clock.tick() > 500:
    #     #     """
    #     #     1. If obj is the same or obj is None, then unhighlight and reset selected obj
    #     #     2. If obj is different, then unhighlight, change selected obj and highlight
    #     #     """
    #     #     self.clock.tick()
    #     #     if obj == self.ctg.selected_obj or obj is None:
    #     #         self.ctg.reset_selected_obj()
    #     #         return
    #     #     if obj != self.ctg.selected_obj:
    #     #         self.ctg.reset_selected_obj()
    #     #         self.ctg.select_obj(pos=pos, screen_pos=True)
    #     #         self.ctg.highlight_object(hover=False)
    #     # if event.type == pygame.MOUSEMOTION and not self.mouse_up:
    #     #     self.move_obj(event)
    #     # if event.type == pygame.MOUSEBUTTONUP:
    #     #     self.mouse_up = True
    #
    # def check_mouse_unselected(self, event):
    #     pos = pygame.mouse.get_pos()
    #     obj = self.ctg.get_object_from_mouse_pos(pos, screen_pos=True)
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         """
    #         Nothing else is selected, so we highlight and set to selected_obj
    #         """
    #         self.mouse_up = False
    #         self.mouse_down_time = time.time()
    #         if obj is not None:
    #             self.ctg.select_obj(pos, screen_pos=True)
    #             print('selected obj: ', self.ctg.selected_obj)
    #             self.ctg.highlight_object(hover=False)
    #
    # def check_mouse_hover(self):
    #     pos = pygame.mouse.get_pos()
    #     obj = self.ctg.get_object_from_mouse_pos(pos, screen_pos=True)
    #     if obj is not None:
    #         self.ctg.hover_obj(pos=pos, screen_pos=True)
    #         self.ctg.highlight_object(hover=True)
    #     if obj is None and self.ctg.hovered_obj is not None and self.ctg.hovered_obj != self.ctg.selected_obj:
    #         self.ctg.unhighlight_object(hover=True)
    #         self.ctg.reset_hovered_obj()
    #
    # def check_open_script(self, event):
    #     pos = pygame.mouse.get_pos()
    #     obj = self.ctg.get_object_from_mouse_pos(pos, screen_pos=True)
    #     if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.ctg.selected_obj:
    #         #event.type == pygame.MOUSEBUTTONUP and self.clock.tick() < MouseConstants.DOUBLE_CLICK_TIME and obj is not None:
    #         print('opening code')
    #         self.ctg.draw_input_text(object=self.ctg.selected_obj)

    def move_obj(self):
        pos = pygame.mouse.get_pos()
        self.ctg.selected_obj.set_center(
            np.array(center_screen_conversion(pos)) - np.array(self.ctg.selected_obj.relative_pos)
        )
        self.main_scr.fill(ColourConstants.BACKGROUND)
        self.ctg.set_grid()
        self.ctg.display_objects()

    def refresh_mneme_ctg(self):
        self.setup_mneme()
        self.setup_cartograph()


if __name__ == '__main__':
    PyGameDisplay().run_main()
