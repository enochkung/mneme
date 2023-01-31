import uuid
from typing import List, Dict, Any

import pygame

from Cartographer.cartographer import Cartographer
from gameConstants import ColourConstants, DimensionConstants
from managers.connectionManager.connectionObj import ConnectionObj
from managers.displayManager.displayObject import DisplayNetwork, DisplayConnection, DisplayBlock
from managers.folderManager.folderObj import ScriptObj


class DisplayManager:
    session = None
    mainScr = None
    Blocks: Dict[str, DisplayBlock] = dict()
    Connections: Dict[str, DisplayConnection] = dict()
    graph: DisplayNetwork = None
    cartographer: Cartographer = Cartographer()

    def __init__(self, connectionDict: Dict[str, ConnectionObj], scriptDict: Dict[str, ScriptObj]):
        self.createDisplayObjs(connectionDict, scriptDict)
        DisplayNetwork().createGraph(connectionDict, scriptDict)

    def createDisplayObjs(self, connectionDict: Dict[str, ConnectionObj], scriptDict: Dict[str, ScriptObj]):
        self.createScriptObjs(scriptDict)
        self.createConnectionObjs(connectionDict)

    def createScriptObjs(self, scriptDict: Dict[str, ScriptObj]):
        for blockID, block in scriptDict.items():
            displayBlock = DisplayBlock()
            displayBlock.id = blockID
            displayBlock.mnemeSelf = block
            displayBlock.level = block.level
            self.Blocks[blockID] = displayBlock

    def createConnectionObjs(self, connectionDict: Dict[str, ConnectionObj]):
        for connectionID, connection in connectionDict.items():
            displayConnection = DisplayConnection()
            displayConnection.id = connectionID
            displayConnection.sourceID = connection.sourceScriptID
            displayConnection.sourceBlock = self.Blocks[displayConnection.sourceID]
            displayConnection.targetID = connection.targetScriptID
            displayConnection.targetBlock = self.Blocks[displayConnection.targetID]
            displayConnection.mnemeSelf = connection
            self.Connections[connectionID] = displayConnection

    def initialise(self):
        self.drawObjects()
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

    def drawObjects(self):
        self.autosetObjLoc()
        self.drawConnections()
        self.drawBlocks()

    def autosetObjLoc(self):
        """
        Mneme has own setting for block locations. It will also allow user to drag and reposition
        but a reset will reposition blocks back to the Mneme preset method.

        1. For each script, set their "level" depending on the directory.
            - require lowest and highest level
            - split the entire screen to evenly space levels
        2. Depending on level, set block spacing
        3. Connect blocks optimally
        :return:
        """
        self.cartographer.autosetBlockAndConnections(self.Blocks, self.Connections)

    def drawBlocks(self):
        for block in self.Blocks.values():
            block.draw()

    def drawConnections(self):
        for connection in self.Connections.values():
            connection.draw()

    @staticmethod
    def update():
        pygame.display.update()
