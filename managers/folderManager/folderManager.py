import json
import os
from typing import Dict, List

from managers.folderManager.folderObj import FolderObj, ScriptObj, FolderNetwork


class FolderManager:
    folderStructureDict: Dict = dict()
    folderNetwork: FolderNetwork = None
    folderDict: Dict[str, FolderObj] = dict()
    fileDict:  Dict[str, ScriptObj] = dict()

    def __init__(self):
        self.config = json.load(open('config.json'))
        self.rootFolder = self.getRootFolder()
        self.getFolderStructure()
        pass

    def getRootFolder(self) -> str:
        return self.config['folder']

    def getFolderStructure(self) -> None:
        self.buildFolderStructure(self.rootFolder)

    def buildFolderStructure(self, rootFolder: str):
        folderWalk = os.walk(rootFolder)
        for root, dirs, scripts in list(folderWalk):
            rootFolderObj = self.createFolderObj(root, dirs, scripts)
            self.folderStructureDict[root] = rootFolderObj
            self.folderDict[rootFolderObj.id] = rootFolderObj

        for root, folderobj in self.folderStructureDict.items():
            for subfolder in folderobj.subfolderNames:
                folderobj.subfolderObjs.append(self.folderStructureDict[root + '\\' + subfolder])

    def createFolderObj(self, root: str, dirs: List[str], scripts: List[str]) -> FolderObj:
        folder = FolderObj()
        folder.pathLocation = root
        folder.folder = None
        folder.name = root
        folder.scriptNames = scripts
        for script in folder.scriptNames:
            scriptObj = self.createScriptObj(root, script)
            folder.fileObjs.append(scriptObj)
            self.fileDict[scriptObj.id] = scriptObj

        folder.subfolderNames = dirs
        return folder

    def createScriptObj(self, root: str, script: str):
        scriptObj = ScriptObj()
        scriptObj.pathLocation = root + '\\' + script
        scriptObj.folder = root
        scriptObj.name = script
        scriptObj.extension = script.split('.')[-1]
        return scriptObj


if __name__ == '__main__':
    FolderManager()
