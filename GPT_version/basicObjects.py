from typing import List, Union
import uuid


class Connector:
    id: str = None
    source: str = None
    target: str = None


class File:
    id: str = None
    connectors: List[str] = list()
    name: str = None
    folder: str = None


class Folder:
    id: str = None
    connectors: List[str] = list()
    name: str = None
    mother: str = None


class Function:
    id: str = None
    file: str = None
