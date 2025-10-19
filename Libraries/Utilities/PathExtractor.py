import os
import re
import glob
from pathlib import Path
from typing import Optional, Tuple, Union, List
from robot.api import logger
from robot.api.deco import keyword, library


@library(doc_format='ROBOT')
class PathExtractor:
    """
    A class for extracting and replacing parts of a path.
    Designed to be used with Robot Framework.
    """

    @keyword('Extract From Folder')
    def extract_from_folder(self, full_path: str, start_folder: str) -> Optional[ str ]:
        """
        Extract a sub-path starting from a specific folder.

        Arguments:
            full_path: The complete path to extract from
            start_folder: The folder name to start extracting from

        Returns:
            The extracted sub-path starting from the specified folder,
            or None if the folder is not found in the path

        Examples:
            | ${result}= | Extract From Folder | a/b/c/d/e.exe | d |
        """
        # Convert to Path object for better path manipulation
        path_obj = Path(full_path)

        # Get all parts of the path
        parts = path_obj.parts

        # Find the start_folder in the path
        for i, part in enumerate(parts):
            if part == start_folder:
                # Return the path from the start_folder onwards
                result = os.path.join(*parts[ i: ])
                logger.info(f"Extracted path: {result}")
                return result

        # Return None if start_folder is not found
        logger.warn(f"Folder '{start_folder}' not found in path '{full_path}'")
        return None

    @keyword('Replace Path Prefix')
    def replace_path_prefix(self, original_path: str, common_folder: str, new_prefix: str) -> Optional[ str ]:
        """
        Replace part of a path before a common folder with a new prefix.

        Arguments:
            original_path: The original path to modify
            common_folder: The common folder that marks the start of the part to keep
            new_prefix: The new prefix path to prepend

        Returns:
            The new path with the prefix replaced, or None if the common folder is not found

        Examples:
            | ${result}= | Replace Path Prefix | a/b/c/d/e.exe | c | f/g/h |
        """
        # Get the sub-path starting from the common folder
        sub_path = self.extract_from_folder(original_path, common_folder)

        if sub_path is None:
            return None

        # Get the common folder and everything after it
        common_folder_parts = sub_path.split(os.sep)

        # Ensure new_prefix doesn't have trailing separator
        new_prefix = new_prefix.rstrip(os.sep)

        # Combine the new prefix with the common folder and everything after it
        result = os.path.join(new_prefix, *common_folder_parts)
        logger.info(f"Original path: {original_path}")
        logger.info(f"New path: {result}")
        return result

    @keyword('Add Path Postfix')
    def add_path_postfix(self, original_path: str, postfix: str) -> str:
        """
        Add a postfix to a path.

        Arguments:
            original_path: The original path to modify
            postfix: The postfix to add to the path

        Returns:
            The path with the postfix added

        Examples:
            | ${result}= | Add Path Postfix | a/b/c/d/e.exe | _backup |
        """
        # Split the path into directory and filename parts
        path_obj = Path(original_path)

        # Get the parent directory and filename
        directory = str(path_obj.parent)
        filename = path_obj.name

        # Split filename into name and extension
        name_parts = filename.split('.')

        if len(name_parts) > 1:
            # File has an extension
            name = '.'.join(name_parts[ :-1 ])
            extension = name_parts[ -1 ]
            new_filename = f"{name}{postfix}.{extension}"
        else:
            # File has no extension
            new_filename = f"{filename}{postfix}"

        # Combine the directory with the new filename
        if directory == '.':
            result = new_filename
        else:
            result = os.path.join(directory, new_filename)

        logger.info(f"Original path: {original_path}")
        logger.info(f"Path with postfix: {result}")
        return result

    @keyword('Replace File Path')
    def replace_file_path(self, original_path: str, new_path: str) -> str:
        """
        Replace a file path entirely with a new path.

        Arguments:
            original_path: The original path to replace
            new_path: The new path to use

        Returns:
            The new path

        Examples:
            | ${result}= | Replace File Path | a/b/c/d/e.exe | x/y/z/file.txt |
        """
        logger.info(f"Original path: {original_path}")
        logger.info(f"Replaced with: {new_path}")
        return new_path

    @keyword('Get File Name')
    def get_file_name(self, file_path: str, with_extension: bool = True) -> str:
        """
        Get the filename from a path, with or without extension.

        Arguments:
            file_path: The file path to extract the filename from
            with_extension: Whether to include the file extension (default: True)

        Returns:
            The filename with or without extension

        Examples:
            | ${result}= | Get File Name | a/b/c/d/e.exe | ${TRUE} |
        """
        path_obj = Path(file_path)
        if with_extension:
            result = path_obj.name
        else:
            result = path_obj.stem

        logger.info(f"Extracted filename: {result} from {file_path}")
        return result

    @keyword('Get File Extension')
    def get_file_extension(self, file_path: str) -> str:
        """
        Get the file extension from a path.

        Arguments:
            file_path: The file path to extract the extension from

        Returns:
            The file extension without the dot

        Examples:
            | ${result}= | Get File Extension | a/b/c/d/e.exe |
        """
        path_obj = Path(file_path)
        result = path_obj.suffix.lstrip('.')

        logger.info(f"Extracted extension: {result} from {file_path}")
        return result

    @keyword('Get Parent Directory')
    def get_parent_directory(self, file_path: str, levels: int = 1) -> str:
        """
        Get the parent directory of a path, with optional level specification.

        Arguments:
            file_path: The file path to get the parent directory from
            levels: Number of levels up to go (default: 1)

        Returns:
            The parent directory path

        Examples:
            | ${result}= | Get Parent Directory | a/b/c/d/e.exe | 2 |
        """
        path_obj = Path(file_path)

        # Start with the parent
        result = path_obj.parent

        # Go up additional levels if requested
        for _ in range(levels - 1):
            if str(result) == ".":
                break
            result = result.parent

        logger.info(f"Parent directory (level {levels}): {result} from {file_path}")
        return str(result)

    @keyword('Join Paths')
    def join_paths(self, *paths: str) -> str:
        """
        Join multiple path components together.

        Arguments:
            *paths: Path components to join

        Returns:
            The joined path

        Examples:
            | ${result}= | Join Paths | a | b | c | file.txt |
        """
        result = os.path.join(*paths)
        logger.info(f"Joined path: {result}")
        return result

    @keyword('Find Files')
    def find_files(self, directory: str, pattern: str) -> List[ str ]:
        """
        Find files matching a pattern in a directory.

        Arguments:
            directory: The directory to search in
            pattern: The glob pattern to match files against

        Returns:
            List of matching file paths

        Examples:
            | ${files}= | Find Files | downloads | *.pdf |
        """
        search_pattern = os.path.join(directory, pattern)
        matches = glob.glob(search_pattern)

        logger.info(f"Found {len(matches)} files matching pattern '{pattern}' in '{directory}'")
        for match in matches:
            logger.debug(f"  Match: {match}")

        return matches

    @keyword('Normalize Path')
    def normalize_path(self, file_path: str) -> str:
        """
        Normalize a path (resolve relative references, simplify).

        Arguments:
            file_path: The file path to normalize

        Returns:
            The normalized path

        Examples:
            | ${result}= | Normalize Path | a/b/../c/./d/e.exe |
        """
        result = os.path.normpath(file_path)
        logger.info(f"Normalized path: {result} from {file_path}")
        return result

    @keyword('Replace Extension')
    def replace_extension(self, file_path: str, new_extension: str) -> str:
        """
        Replace the extension of a file path.

        Arguments:
            file_path: The file path to modify
            new_extension: The new extension (with or without dot)

        Returns:
            The path with the new extension

        Examples:
            | ${result}= | Replace Extension | a/b/c/d/e.exe | txt |
        """
        path_obj = Path(file_path)

        # Ensure the new extension has a leading dot
        if not new_extension.startswith('.'):
            new_extension = f".{new_extension}"

        # Create a new path with the same stem but different suffix
        new_path = path_obj.with_suffix(new_extension)

        logger.info(f"Changed extension: {file_path} → {new_path}")
        return str(new_path)

    @keyword(name="Get Project Directory")
    def get_project_directory(self):
        """
        Attempts to automatically find the project directory.

        Returns:
            str: The absolute path of the project directory.

        Raises:
            FileNotFoundError: If the project directory cannot be determined.
        """
        # Method 1: Look for common project identifiers
        current_path = os.path.dirname(os.path.abspath(__file__))

        # Common project identifiers
        identifiers = [ '.git', 'pyproject.toml', 'setup.py', 'requirements.txt', '.project' ]

        # Walk up the directory tree
        while True:
            for identifier in identifiers:
                if os.path.exists(os.path.join(current_path, identifier)):
                    return current_path

            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:  # Reached the root
                break

            current_path = parent_path

        # Method 2: Try to infer from Python module structure
        current_path = os.path.dirname(os.path.abspath(__file__))
        path_parts = current_path.split(os.sep)

        # Look for a directory with an __init__.py file but its parent doesn't have one
        for i in range(len(path_parts), 0, -1):
            test_path = os.sep.join(path_parts[ :i ])
            if os.path.exists(os.path.join(test_path, '__init__.py')):
                parent_path = os.path.dirname(test_path)
                if not os.path.exists(os.path.join(parent_path, '__init__.py')):
                    return test_path

        raise FileNotFoundError("Could not automatically determine project directory")