from typing import List

import networkx as nx
import uuid

from managers.managerConstants import FolderConstants


class ScriptObj:
    id: uuid = None
    pathLocation: str = None
    folder: uuid = None
    name: str = None
    extension: str = None

    def __init__(self):
        self.id = uuid.uuid4()


class FolderObj:
    id: uuid = None
    pathLocation: str = None
    folder: uuid = None
    name: str = None
    fileObjs: List = list()
    fileNames: List = list()
    subfolderObjs: List = list()
    subfolderNames: List = list()

    def __init__(self):
        self.id = uuid.uuid4()


class FolderNetwork:
    graph: nx.DiGraph = None

    def createNetwork(self, folderDict):
        self.graph = nx.DiGraph()
        for folderID, folderObj in folderDict.items():
            self.createNodesAndConnections(folderID, folderObj)

    def createNodesAndConnections(self, folderID: uuid, folderObj: FolderObj):
        self.graph.add_node(folderID)
        self.graph.add_nodes_from({folderID: {FolderConstants.Type: FolderConstants.FolderType}})

        for script in folderObj.fileObjs:
            self.graph.add_node(script.id)
            self.graph.add_nodes_from({script.id: {FolderConstants.Type: FolderConstants.ScriptType}})

