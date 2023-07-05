import ast
import builtins
import os
import re
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


def extract_used_imported_functions(script_path):
    used_functions = []
    imported_functions = {}

    # Parse the script's abstract syntax tree (AST)
    with open(script_path, 'r') as file:
        script_content = file.read()
        tree = ast.parse(script_content, script_path)

        # Extract the imported functions and their aliases
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ImportFrom):
                module_name = node.module
                for alias in node.names:
                    imported_functions[f"{module_name}.{alias.name}"] = alias.asname or alias.name
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imported_functions[alias.name] = alias.asname or alias.name

        # Extract the names of used functions
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                function_name = node.func.id
                if function_name not in builtins.__dict__:
                    used_functions.append(function_name)

    # Filter out the unused imported functions
    used_imported_functions = {
        function_name: function_alias
        for function_name, function_alias in imported_functions.items()
        if function_alias in used_functions
    }

    return used_imported_functions


if __name__ == '__main__':
    # Example usage
    script_path = r'C:\Users\FW246CA\repos\mneme\mneme\test_folder\main.py'
    used_imported_functions = extract_used_imported_functions(script_path)
    print(used_imported_functions)
