import os
import uuid
from typing import Dict, List

from GPT_version.utils import extract_imports
from basicObjects import File, Folder, Connector


class StructureManager:
    masterDirectory: str = None
    structure: Dict[str, Dict[str, List]] = None
    fileObjects: Dict[str, File] = dict()
    folderObjects: Dict[str, Folder] = dict()
    connectorObjects: Dict[str, Connector] = dict()
    fileNameToId: Dict[str, str] = dict()
    folderNameToId: Dict[str, str] = dict()

    def getStructure(self):
        """
        Structure of Folders and Files

        Folder Name: { 'Files': list of filenames,
                       'Folders': list of foldernames }
        """
        structure = dict()

        subObjects = os.walk(self.masterDirectory)

        for subobject in subObjects:
            structure[subobject[0]] = dict()
            structure[subobject[0]]['Files'] = subobject[2]
            if subobject[1]:
                structure[subobject[0]]['Folders'] = [subobject[0] + rf'\{x}' for x in subobject[1]]

        self.structure = structure

    def createFileObjects(self):
        files = [(folderName, file) for folderName, folder in self.structure.items() for file in folder['Files']]

        for file in files:
            print('File: ', file[1])
            fileObject = File()
            fileObject.id = str(uuid.uuid4())
            fileObject.name = file[1]
            fileObject.folder = file[0]

            self.fileObjects[fileObject.id] = fileObject
            self.fileNameToId[file[0] + rf"\{file[1]}"] = fileObject.id

    def createFolderObjects(self):
        folders = self.structure.items()

        for folderName, folder in folders:
            print('Folder: ', folderName)
            folderObject = Folder()
            folderObject.id = str(uuid.uuid4())
            folderObject.name = folder
            motherFolder = max(
                [_folder for _folder in self.structure if _folder in folder and _folder != folder],
                key=lambda x: len(x),
                default=None
            )

            folderObject.mother = motherFolder
            # motherFolder is empty iff folder is the master folder

            self.folderObjects[folderObject.id] = folderObject
            self.folderNameToId[folderName] = folderObject.id

    def createObjects(self):
        self.createFileObjects()
        self.createFolderObjects()

    def getConnections(self):
        for folder, folderStruct in self.structure.items():
            for file in folderStruct['Files']:
                fileDir = folder + rf'\{file}'
                imports = extract_imports(fileDir)
                for imp in imports:
                    connector = Connector()
                    connector.id = str(uuid.uuid4())
                    connector.source = self.fileNameToId[fileDir]
                    connector.target = self.fileNameToId[imp]

                    self.connectorObjects[connector.id] = connector
                    self.fileObjects[self.fileNameToId[imp]].connectors.append(connector.id)
                    self.fileObjects[self.fileNameToId[fileDir]].connectors.append(connector.id)
                    self.folderObjects[self.folderNameToId[folder]].connectors.append(connector.id)


if __name__ == '__main__':
    sm = StructureManager()
    sm.masterDirectory = r'C:\Users\FW246CA\repos\mneme\mneme\test_folder'
    sm.getStructure()
    sm.createObjects()

    sm.getConnections()
    pass
