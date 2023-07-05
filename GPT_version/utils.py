import re
import os
import sys


def extract_imports(script_path):
    imports = []
    script_dir = os.path.dirname(script_path)

    with open(script_path, 'r') as file:
        script_content = file.read()

        # Use regular expressions to find import statements
        import_regex = r'^\s*import\s+([\w\.]+)'
        from_import_regex = r'^\s*from\s+([\w\.]+)\s+import'
        matches = re.findall(import_regex, script_content, re.MULTILINE)
        matches += re.findall(from_import_regex, script_content, re.MULTILINE)

        # Extract directory paths from import statements
        for module in matches:
            module_path = module.replace('.', '\\')
            module_dir = os.path.join(script_dir, module_path + '.py')
            if not os.path.exists(module_dir):
                # Search for the correct directory name
                module_dir = None
                for directory in sys.path:
                    potential_dir = os.path.join(directory, module_path + '.py')
                    if os.path.exists(potential_dir):
                        module_dir = potential_dir
                        break
            if module_dir is not None:
                imports.append(module_dir)

    return imports