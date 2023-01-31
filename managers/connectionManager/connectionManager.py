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
        self.scriptDict = folderManager.scriptDict
        self.initialiseConnections()

    def initialiseConnections(self):
        for scriptObj in self.scriptDict.values():
            with open(scriptObj.pathLocation) as f:
                lines = f.readlines()
                for line in filter(lambda _line: 'import' in _line, lines):
                    lineWords = line.split(' ')
                    if lineWords[0] == 'from' or lineWords[0] == 'import':
                        importSource = lineWords[1]
                    else:
                        continue
                    isSource, sourceLocationName, sourceScriptName = self._checkSource(importSource)
                    # print(isSource, sourceLocation, importSource)
                    if isSource:
                        sourceFolderObj = self.folderStructureDict[sourceLocationName]
                        sourceScriptObj = [scriptobj for scriptobj in sourceFolderObj.fileObjs
                                           if sourceScriptName in scriptobj.name][0]
                        connectionObj = ConnectionObj().createObj(sourceScriptObj, scriptObj)
                        self.connectionDict[connectionObj.id] = connectionObj

        pass

    def _checkSource(self, importSource: str) -> Tuple[bool, Optional[str], Optional[str]]:
        location = importSource.split('.')

        for pathLocation in self.folderStructureDict:
            if location[:-1] == pathLocation.split('\\')[(-len(location) + 1):]:
                return True, pathLocation, location[-1]
        return False, None, None
