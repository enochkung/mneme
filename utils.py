from typing import Tuple

import numpy as np


def center_to_screen_coord(pos: np.array) -> np.array:
    return np.array([pos[0], 900 - pos[1]])
