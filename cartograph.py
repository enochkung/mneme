import numpy as np
import pygame

from gameConstants import ColourConstants
from mneme import MneScript
from typing import List, Dict


class CtgScript:
    def __init__(self, mneScript, pos=(0, 0), dim=(20, 30)):
        self.mneScript = mneScript
        self.pos = np.array(pos)
        self.shape = dim
        self.colour = ColourConstants.WHITE
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.shape[0], self.shape[1])


class CtgConnection:
    def __init__(self, sourceScript, targetScript):
        self.source_object = sourceScript
        self.target_object = targetScript
        self.colour = ColourConstants.WHITE


class Cartograph:
    def __init__(self, session):
        self.current_filter = None
        self.session = session
        self.mne_objects = list()
        self.ctgScripts: Dict[str, CtgScript] = dict()
        self.ctgConnections: List[CtgConnection] = list()

    def initialise_display_objects(self, mneObjects: List[MneScript]) -> None:
        """
        mneObjects contain list of imports
        :param mneObjects:
        :return:
        """
        self.mne_objects = mneObjects
        self.initialise_scripts()
        self.initialise_connections()
        self.display_initialised_objects()

    def initialise_scripts(self):
        for mneScript in self.mne_objects:
            self.ctgScripts[mneScript.script_name] = CtgScript(mneScript)

    def initialise_connections(self):
        for mneScript in self.mne_objects:
            for mneImport in mneScript.imports:
                self.ctgConnections.append(
                    CtgConnection(self.ctgScripts[mneImport.import_script_name],
                                  self.ctgScripts[mneImport.current_script_name])
                )

    def display_initialised_objects(self):
        for script in self.ctgScripts.values():
            self.draw_script(script)

        for connection in self.ctgConnections:
            self.draw_connection(connection)

    def draw_script(self, script: CtgScript):
        pygame.draw.rect(self.session, script.colour, script.rect)

    def draw_connection(self, connection):
        pygame.draw.line(self.session, connection.colour, connection.source_object.pos, connection.target_object.pos,
                         width=2)

    def get_connection_by_filter(self, filter):
        pass

    def get_inputs_for_pygame(self):
        pass
