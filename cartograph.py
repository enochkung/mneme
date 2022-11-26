from typing import List, Dict, Tuple

import numpy as np
import pygame

from gameConstants import ColourConstants
from mneme import MneScript
from utils import center_screen_conversion


class CtgScript:
    center = None
    screen_center = None
    pos = None
    screen_pos = None
    rect = None
    relative_pos = None

    def __init__(self, mneScript, center=np.array((0, 0)), dim=np.array((100, 100)), colour=ColourConstants.D_CYAN):
        self.mneScript = mneScript
        self.shape = dim
        self.colour = colour
        self.border_colour = ColourConstants.WHITE
        self.set_center(center)

    def get_pos_from_center(self) -> np.array:
        return np.array([self.center[0] - self.shape[0] / 2, self.center[1] + self.shape[1] / 2])

    def draw(self, session):
        pygame.draw.rect(session, self.colour, self.rect, 0)
        pygame.draw.rect(session, self.border_colour, self.rect, 1)

    def set_center(self, center, screen_pos=False):
        self.center = center
        self.screen_center = center_screen_conversion(self.center)
        self.pos = self.get_pos_from_center()
        self.screen_pos = self.pos if screen_pos else center_screen_conversion(self.pos)
        self.rect = pygame.Rect(self.screen_pos[0], self.screen_pos[1], self.shape[0], self.shape[1])

    def in_pos(self, pos):
        return (pos[0] >= self.center[0] - self.shape[0]/2) and (pos[0] <= self.center[0] + self.shape[0]/2) and \
               (pos[1] >= self.center[1] - self.shape[1]/2) and (pos[1] <= self.center[1] + self.shape[1]/2)


class CtgConnection:
    def __init__(self, sourceScript, targetScript):
        self.source_object = sourceScript
        self.target_object = targetScript
        self.colour = ColourConstants.WHITE

    def draw(self, session):
        pygame.draw.line(session, self.colour, self.source_object.screen_center,
                         self.target_object.screen_center, width=2)


class Cartograph:
    def __init__(self, session, mneme):
        self.current_filter = None
        self.session = session
        self.mneme = mneme
        self.mne_objects = list()
        self.selected_obj = None
        self.ctgScripts: Dict[str, CtgScript] = dict()
        self.ctgConnections: List[CtgConnection] = list()
        self.opt_pos: Dict[str, Tuple[float, float]] = dict()

    def set_grid(self):
        for i in range(16):
            pygame.draw.line(self.session, ColourConstants.GREY, (i * 100, 0), (i * 100, 1000))
            pygame.draw.line(self.session, ColourConstants.GREY, (0, i * 100), (1500, i * 100))

    def initialise_display_objects(self, mneObjects: List[MneScript]) -> None:
        """
        mneObjects contain list of imports
        :param mneObjects:
        :return:
        """
        self.set_grid()
        self.mne_objects = mneObjects
        self.optimise_pos()
        self.initialise_scripts()
        self.initialise_connections()
        self.display_objects()

    def initialise_scripts(self):
        for scriptNum, mneScript in enumerate(self.mne_objects):
            self.ctgScripts[mneScript.script_name] = CtgScript(
                mneScript, colour=ColourConstants.COLOUR_LIST[mneScript.level - 1]
            )
            self.ctgScripts[mneScript.script_name].set_center(
                self.opt_pos[mneScript.script_name]
            )

    def initialise_connections(self):
        for mneScript in self.mne_objects:
            for mneImport in mneScript.imports:
                self.ctgConnections.append(
                    CtgConnection(self.ctgScripts[mneImport.import_script_name],
                                  self.ctgScripts[mneImport.current_script_name])
                )

    def display_objects(self):
        for connection in self.ctgConnections:
            self.draw_connection(connection)

        for script in self.ctgScripts.values():
            self.draw_script(script)

    def draw_script(self, script: CtgScript):
        script.draw(self.session)

    def draw_connection(self, connection):
        connection.draw(self.session)

    def optimise_pos(self):
        levels = [mneScript.level for mneScript in self.mne_objects]
        levels.sort()

        divisions = len(set(levels)) + 1
        coord_vert_increment = 900 / divisions
        for level_num, level in enumerate(set(levels)):
            scripts_at_level = [mneScript for mneScript in self.mne_objects if mneScript.level == level]
            horizontal_divisions = len(scripts_at_level) + 1
            coord_hor_increment = 1500 / horizontal_divisions
            for script_num, mneScript in enumerate(scripts_at_level):
                self.opt_pos[mneScript.script_name] = (
                    coord_hor_increment * (script_num + 1), 900 -coord_vert_increment * (level_num + 1)
                )

    def get_object_from_mouse_pos(self, pos):
        ctg_pos = center_screen_conversion(pos)
        for script in self.ctgScripts.values():
            if script.in_pos(ctg_pos):
                return script
        return

    def select_obj(self, pos):
        self.selected_obj = self.get_object_from_mouse_pos(pos)
        if self.selected_obj is not None:
            self.selected_obj.relative_pos = np.array(center_screen_conversion(pos)) - np.array(self.selected_obj.center)

    def reset(self):
        self.set_grid()
        self.optimise_pos()
        self.reset_scripts()
        self.reset_connections()
        self.display_objects()

    def reset_scripts(self):
        for scriptName, script in self.ctgScripts.items():
            script.set_center(self.opt_pos[scriptName])

    def reset_connections(self):
        pass

    def get_connection_by_filter(self, filter):
        pass

    def get_inputs_for_pygame(self):
        pass
