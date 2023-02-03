import uuid
from typing import Tuple, Union, Dict, Any

import networkx as nx
import pygame

from gameConstants import ColourConstants, DimensionConstants
from managers.connectionManager.connectionObj import ConnectionObj
from managers.folderManager.folderObj import FolderObj, ScriptObj


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

    def createPygameObj(self):
        pass

    def refresh(self):
        pass

    def draw(self, session):
        rect = pygame.Rect(self.center[0] - self.width / 2,
                           self.center[1] - self.width / 2,
                           self.shape[0],
                           self.shape[1])

        pygame.draw.rect(session, self.colour, rect, 0, border_radius=2)
        pygame.draw.rect(session, self.border_colour, rect, width=self.width, border_radius=2)

    def updatePos(self, pos: Tuple[int, float], levels: int):
        self.center = ((pos[0] + 1) * DimensionConstants.WIN_HEIGHT * DimensionConstants.SQUAREUNIT / (levels + 1),
                       pos[1] * DimensionConstants.WIN_WIDTH * DimensionConstants.SQUAREUNIT)


class DisplayConnection:
    id: uuid = None
    mnemeSelf: ConnectionObj = None
    sourceBlock: DisplayBlock = None
    targetBlock: DisplayBlock = None
    sourceLoc: Tuple = (0, 0)
    targetLoc: Tuple = (0, 0)

    def createPygameObj(self):
        pass

    def refresh(self):
        pass

    def draw(self, session):
        print(self.id)


class DisplayNetwork:
    graph: nx.DiGraph = None

    def createGraph(self, connectionDict: Dict[str, ConnectionObj], scriptDict: Dict[str, Any]) -> None:
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(scriptDict.keys())
        self.graph.add_edges_from(
            [(connection.sourceScriptID, connection.targetScriptID)
             for connection in connectionDict.values()]
        )
