import uuid
from typing import List, Dict, Any, Tuple

import pygame

from Cartographer.cartographer import Cartographer, Navigator
from gameConstants import ColourConstants, DimensionConstants
from managers.connectionManager.connectionObj import ConnectionObj
from managers.displayManager.displayObject import DisplayNetwork, DisplayConnection, DisplayBlock
from managers.folderManager.folderObj import ScriptObj


class DisplayManager:
    mainScr = None
    Blocks: Dict[str, DisplayBlock] = dict()
    Connections: Dict[str, DisplayConnection] = dict()
    graph: DisplayNetwork = None
    cartographer: Cartographer = Cartographer()
    navigator: Navigator = Navigator()
    blockCoords: Dict[str, Tuple[int, float]]
    connectionCoords: Dict[str, List[Tuple[float, float]]]
    numLevels: int = 0

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

    def initialise(self, devMode=False):
        pygame.init()
        self.mainScr = pygame.display.set_mode((DimensionConstants.WIN_WIDTH, DimensionConstants.WIN_HEIGHT),
                                               pygame.RESIZABLE)
        self.mainScr.fill(ColourConstants.BACKGROUND)
        pygame.display.set_caption('MnemeV2')
        if devMode:
            self.drawGrid()
        self.drawObjects(initialise=True)

    def drawGrid(self):
        for i in range(16):
            pygame.draw.line(self.mainScr, ColourConstants.GREY, (i * DimensionConstants.SQUAREUNIT, 0),
                             (i * DimensionConstants.SQUAREUNIT, DimensionConstants.HEIGHT))
            pygame.draw.line(self.mainScr, ColourConstants.GREY, (0, i * DimensionConstants.SQUAREUNIT),
                             (DimensionConstants.WIDTH, i * DimensionConstants.SQUAREUNIT))

    def drawObjects(self, initialise=False):
        self.mainScr.fill(ColourConstants.BACKGROUND)
        if initialise:
            self.autosetBlocks()
            self.autosetConnections()
        self.drawConnections()
        self.drawBlocks()

    def autosetBlocks(self) -> None:
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
        self.blockCoords = self.cartographer.autosetBlocks(self.Blocks, self.Connections)
        self.numLevels = self.cartographer.numLevels
        self.updateBlockPos()

    def autosetConnections(self) -> None:
        self.connectionCoords = self.navigator.autosetConnections(self.Blocks, self.Connections)
        self.updateConnectionPos()

    def updateBlockPos(self):
        for scriptID, pos in self.blockCoords.items():
            self.Blocks[scriptID].updatePos(pos, self.numLevels)

    def updateConnectionPos(self):
        for connectionID, pos in self.connectionCoords.items():
            self.Connections[connectionID].updatePos(pos)

    def drawBlocks(self) -> None:
        for block in self.Blocks.values():
            block.draw(self.mainScr)

    def drawConnections(self) -> None:
        for connection in self.Connections.values():
            connection.draw(self.mainScr)

    def runSingleClick(self, pos):
        for blockID, block in self.Blocks.items():
            if block.isinBlock(pos):
                block.singleClicked()
            else:
                block.clicked = False

    def runDoubleClick(self, pos):
        for blockID, block in self.Blocks.items():
            if block.isinBlock(pos):
                block.doubleClicked()
            else:
                block.clicked = False

    def checkHover(self, pos):
        for blockID, block in self.Blocks.items():
            if block.isinBlock(pos) and not block.clicked:
                block.highlight()
                return
            elif not block.clicked:
                block.dehighlight()

    def runDragging(self):
        pos = pygame.mouse.get_pos()
        for blockID, block in self.Blocks.items():
            if block.isinBlock(pos):
                block.recenter((pos[1], pos[0]))
                break
        self.update()

    def update(self):
        self.mainScr.fill(ColourConstants.BACKGROUND)
        self.drawGrid()
        self.drawObjects()
        pygame.display.update()
