from typing import List, Dict, Any

import pygame

from gameConstants import ColourConstants, DimensionConstants
from managers.connectionManager.connectionObj import ConnectionObj
from managers.displayManager.displayObject import DisplayNetwork, DisplayConnection, DisplayBlock
from managers.folderManager.folderObj import ScriptObj


class DisplayManager:
    session = None
    mainScr = None
    Blocks: Dict = dict()
    Connections: Dict = dict()
    graph: DisplayNetwork = None

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
            self.Connections[blockID] = displayBlock

    def createConnectionObjs(self, connectionDict: Dict[str, ConnectionObj]):
        for connectionID, connection in connectionDict.items():
            displayConnection = DisplayConnection()
            displayConnection.id = connectionID
            displayConnection.sourceID = connection.sourceScriptID
            displayConnection.targetID = connection.targetScriptID
            displayConnection.mnemeSelf = connection
            self.Connections[connectionID] = displayConnection

    def initialise(self):
        pygame.init()
        self.mainScr = pygame.display.set_mode((DimensionConstants.WIN_WIDTH, DimensionConstants.WIN_HEIGHT),
                                               pygame.RESIZABLE)
        self.mainScr.fill(ColourConstants.BACKGROUND)
        pygame.display.set_caption('MnemeV2')
        self.drawObjects()

    def drawGrid(self):
        for i in range(16):
            pygame.draw.line(self.mainScr, ColourConstants.GREY, (i * DimensionConstants.SQUAREUNIT, 0),
                             (i * DimensionConstants.SQUAREUNIT, DimensionConstants.HEIGHT))
            pygame.draw.line(self.mainScr, ColourConstants.GREY, (0, i * DimensionConstants.SQUAREUNIT),
                             (DimensionConstants.WIDTH, i * DimensionConstants.SQUAREUNIT))

    def drawObjects(self):
        self.drawConnections()
        self.drawBlocks()

    def drawBlocks(self):
        for block in self.Blocks.values():
            block.draw()

    def drawConnections(self):
        for connection in self.Connections.values():
            connection.draw()

    @staticmethod
    def update():
        pygame.display.update()
