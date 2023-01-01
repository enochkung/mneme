import time
from typing import Tuple

import numpy as np


def center_screen_conversion(pos: np.array) -> np.array:
    return np.array([pos[0], 900 - pos[1]])


def mouse_time_diff(time1: float, time2: float) -> float:
    """ retrun in milliseconds"""
    return (time1 - time2) * 1000


def mouse_time_diff_now(old_time: float) -> float:
    return mouse_time_diff(time.time(), old_time)
