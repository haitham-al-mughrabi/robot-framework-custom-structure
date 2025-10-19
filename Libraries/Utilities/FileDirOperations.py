import os
from robot.api import logger
from robot.api.deco import keyword, library
import shutil


@library(doc_format='ROBOT')
class FileDirOperations:
    @keyword("Check And Create Directory")
    def check_and_create_directory(self, directory_path):
        """
        Checks if a directory exists. If it doesn't, creates the directory.

        Args:
            directory_path (str): The path of the directory to check/create.
        """
        if os.path.exists(directory_path):
            logger.info(f"Directory already exists: {directory_path}")
        else:
            try:
                os.makedirs(directory_path)
                logger.info(f"Directory created: {directory_path}")
            except Exception as e:
                logger.error(f"Failed to create directory: {e}")
                raise

    @keyword("Check And Create File")
    def check_and_create_file(self, file_path, content=None):
        """
        Checks if a file exists. If it doesn't, creates the file.
        Optionally fills the file with content if provided.

        Args:
            file_path (str): The path of the file to check/create.
            content (str, optional): The content to write to the file. If None or empty, the file will be empty.
        """
        if os.path.exists(file_path):
            logger.info(f"File already exists: {file_path}")
        else:
            try:
                # Create the directory structure if it doesn't exist
                directory = os.path.dirname(file_path)
                if directory and not os.path.exists(directory):
                    os.makedirs(directory)
                    logger.info(f"Directory created: {directory}")

                # Create the file and write content if provided
                with open(file_path, "w") as file:
                    if content:
                        file.write(content)
                        logger.info(f"File created and filled with content: {file_path}")
                    else:
                        file.write("")  # Create an empty file
                        logger.info(f"File created: {file_path}")
            except Exception as e:
                logger.error(f"Failed to create file: {e}")
                raise

    @keyword("Delete Directory If File Exists")
    def delete_directory_if_file_exists(self, file_path):
        """
        Checks if a file exists. If it does, deletes the directory containing the file.

        Args:
            file_path (str): The path of the file to check.
        """
        if os.path.exists(file_path):
            directory = os.path.dirname(file_path)
            if directory:
                try:
                    shutil.rmtree(directory)  # Delete the directory and its contents
                    logger.info(f"Directory deleted: {directory}")
                except Exception as e:
                    logger.error(f"Failed to delete directory: {e}")
                    raise
        else:
            logger.info(f"File does not exist: {file_path}")

    @keyword("Delete File If Exists")
    def delete_file_if_exists(self, file_path):
        """
        Checks if a file exists. If it does, deletes the file.

        Args:
            file_path (str): The path of the file to check.
        """
        if os.path.exists(file_path):
            try:
                os.remove(file_path)  # Delete the file
                logger.info(f"File deleted: {file_path}")
            except Exception as e:
                logger.error(f"Failed to delete file: {e}")
                raise
        else:
            logger.info(f"File does not exist: {file_path}")

    @keyword("Delete Everything Inside Directory")
    def delete_everything_inside_directory(self, directory_path):
        """
        Deletes all files and subdirectories inside the specified directory.

        Args:
            directory_path (str): The path of the directory to clean.
        """
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            try:
                # Iterate over all items in the directory
                for item in os.listdir(directory_path):
                    item_path = os.path.join(directory_path, item)
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.remove(item_path)  # Delete files or symbolic links
                        logger.info(f"Deleted file: {item_path}")
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Delete subdirectories
                        logger.info(f"Deleted directory: {item_path}")
                logger.info(f"All contents deleted from directory: {directory_path}")
            except Exception as e:
                logger.error(f"Failed to delete contents: {e}")
                raise
        else:
            logger.error(f"Directory does not exist or is not a directory: {directory_path}")

    @keyword("Move File If Exists")
    def move_file_if_exists(self, source_path, destination_path):
        """
        Checks if a file exists at the source path. If it does, moves it to the destination path.

        Args:
            source_path (str): The path of the file to move.
            destination_path (str): The path where the file should be moved.
        """
        if os.path.exists(source_path) and os.path.isfile(source_path):
            try:
                # Create the destination directory if it doesn't exist
                destination_directory = os.path.dirname(destination_path)
                if destination_directory and not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)
                    logger.info(f"Created directory: {destination_directory}")

                # Move the file
                shutil.move(source_path, destination_path)
                logger.info(f"Moved file from {source_path} to {destination_path}")
            except Exception as e:
                logger.error(f"Failed to move file: {e}")
                raise
        else:
            logger.error(f"File does not exist or is not a file: {source_path}")

    @keyword("Move All Files From Directory")
    def move_all_files_from_directory(self, source_directory, destination_directory):
        """
        Moves all files from the source directory to the destination directory.

        Args:
            source_directory (str): The path of the source directory.
            destination_directory (str): The path of the destination directory.
        """
        if os.path.exists(source_directory) and os.path.isdir(source_directory):
            try:
                # Create the destination directory if it doesn't exist
                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)
                    logger.info(f"Created destination directory: {destination_directory}")

                # Move all files from the source directory to the destination directory
                for file_name in os.listdir(source_directory):
                    source_file_path = os.path.join(source_directory, file_name)
                    if os.path.isfile(source_file_path):  # Ensure it's a file (not a subdirectory)
                        destination_file_path = os.path.join(destination_directory, file_name)
                        shutil.move(source_file_path, destination_file_path)
                        logger.info(f"Moved file: {source_file_path} to {destination_file_path}")

                logger.info(f"All files moved from {source_directory} to {destination_directory}")
            except Exception as e:
                logger.error(f"Failed to move files: {e}")
                raise
        else:
            logger.error(f"Source directory does not exist or is not a directory: {source_directory}")

    @keyword("Rename File")
    def rename_file(self, old_file_path, new_file_path):
        """
        Renames a file from the old path to the new path.

        Args:
            old_file_path (str): The current path of the file.
            new_file_path (str): The new path for the file.
        """
        if os.path.exists(old_file_path) and os.path.isfile(old_file_path):
            try:
                os.rename(old_file_path, new_file_path)
                logger.info(f"Renamed file from {old_file_path} to {new_file_path}")
            except Exception as e:
                logger.error(f"Failed to rename file: {e}")
                raise
        else:
            logger.error(f"File does not exist or is not a file: {old_file_path}")

    @keyword("Rename Multiple Files")
    def rename_multiple_files(self, directory_path, old_name_pattern, new_name_pattern):
        """
        Renames multiple files in a directory based on a pattern.

        Args:
            directory_path (str): The path of the directory containing the files.
            old_name_pattern (str): The pattern to match in the file names (e.g., "old_prefix_*").
            new_name_pattern (str): The new pattern to replace in the file names (e.g., "new_prefix_*").
        """
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            try:
                for file_name in os.listdir(directory_path):
                    if file_name.startswith(old_name_pattern):
                        old_file_path = os.path.join(directory_path, file_name)
                        new_file_name = file_name.replace(old_name_pattern, new_name_pattern, 1)
                        new_file_path = os.path.join(directory_path, new_file_name)
                        os.rename(old_file_path, new_file_path)
                        logger.info(f"Renamed file from {old_file_path} to {new_file_path}")
            except Exception as e:
                logger.error(f"Failed to rename files: {e}")
                raise
        else:
            logger.error(f"Directory does not exist or is not a directory: {directory_path}")

    @keyword("Rename Directory")
    def rename_directory(self, old_directory_path, new_directory_path):
        """
        Renames a directory from the old path to the new path.

        Args:
            old_directory_path (str): The current path of the directory.
            new_directory_path (str): The new path for the directory.
        """
        if os.path.exists(old_directory_path) and os.path.isdir(old_directory_path):
            try:
                os.rename(old_directory_path, new_directory_path)
                logger.info(f"Renamed directory from {old_directory_path} to {new_directory_path}")
            except Exception as e:
                logger.error(f"Failed to rename directory: {e}")
                raise
        else:
            logger.error(f"Directory does not exist or is not a directory: {old_directory_path}")

    @keyword("Rename All Files In Directory")
    def rename_all_files_in_directory(self, directory_path, new_name_prefix):
        """
        Renames all files in a directory with a new prefix.

        Args:
            directory_path (str): The path of the directory containing the files.
            new_name_prefix (str): The prefix to add to the file names.
        """
        if os.path.exists(directory_path) and os.path.isdir(directory_path):
            try:
                for index, file_name in enumerate(os.listdir(directory_path)):
                    file_path = os.path.join(directory_path, file_name)
                    if os.path.isfile(file_path):
                        new_file_name = f"{new_name_prefix}_{index + 1}{os.path.splitext(file_name)[1]}"
                        new_file_path = os.path.join(directory_path, new_file_name)
                        os.rename(file_path, new_file_path)
                        logger.info(f"Renamed file from {file_path} to {new_file_path}")
            except Exception as e:
                logger.error(f"Failed to rename files: {e}")
                raise
        else:
            logger.error(f"Directory does not exist or is not a directory: {directory_path}")

    @keyword("Get File Name And Extension")
    def get_file_name_and_extension(self, file_path):
        """
        Extracts the file name and file extension from a given file path.

        Args:
            file_path (str): The full path of the file.

        Returns:
            dict: A dictionary containing the file name and file extension.
                  Example: {"file_name": "example.txt", "file_extension": ".txt"}
        """
        if os.path.isfile(file_path):
            file_name = os.path.basename(file_path)  # Extract file name
            file_extension = os.path.splitext(file_path)[1]  # Extract file extension
            result = {
                "file_name": file_name,
                "file_extension": file_extension
            }
            logger.info(f"File name and extension extracted: {result}")
            return result
        else:
            logger.error(f"Path is not a file: {file_path}")
            raise ValueError(f"Path is not a file: {file_path}")
