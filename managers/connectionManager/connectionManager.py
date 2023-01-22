from typing import Dict, Tuple, Optional

from managers.connectionManager.connectionObj import ConnectionObj
import networkx as nx

from managers.folderManager.folderManager import FolderManager


class ConnectionManager:
    connectionDict: Dict[str, ConnectionObj] = dict()
    connectionNetwork: nx.DiGraph = None

    def __init__(self, folderManager: FolderManager):
        self.folderStructureDict = folderManager.folderStructureDict
        self.folderDict = folderManager.folderDict
        self.fileDict = folderManager.fileDict
        self.initialiseConnections()

    def initialiseConnections(self):
        for fileObj in self.fileDict.values():
            with open(fileObj.pathLocation) as f:
                lines = f.readlines()
                for line in filter(lambda _line: 'import' in _line, lines):
                    lineWords = line.split(' ')
                    if lineWords[0] == 'from':
                        importSource = lineWords[1]
                    elif lineWords[0] == 'import':
                        importSource = lineWords[1]
                    else:
                        continue
                    isSource, sourceLocation = self._checkSource(importSource)
                    # print(isSource, sourceLocation, importSource)
                    if isSource:
                        sourceObj = self.folderStructureDict[sourceLocation]
                        connectionObj = ConnectionObj().createObj(sourceObj, fileObj)
                        self.connectionDict[connectionObj.id] = connectionObj

        pass

    def _checkSource(self, importSource: str) -> Tuple[bool, Optional[str]]:
        location = importSource.split('.')

        for pathLocation in self.folderStructureDict:
            if location[:-1] == pathLocation.split('\\')[(-len(location) + 1):]:
                return True, pathLocation
        return False, None
