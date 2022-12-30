from typing import Set, List, Dict, Union, Tuple
import os


class MneDir:
    def __init__(self, dir_address: str):
        self.dir_address = dir_address
        self.sub_folders: Set[MneDir] = set()
        self.sub_pyscripts: Set[MneScript] = set()


class MneScript:
    def __init__(self, script_name, imports, classes, functions):
        self.script_name = script_name
        self.imports: Set[MneImport] = imports
        self.classes: Set[MneClass] = classes
        self.functions: Set[MneFunc] = functions
        self.level: int = 0


class MneClass:
    def __init__(self, class_name, pyscript_dir):
        self.class_name = class_name
        self.pyscript_dir = pyscript_dir
        self.methods: Set[str] = set()
        self.attributes: Set[str] = set()
        self.reference_files: Set[MneScript] = set()


class MneFunc:
    def __init__(self, func_name, pyscript_dir):
        self.func_name = func_name
        self.pyscript_dir = pyscript_dir
        self.script_object = MneScript
        self.reference_files: Set[MneScript] = set()


class MneImport:
    def __init__(self, import_script, imported, pyscript_dir):
        self.import_script_name: str = import_script
        self.imported_object_name: str = imported
        self.current_script_name: str = pyscript_dir
        self.import_script_object: MneScript = None
        self.import_imported_objects: List[Union[MneClass, MneFunc]] = list()


class Mneme:
    root_dir: str = None
    folders: List[MneDir] = list()
    objects_by_script: Dict = dict()
    root_mnedir: MneDir = None
    mnedir_dict: Dict = dict()
    scripts: List[MneScript] = list()
    ignored_folder_set: Set[str] = {'.git', '.idea', '__pycache__'}
    ignored_script_set: Set[str] = set()

    def directory_reader(self, root_dir) -> None:
        self.root_dir = root_dir
        self.mnedir_dict = dict()

        os_walk = os.walk(self.root_dir)
        for root, dirs, scripts in os_walk:
            if self.dir_create(root, dirs, scripts):
                mnedir = MneDir(root)
                mnedir.sub_folders = {
                    folder for folder in dirs if all(ignored not in folder for ignored in self.ignored_folder_set)
                }
                mnedir.sub_pyscripts = {
                    script for script in scripts if
                    all(ignored not in script for ignored in self.ignored_script_set) and
                    '.py' in script
                }
                self.mnedir_dict[root] = mnedir
        self.root_mnedir = self.mnedir_dict[self.root_dir]

    def dir_create(self, root, dirs, scripts):
        return not any(root.__contains__(ignored) for ignored in self.ignored_folder_set)

    def object_log(self):
        """
        Read all py scripts and locate classes and functions
        :return:
        """
        for directory, mnedir in self.mnedir_dict.items():
            for pyscript in mnedir.sub_pyscripts:
                with open(directory + '\\' + pyscript) as f:
                    # TODO: different directories may have same pyscript
                    lines = f.readlines()
                    imports, classes, functions = self.get_objects(lines, directory + '\\' + pyscript)
                    mneScript = MneScript(directory + '\\' + pyscript, imports, classes, functions)
                    mneScript.level = len(mneScript.script_name.replace(self.root_dir + '\\', '').split('\\'))
                    self.scripts.append(mneScript)

    def get_objects(self, lines: List[str], pyscript: str) -> \
            Tuple[List[MneImport], List[MneClass], List[MneFunc]]:
        imports_list = list()
        classes_list = list()
        funcs_list = list()
        for line in lines:
            if 'from' in line and 'import' in line:
                imports_component = line.replace('\n', '').replace('from ', '').split(' import ')
                cleanup_address = self.cleanup_address(self.root_dir + '\\' + imports_component[0].replace('.', '\\') + '.py')
                imports_list.append(
                    MneImport(cleanup_address, imports_component[1].split(', '), pyscript)
                )
            if 'class' in line:
                classes_list.append(MneClass(line.replace(':\n', '').split(' ')[1], pyscript))
            if 'def' in line:
                funcs_list.append(MneFunc(line.replace(':', '').split(' ')[1].split('(')[0], pyscript))

        return imports_list, classes_list, funcs_list

    def cleanup_address(self, dir_address):
        return dir_address.replace('\\\\', '\\')