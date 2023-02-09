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
        self.setup(devMode=devMode)
        while self.run:
            self.interpretInput()
            self.updatingDisplay()

    def setup(self, devMode=False):
        self.setupManagers()
        self.initialiseDisplay(devMode=devMode)

    def setupManagers(self):
        self.folderManager = FolderManager()
        self.connectionManager = ConnectionManager(self.folderManager)

        self.displayManager = DisplayManager(
            self.connectionManager.connectionDict,
            self.folderManager.scriptDict
        )
        self.inputManager = InputManager(self.displayManager)

    def initialiseDisplay(self, devMode=False):
        self.displayManager.initialise(devMode=devMode)

    def interpretInput(self) -> None:
        self.run = self.inputManager.interpretInput()

    def updatingDisplay(self) -> None:
        self.displayManager.update()

    def gridBackground(self):
        self.displayManager.drawGrid()


def main(devMode=False):
    Mneme().main(devMode)
