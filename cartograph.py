from tkinter import TOP
from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename
from typing import List, Dict, Tuple, Union

import numpy as np
import pygame

from gameConstants import ColourConstants, DimensionConstants
from main import FileMenu
from mneme import MneScript
from utils import center_screen_conversion

import tkinter as tk
from tkinter.scrolledtext import ScrolledText


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
        self.width = DimensionConstants.ScriptWidth
        self.set_center(center)

    def get_pos_from_center(self) -> np.array:
        return np.array([self.center[0] - self.shape[0] / 2, self.center[1] + self.shape[1] / 2])

    def draw(self, session):
        pygame.draw.rect(session, self.colour, self.rect, 0, border_radius=2)
        pygame.draw.rect(session, self.border_colour, self.rect, width=self.width, border_radius=2)

    def set_center(self, center, screen_pos=False):
        self.center = center
        self.screen_center = center_screen_conversion(self.center)
        self.pos = self.get_pos_from_center()
        self.screen_pos = self.pos if screen_pos else center_screen_conversion(self.pos)
        self.rect = pygame.Rect(self.screen_pos[0], self.screen_pos[1], self.shape[0], self.shape[1])

    def in_pos(self, pos):
        return self.rect.collidepoint(pos)
        # return (pos[0] >= self.center[0] - self.shape[0] / 2) and (pos[0] <= self.center[0] + self.shape[0] / 2) and \
        #        (pos[1] >= self.center[1] - self.shape[1] / 2) and (pos[1] <= self.center[1] + self.shape[1] / 2)

    def highlight(self):
        self.width = DimensionConstants.ScriptHighlightWidth

    def is_highlighted(self):
        return self.width == DimensionConstants.ScriptHighlightWidth


class CtgConnection:
    def __init__(self, sourceScript, targetScript):
        self.source_object = sourceScript
        self.target_object = targetScript
        self.colour = ColourConstants.WHITE
        self.width = DimensionConstants.ConnectionWidth

    def draw(self, session, segments=None):
        source_loc = self.source_object.screen_center
        target_loc = self.target_object.screen_center
        if any(source_loc[i] == target_loc[i] for i in range(2)) and segments is None:
            segments = 1
        else:
            segments = 2

        if segments == 1:
            pygame.draw.line(session, self.colour, source_loc, target_loc, width=self.width)
            return
        if segments == 2:
            pygame.draw.line(session, self.colour, source_loc, (source_loc[0], target_loc[1]), width=self.width)
            pygame.draw.line(session, self.colour, (source_loc[0], target_loc[1]), target_loc, width=self.width)

    def is_highlighted(self):
        return self.width == DimensionConstants.ConnectionHighlightWidth


class CtgTextInput:
    def __init__(self, obj):
        self.obj = obj
        self.shape = (int(DimensionConstants.WIDTH/2), int(DimensionConstants.HEIGHT/2))
        self.input_rect = None
        self.active = False
        self.base_font = None
        self.user_text = 'testing'
        self.tkCompiler = tk.Tk()
        self.tkCompiler.geometry(f'{self.shape[0]}x{self.shape[1]}')
        self.menu_bar = tk.Menu(self.tkCompiler, tearoff=False)
        self.editor = None
        self.save_new_script = False

    def read_script(self, script):
        self.editor = ScrolledText(self.tkCompiler, bg='white', width=self.shape[0], height=self.shape[1])
        self.editor.pack(padx=DimensionConstants.MARGIN, pady=DimensionConstants.MARGIN)
        self.menu_bar.add_command(label='Save', command=self.save)
        self.menu_bar.add_command(label='Save As', command=self.save_as)
        self.tkCompiler.config(menu=self.menu_bar)

        path = script.mneScript.script_name
        with open(path, 'r') as file:
            code = file.read()
            self.editor.delete('1.0', tk.constants.END)
            self.editor.insert('1.0', code)
        self.tkCompiler.mainloop()

    def save(self):
        if self.obj is None:
            self.save_as()
            return
        self.save_as(self.obj.mneScript.script_name)

    def save_as(self, path=None):
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')]) if path is None else path
        with open(path, 'w') as file:
            code = self.editor.get('1.0', tk.END)
            file.write(code)
            self.set_file_path(path)

        if self.obj is None:
            self.save_new_script = True

    def set_file_path(self, path):
        self.editor.file_path = path

    def print_script(self):
        pass

    def create_empty_console(self):
        pass

    def draw(self):
        object = self.obj
        if object is None:
            self.editor = ScrolledText(self.tkCompiler, bg='white', width=self.shape[0], height=self.shape[1])
            self.editor.pack(padx=DimensionConstants.MARGIN, pady=DimensionConstants.MARGIN)
            self.menu_bar.add_command(label='Save', command=self.save)
            self.menu_bar.add_command(label='Save As', command=self.save_as)
            self.tkCompiler.config(menu=self.menu_bar)
            self.tkCompiler.mainloop()

            return
        self.read_script(object)


