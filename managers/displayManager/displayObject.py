import uuid
from typing import Tuple, Union, Dict, Any, List

import networkx as nx
import pygame

from gameConstants import ColourConstants, DimensionConstants
from managers.connectionManager.connectionObj import ConnectionObj
from managers.folderManager.folderObj import FolderObj, ScriptObj
from utils import flipCoords


class DisplayBlock:
    id: uuid = None
    center: Tuple = (0, 0)
    mnemeSelf: Union[FolderObj, ScriptObj] = None
    shape: Tuple[float, float] = (DimensionConstants.ScriptWidth * DimensionConstants.SQUAREUNIT,
                                  DimensionConstants.ScriptWidth * DimensionConstants.SQUAREUNIT)
    colour: Tuple[int, int, int] = ColourConstants.D_CYAN
    border_colour: Tuple[int, int, int] = ColourConstants.WHITE
    width: int = DimensionConstants.ScriptWidth
    level: int = None
    clicked: bool = False

    def createPygameObj(self):
        pass

    def refresh(self):
        pass

    def draw(self, session):
        rect = pygame.Rect(self.center[1] - self.shape[1] / 2,
                           self.center[0] - self.shape[0] / 2,
                           self.shape[0],
                           self.shape[1])

        pygame.draw.rect(session, self.colour, rect, 0, border_radius=2)
        pygame.draw.rect(session, self.border_colour, rect, width=self.width, border_radius=2)

    def updatePos(self, pos: Tuple[int, float], levels: int):
        self.center = ((pos[0] + 1) * DimensionConstants.WIN_HEIGHT / (levels + 1),
                       pos[1] * DimensionConstants.WIN_WIDTH)

    def isinBlock(self, pos):
        return self.center[1] - self.shape[1] / 2 <= pos[0] <= self.center[1] + self.shape[1] / 2 and \
               self.center[0] - self.shape[0] / 2 <= pos[1] <= self.center[0] + self.shape[0] / 2

    def highlight(self):
        self.width = DimensionConstants.ScriptHighlightWidth

    def dehighlight(self):
        self.width = DimensionConstants.ScriptWidth

    def singleClicked(self):
        if self.clicked:
            self.dehighlight()
        else:
            self.highlight()
        self.clicked = not self.clicked

    def doubleClicked(self):
        self.clicked = True
        self.highlight()

    def recenter(self, pos):
        self.center = pos



class DisplayConnection:
    id: uuid = None
    mnemeSelf: ConnectionObj = None
    sourceBlock: DisplayBlock = None
    targetBlock: DisplayBlock = None
    sourceLoc: Tuple = (0, 0)
    targetLoc: Tuple = (0, 0)
    vertices: List[Tuple[float, float]] = list()
    width: int = DimensionConstants.ConnectionWidth
    colour: Tuple[int, int, int] = ColourConstants.WHITE

    def createPygameObj(self):
        pass

    def refresh(self):
        pass

    def draw(self, session):
        for i in range(len(self.vertices) - 1):
            pygame.draw.line(session, self.colour, self.vertices[i], self.vertices[i+1],
                             width=self.width)

    def updatePos(self, vertices: List[Tuple[float, float]]):
        self.vertices = [flipCoords(pos) for pos in vertices]


class DisplayNetwork:
    graph: nx.DiGraph = None

    def createGraph(self, connectionDict: Dict[str, ConnectionObj], scriptDict: Dict[str, Any]) -> None:
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(scriptDict.keys())
        self.graph.add_edges_from(
            [(connection.sourceScriptID, connection.targetScriptID)
             for connection in connectionDict.values()]
        )
