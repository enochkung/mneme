import sys

import pygame
import time


class InputManager:
    def __init__(self):
        self.last_click = 0
        self.clickTrigger = False
        self.rectangles = []

    def singleClick(self, pos):
        print(f"Single click at position: {pos}")

    def doubleClick(self, pos):
        print(f"Double click at position: {pos}")

    def runQuit(self):
        pygame.quit()
        sys.exit()

    def createRect(self):
        rect = pygame.Rect(50, 50, 100, 100)
        fill_color = (0, 0, 255)  # blue
        border_color = (128, 128, 128)  # grey
        border_width = 2
        rectangle = Rectangle(rect, fill_color, border_color, border_width)
        self.rectangles.append(rectangle)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.runQuit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.runQuit()
                elif event.key == pygame.K_g:
                    self.createRect()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                current_time = time.time()
                if current_time - self.last_click < 0.5 and self.clickTrigger:
                    self.doubleClick(pos)
                    self.clickTrigger = False
                else:
                    self.clickTrigger = True
                    self.last_click = current_time
                    pygame.time.set_timer(pygame.USEREVENT, 700)
            if event.type == pygame.USEREVENT:
                if self.clickTrigger:
                    self.singleClick(pygame.mouse.get_pos())
                    self.clickTrigger = False


class GUIBase:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.input_manager = InputManager()

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            for rectangle in self.input_manager.rectangles:
                rectangle.draw(self.screen)
            self.input_manager.processInput()
            pygame.display.update()
        # pygame.quit()


class Rectangle:
    def __init__(self, rect, fill_color, border_color, hover_color, border_width=0):
        self.rect = rect
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_width = border_width
        self.hover = False
        self.hover_color = hover_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width)
        pygame.draw.rect(screen, self.fill_color, self.rect.inflate(-self.border_width*2, -self.border_width*2))


if __name__ == "__main__":
    gui = GUIBase(1500, 900)
    gui.run()