class CtgPotentialScript:
    center = None
    screen_center = None
    pos = None
    screen_pos = None
    rect = None
    relative_pos = None

    def __init__(self, center=np.array((0, 0)), dim=np.array((100, 100)), colour=ColourConstants.D_CYAN):
        self.colour = colour
        self.shape = dim
        self.center = center
        self.border_colour = ColourConstants.WHITE
        self.width = DimensionConstants.ScriptWidth
        self.set_center(center)

    def draw(self, session):
        pygame.draw.rect(session, self.colour, self.rect, 0, border_radius=2)
        pygame.draw.rect(session, self.border_colour, self.rect, width=self.width, border_radius=2)

    def set_center(self, center, screen_pos=False):
        self.center = center
        self.screen_center = center_screen_conversion(self.center)
        self.pos = self.get_pos_from_center()
        self.screen_pos = self.pos if screen_pos else center_screen_conversion(self.pos)
        self.rect = pygame.Rect(self.screen_pos[0], self.screen_pos[1], self.shape[0], self.shape[1])

    def get_pos_from_center(self) -> np.array:
        return np.array([self.center[0] - self.shape[0] / 2, self.center[1] + self.shape[1] / 2])

    def convert_to_ctgScript(self, text_input: CtgTextInput) -> CtgScript:
        mne_script = MneScript(script_name=text_input.editor.file_path,
                               imports=set(),
                               classes=set(),
                               functions=set())
        return CtgScript(mne_script, center=self.center)


