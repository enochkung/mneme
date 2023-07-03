from typing import List, Union
import uuid


class Connector:
    id: uuid.uuid4 = uuid.uuid4()
    source: Union[File, Folder] = None
    target: Union[File, Folder] = None


class File:
    id: uuid.uuid4 = uuid.uuid4()
    connectors: List[Connector] = list()


class Folder:
    id: uuid.uuid4 = uuid.uuid4()
    connectors: List[Connector] = list()


