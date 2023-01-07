import time

import numpy as np
import pygame

from gameConstants import DimensionConstants, ColourConstants
from utils import isQuit, isKey, isMouse


class Mneme:
    run: bool = True
    inputManager = None
    displayManager = None
    folderManager = None
    mainScr = None

    def main(self):
        self.runPygame()

    def runPygame(self):
        self.setup()
        while self.run:
            self.interpretInput()
            self.updatingDisplay()

    def setup(self):
        self.setupManagers()
        self.setupDisplay()

    def setupManagers(self):
        self.inputManager = InputManager()

    def setupDisplay(self):
        self.displayManager = DisplayManager()
        self.displayManager.setup()

    def interpretInput(self) -> None:
        self.run = self.inputManager.interpretInput()

    def updatingDisplay(self) -> None:
        self.displayManager.drawGrid()
        self.displayManager.update()

    def gridBackground(self):
        self.displayManager.drawGrid()


class InputManager:
    mouseDown: bool = False
    mouseUp: bool = True
    firstClick: bool = False
    lastMouseDownTime: float = 0.0
    lastMouseUpTime: float = 0.0

    def interpretInput(self) -> bool:
        output = True
        for event in pygame.event.get():
            if isQuit(event):
                # quit
                output = False
            elif isKey(event):
                output = self.interpretKey(event)
            elif isMouse(event):
                output = self.interpretMouse(event)
        if not pygame.event.get() and self.firstClick:
            self.isSingleClick()
        return output

    def interpretKey(self, event):
        if event.key == pygame.K_n:
            # create new block
            print('pressed n')
        elif event.key == pygame.K_r:
            # refresh block positions
            print('pressed r')
        elif event.key == pygame.K_DELETE:
            # remove selected block or connection
            print('pressed delete')
        return True

    def interpretMouse(self, event):
        timeMark = time.time()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.firstClick:
                self.firstClick = True
            elif self.timeLastButtonDown(timeMark) < 200:
                self.firstClick = False
                self.runDoubleClick()
            self.mouseDown = True
            self.lastMouseDownTime = timeMark
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouseDown = False
            self.lastMouseUpTime = timeMark

        return True

    def isSingleClick(self) -> bool:
        timeMark = time.time()
        if not self.mouseDown and self.firstClick and self.timeLastButtonUp(timeMark) > 200:
            self.firstClick = False
            self.runSingleClick()
        return True

    def runSingleClick(self):
        print('single click')

    def runDoubleClick(self):
        print('double click')

    def printTestState(self):
        print('firstClick: ', self.firstClick)
        print('mouseDown: ', self.mouseDown)
        print('lastMouseDownTime: ', self.lastMouseDownTime)
        print('lastMouseUp: ', self.lastMouseUpTime)
        print('current time: ', time.time())

    def timeLastButtonDown(self, timeMark):
        return np.abs(timeMark - self.lastMouseDownTime) * 1000

    def timeLastButtonUp(self, timeMark):
        return np.abs(timeMark - self.lastMouseUpTime) * 1000


class DisplayManager:
    session = None
    mainScr = None

    def setup(self):
        pygame.init()
        self.mainScr = pygame.display.set_mode((DimensionConstants.WIN_WIDTH, DimensionConstants.WIN_HEIGHT),
                                               pygame.RESIZABLE)
        self.mainScr.fill(ColourConstants.BACKGROUND)
        pygame.display.set_caption('MnemeV2')

    def drawGrid(self):
        for i in range(16):
            pygame.draw.line(self.mainScr, ColourConstants.GREY, (i * DimensionConstants.SQUAREUNIT, 0),
                             (i * DimensionConstants.SQUAREUNIT, DimensionConstants.HEIGHT))
            pygame.draw.line(self.mainScr, ColourConstants.GREY, (0, i * DimensionConstants.SQUAREUNIT),
                             (DimensionConstants.WIDTH, i * DimensionConstants.SQUAREUNIT))

    @staticmethod
    def update():
        pygame.display.update()


def main():
    Mneme().main()
