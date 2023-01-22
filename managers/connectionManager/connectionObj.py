import uuid

from managers.folderManager.folderObj import ScriptObj


class ConnectionObj:
    id: uuid = None
    sourceScriptID: str = None
    targetScriptID: str = None

    def __init__(self):
        self.id = uuid.uuid4()

    def createObj(self, sourceScript: ScriptObj, targetScript: ScriptObj):
        self.sourceScriptID = sourceScript.id
        self.targetScriptID = targetScript.id
        return self