class Cartograph:
    def __init__(self, session, mneme):
        self.current_filter = None
        self.session = session
        self.mneme = mneme
        self.mne_objects = list()
        self.selected_obj = None
        self.hovered_obj = None
        self.potential_obj = None
        self.ctgScripts: Dict[str, CtgScript] = dict()
        self.ctgConnections: List[CtgConnection] = list()
        self.ctgPotentialScripts: List[CtgPotentialScript] = list()
        self.ctgTextInput: CtgTextInput = None
        self.opt_pos: Dict[str, Tuple[float, float]] = dict()

    def set_grid(self):
        for i in range(16):
            pygame.draw.line(self.session, ColourConstants.GREY, (i * DimensionConstants.SQUAREUNIT, 0),
                             (i * DimensionConstants.SQUAREUNIT, DimensionConstants.HEIGHT))
            pygame.draw.line(self.session, ColourConstants.GREY, (0, i * DimensionConstants.SQUAREUNIT),
                             (DimensionConstants.WIDTH, i * DimensionConstants.SQUAREUNIT))

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
        self.initialise_util_buttons()
        self.display_objects()

    def initialise_util_buttons(self):
        pass

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

        for script in self.ctgPotentialScripts:
            self.draw_script(script)

    def draw_script(self, script: Union[CtgScript, CtgPotentialScript]):
        script.draw(self.session)

    def draw_connection(self, connection):
        connection.draw(self.session)

    def optimise_pos(self):
        levels = [mneScript.level for mneScript in self.mne_objects]
        levels.sort()

        divisions = len(set(levels)) + 1
        coord_vert_increment = DimensionConstants.HEIGHT / divisions
        for level_num, level in enumerate(set(levels)):
            scripts_at_level = [mneScript for mneScript in self.mne_objects if mneScript.level == level]
            horizontal_divisions = len(scripts_at_level) + 1
            coord_hor_increment = DimensionConstants.WIDTH / horizontal_divisions
            for script_num, mneScript in enumerate(scripts_at_level):
                self.opt_pos[mneScript.script_name] = (
                    coord_hor_increment * (script_num + 1),
                    DimensionConstants.HEIGHT - coord_vert_increment * (level_num + 1)
                )

    def get_object_from_mouse_pos(self, pos, screen_pos=False):
        ctg_pos = center_screen_conversion(pos) if not screen_pos else pos
        for script in self.ctgScripts.values():
            if script.in_pos(ctg_pos):
                return script
        return

    def select_obj(self, pos, screen_pos=False):
        self.selected_obj = self.get_object_from_mouse_pos(pos, screen_pos=screen_pos)
        if self.selected_obj is not None:
            self.selected_obj.relative_pos = np.array(center_screen_conversion(pos)) - np.array(
                self.selected_obj.center)

    def hover_obj(self, pos=None, screen_pos=False):
        self.hovered_obj = self.get_object_from_mouse_pos(pos, screen_pos=screen_pos)
        if self.hovered_obj is not None:
            self.hovered_obj.relative_pos = np.array(center_screen_conversion(pos)) - np.array(
                self.hovered_obj.center)

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

    def reset_selected_obj(self):
        self.unhighlight_object(hover=False)
        self.selected_obj = None

    def reset_hovered_obj(self):
        self.unhighlight_object(hover=True)
        self.hovered_obj = None

    def get_connection_by_filter(self, filter):
        pass

    def get_inputs_for_pygame(self):
        pass

    def draw_input_text(self, object=None):
        self.ctgTextInput = CtgTextInput(object)
        self.ctgTextInput.draw()
        if self.ctgTextInput.save_new_script:
            new_ctgScript = self.potential_obj.convert_to_ctgScript(self.ctgTextInput)
            self.ctgScripts[new_ctgScript.mneScript.script_name] = new_ctgScript
        self.ctgPotentialScripts = list()
        self.potential_obj = None

    def create_new_script(self):
        self.draw_input_text()

    def highlight_object(self, hover=True):
        obj = self.hovered_obj if hover else self.selected_obj
        obj.width = DimensionConstants.ScriptHighlightWidth if isinstance(obj, CtgScript) \
            else DimensionConstants.ConnectionHighlightWidth
        if isinstance(obj, CtgScript):
            self.draw_script(obj)
        elif isinstance(obj, CtgConnection):
            self.draw_connection(obj)

    def unhighlight_object(self, hover=True):
        if self.hovered_obj == self.selected_obj and hover:
            return
        obj = self.hovered_obj if hover else self.selected_obj
        obj.width = DimensionConstants.ScriptWidth if isinstance(obj, CtgScript) \
            else DimensionConstants.ConnectionWidth
        if isinstance(obj, CtgScript):
            self.draw_script(obj)
        elif isinstance(obj, CtgConnection):
            self.draw_connection(obj)

    def refresh_ctg(self):
        self.initialise_scripts()
        self.initialise_connections()

    def create_potential_script(self):
        pos = pygame.mouse.get_pos()
        self.potential_obj = CtgPotentialScript(center=center_screen_conversion(pos), colour=ColourConstants.SAFFRON)
        self.ctgPotentialScripts.append(self.potential_obj)
        self.potential_obj.draw(self.session)
        self.potential_obj.relative_pos = np.array(center_screen_conversion(pos)) - np.array(
            self.potential_obj.center)
