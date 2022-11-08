from typing import Set, List
import os


class MneDir:
    def __init__(self, dir_address: str):
        self.dir_address = dir_address
        self.sub_folders: Set[MneDir] = set()
        self.sub_pyscripts: Set[MneScript] = set()


class MneScript:
    def __init__(self):
        self.classes: Set[MneClass] = set()
        self.functions: Set[MneFunc] = set()


class MneClass:
    def __init__(self):
        self.methods: Set[str] = set()
        self.attributes: Set[str] = set()
        self.reference_files: Set[MneScript] = set()


class MneFunc:
    def __init__(self):
        self.reference_files: Set[MneScript] = set()


class Mneme:
    root_dir: str = None
    folders: List[MneDir] = list()
    mnedir: MneDir = None
    scripts: List[MneScript] = list()
    ignored_folder: Set[str] = set()

    def directory_reader(self) -> MneDir:
        os_walk = os.walk(os.getcwd())
        for root, dirs, scripts in os_walk:
            if self.dir_create(root, dirs, scripts):
                mnedir = MneDir(root)
                mnedir.sub_folders = {
                    folder for folder in dirs if all(ignored not in folder for ignored in self.ignored_folders)
                }
                mnedir.sub_pyscripts =

    def object_log(self):
        pass

    def diagram_generator(self):
        pass


