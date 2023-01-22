import uuid
from typing import Tuple, Union, Dict, Any

import networkx as nx

from gameConstants import ColourConstants, DimensionConstants
from managers.connectionManager.connectionObj import ConnectionObj
from managers.folderManager.folderObj import FolderObj, ScriptObj


class DisplayBlock:
    id: uuid = None
    center: Tuple = (0, 0)
    mnemeSelf: Union[FolderObj, ScriptObj] = None
    shape: Tuple = None
    colour: ColourConstants = None
    border_colour: ColourConstants = ColourConstants.WHITE
    width: DimensionConstants = DimensionConstants.ScriptWidth

    def createPygameObj(self):
        pass

    def refresh(self):
        pass

    def draw(self):
        print(self.id)


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

    def draw(self):
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
