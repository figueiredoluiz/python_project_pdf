import os
import json
from typing import List, Optional, Dict, Any
import pathspec

class FileUtils:
    @staticmethod
    def get_file_extension(file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        return ext.lstrip('.')

    @staticmethod
    def is_binary(file_path: str) -> bool:
        """
        Check if a file is binary.

        Args:
        file_path (str): The path to the file.

        Returns:
        bool: True if the file is binary, False otherwise.
        """
        try:
            with open(file_path, 'rb') as f:
                for block in iter(lambda: f.read(1024), b''):
                    if b'\0' in block:
                        return True
            return False
        except:
            return False

    @staticmethod
    def get_gitignore_patterns(directory: str) -> Optional[pathspec.PathSpec]:
        gitignore_path = os.path.join(directory, '.gitignore')
        if os.path.isfile(gitignore_path):
            try:
                with open(gitignore_path, 'r') as gitignore_file:
                    return pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignore_file)
            except Exception as e:
                print(f"Warning: Error reading .gitignore file: {e}")
        return None

    @staticmethod
    def get_file_structure(directory: str, gitignore_matcher: Optional[pathspec.PathSpec] = None) -> List[str]:
        file_structure = []
        for root, dirs, files in os.walk(directory):
            if '.git' in dirs:
                dirs.remove('.git')
            if '.gitignore' in dirs:
                dirs.remove('.gitignore')
            for file in files:
                try:
                    file_path = os.path.relpath(os.path.join(root, file), directory)
                    if gitignore_matcher and gitignore_matcher.match_file(file_path):
                        continue
                    file_structure.append(file_path)
                except UnicodeDecodeError:
                    print(f"Warning: Could not process file name: {file}")
        return sorted(file_structure)

    @staticmethod
    def get_project_info(directory: str) -> Optional[Dict[str, Any]]:
        package_json_path = os.path.join(directory, 'package.json')
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                data = json.load(f)
                return {
                    "name": data.get("name", "Unnamed Project"),
                    "version": data.get("version", "0.0.0"),
                    "author": data.get("author"),
                    "description": data.get("description"),
                    "license": data.get("license"),
                    "homepage": data.get("homepage"),
                    "repository": data.get("repository", {}).get("url") if isinstance(data.get("repository"), dict) else data.get("repository"),
                    "keywords": data.get("keywords")
                }
        return None
