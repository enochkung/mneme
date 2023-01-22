import time

import numpy as np
import pygame

from utils import getMousePos, isQuit, isKey, isMouse


class InputManager:
    mouseDown: bool = False
    mouseUp: bool = True
    firstClick: bool = False
    lastMouseDownTime: float = 0.0
    lastMouseUpTime: float = 0.0
    displayManager = None

    def __init__(self, _displayManager):
        self.displayManager = _displayManager

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
        pos = getMousePos()
        print('single click', pos)

    def runDoubleClick(self):
        pos = getMousePos()
        print('double click', pos)

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