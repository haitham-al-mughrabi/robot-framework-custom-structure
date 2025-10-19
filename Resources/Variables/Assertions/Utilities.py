from pathlib import Path

optimize_link = lambda link: Path(link)
# ASSERTIONS.RESOURCE
POSITIVE_ELEMENT_STATE_RESULT = """
Assertion Got Successfully Passed.
Element Status Matches The Expected Result.
"""

# Cookies.resource
COOKIE_JAR_EMPTY = """
Given Cookie Is Empty!
"""

# DynamicValues.resource
CITY_NOT_FOUND_IN_ENUM = """
No Group Has The Given Name. Aborting!
"""

# FileDirOperations.resource
DIRECTORY_ALREADY_DELETED_MESSAGE = """
Directory/Directories has/have been already deleted
"""
FILE_ALREADY_DELETED_MESSAGE = """
File is already deleted
"""

# Dynamic Variables
NEGATIVE_ELEMENT_STATE_RESULT = lambda expected_status, element_statuses: f"""
Assertion Failed. Expected {expected_status} Status. Got {', '.join(element_statuses)}
"""
NEGATIVE_VARIABLE_TYPE_ERROR = lambda value_type: f"""
Passed Value Not Supported! Provided Variable Type:{value_type}
"""
DIRECTORY_FOUND_PATH_MESSAGE = lambda directory_path: rf"""
Directory is already created under {optimize_link(directory_path)}
"""
FILE_FOUND_PATH_MESSAGE = lambda file_path: rf"""
File is already created under {file_path}
"""
FILE_NOT_EXISTS_MESSAGE = lambda expected_file_path: rf"""
File {expected_file_path} does not exists.
"""
DIRECTORY_NOT_EXISTS_MESSAGE = lambda expected_directory_path: rf"""
Directory {expected_directory_path} does not exists.
"""
LOCAL_STORAGE_HAS_THE_DESIRED_KEY = lambda desired_key: f"""
The key {desired_key} has been found in the browser local storage.
"""
KEY_NOT_FOUND_IN_LOCAL_STORAGE = lambda desired_key: f"""
The Key {desired_key} could not be found in the local storage. Aborting!
"""
KEY_FOUND_IN_LOCAL_STORAGE_ERROR = lambda desired_key: f"""
The key {desired_key} has been found in the browser local storage. Aborting!
"""
KEY_NOT_FOUND_IN_LOCAL_STORAGE_SUCCESS = lambda desired_key: f"""
The key {desired_key} couldn't be found in the browser local storage.
"""
