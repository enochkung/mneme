import time

import numpy as np
import pygame


def center_screen_conversion(pos: np.array) -> np.array:
    return np.array([pos[0], 900 - pos[1]])


def mouse_time_diff(time1: float, time2: float) -> float:
    """ retrun in milliseconds"""
    return (time1 - time2) * 1000


def mouse_time_diff_now(old_time: float) -> float:
    return mouse_time_diff(time.time(), old_time)


def isQuit(event) -> bool:
    return event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q)


def isKey(event) -> bool:
    return event.type == pygame.KEYDOWN or event.type == pygame.KEYUP


def isMouse(event) -> bool:
    return event.type == pygame.MOUSEBUTTONUP or \
           event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION
