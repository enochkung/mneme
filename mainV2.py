from managers.connectionManager.connectionManager import ConnectionManager
from managers.displayManager.displayManager import DisplayManager
from managers.folderManager.folderManager import FolderManager
from managers.inputManager.inputManager import InputManager


class Mneme:
    run: bool = True
    inputManager = None
    displayManager = None
    folderManager = None
    connectionManager = None
    mainScr = None

    def main(self, devMode=False):
        self.runPygame(devMode)

    def runPygame(self, devMode=False):
        self.setup()
        while self.run:
            self.interpretInput()
            self.updatingDisplay(withGrid=devMode)

    def setup(self):
        self.setupManagers()
        self.initialiseDisplay()

    def setupManagers(self):
        self.folderManager = FolderManager()
        self.connectionManager = ConnectionManager(self.folderManager)
        self.displayManager = DisplayManager(
            self.connectionManager.connectionDict,
            self.folderManager.fileDict
        )
        self.inputManager = InputManager(self.displayManager)

    def initialiseDisplay(self):
        self.displayManager.initialise()

    def interpretInput(self) -> None:
        self.run = self.inputManager.interpretInput()

    def updatingDisplay(self, withGrid=False) -> None:
        if withGrid:
            self.displayManager.drawGrid()
        self.displayManager.update()

    def gridBackground(self):
        self.displayManager.drawGrid()


def main(devMode=False):
    Mneme().main(devMode)
