import re
from robot.api import logger
from robot.api.deco import keyword, library


@library(doc_format='ROBOT')
class StringOperations:
    @keyword("String Contains")
    def string_contains(self, string, substring):
        """
        Checks if a string contains a specific substring.

        Args:
            string (str): The main string to check.
            substring (str): The substring to search for.

        Returns:
            bool: True if the substring is found, otherwise False.
        """
        result = substring in string
        logger.info(f"Checked if '{string}' contains '{substring}': {result}")
        return result

    @keyword("Join Strings")
    def join_strings(self, *strings, separator=" "):
        """
        Joins multiple strings with a specified separator.

        Args:
            *strings (str): The strings to join.
            separator (str): The separator to use (default is a space).

        Returns:
            str: The joined string.
        """
        result = separator.join(strings)
        logger.info(f"Joined strings with separator '{separator}': {result}")
        return result

    @keyword("String To List")
    def string_to_list(self, string, delimiter=" "):
        """
        Splits a string into a list based on a delimiter.

        Args:
            string (str): The string to split.
            delimiter (str): The delimiter to use (default is a space).

        Returns:
            list: The list of substrings.
        """
        result = string.split(delimiter)
        logger.info(f"Split string '{string}' into list: {result}")
        return result

    @keyword("List To String")
    def list_to_string(self, list_of_strings, separator=" "):
        """
        Joins a list of strings into a single string with a specified separator.

        Args:
            list_of_strings (list): The list of strings to join.
            separator (str): The separator to use (default is a space).

        Returns:
            str: The joined string.
        """
        result = separator.join(list_of_strings)
        logger.info(f"Joined list into string with separator '{separator}': {result}")
        return result

    @keyword("Replace In String")
    def replace_in_string(self, string, old, new):
        """
        Replaces occurrences of a substring in a string with a new substring.

        Args:
            string (str): The main string.
            old (str): The substring to replace.
            new (str): The new substring.

        Returns:
            str: The string with replacements.
        """
        result = string.replace(old, new)
        logger.info(f"Replaced '{old}' with '{new}' in '{string}': {result}")
        return result

    @keyword("Extract Numbers From String")
    def extract_numbers_from_string(self, string):
        """
        Extracts all numbers from a string.

        Args:
            string (str): The string to extract numbers from.

        Returns:
            list: A list of extracted numbers as strings.
        """
        numbers = re.findall(r"\d+", string)
        logger.info(f"Extracted numbers from '{string}': {numbers}")
        return numbers

    @keyword("Extract Characters From String")
    def extract_characters_from_string(self, string):
        """
        Extracts all alphabetic characters from a string.

        Args:
            string (str): The string to extract characters from.

        Returns:
            list: A list of extracted characters.
        """
        characters = re.findall(r"[A-Za-z]", string)
        logger.info(f"Extracted characters from '{string}': {characters}")
        return characters

    @keyword("Trim String")
    def trim_string(self, string):
        """
        Removes leading and trailing whitespace from a string.

        Args:
            string (str): The string to trim.

        Returns:
            str: The trimmed string.
        """
        result = string.strip()
        logger.info(f"Trimmed string '{string}': {result}")
        return result

    @keyword("Trim Left")
    def trim_left(self, string):
        """
        Removes leading whitespace from a string.

        Args:
            string (str): The string to trim.

        Returns:
            str: The left-trimmed string.
        """
        result = string.lstrip()
        logger.info(f"Left-trimmed string '{string}': {result}")
        return result

    @keyword("Trim Right")
    def trim_right(self, string):
        """
        Removes trailing whitespace from a string.

        Args:
            string (str): The string to trim.

        Returns:
            str: The right-trimmed string.
        """
        result = string.rstrip()
        logger.info(f"Right-trimmed string '{string}': {result}")
        return result

    @keyword("Count Digits In String")
    def count_digits_in_string(self, string):
        """
        Counts the number of digits in a string.

        Args:
            string (str): The string to count digits in.

        Returns:
            int: The count of digits.
        """
        digits = re.findall(r"\d", string)
        count = len(digits)
        logger.info(f"Counted digits in '{string}': {count}")
        return count

    @keyword("Count Non English Characters")
    def count_non_english_characters(self, string):
        """
        Counts the number of non-English characters in a string.

        Args:
            string (str): The string to count non-English characters in.

        Returns:
            int: The count of non-English characters.
        """
        non_english_chars = re.findall(r"[^A-Za-z0-9\s]", string)
        count = len(non_english_chars)
        logger.info(f"Counted non-English characters in '{string}': {count}")
        return count

    @keyword("Extract Arabic Characters")
    def extract_arabic_characters(self, string):
        """
        Extracts all Arabic characters from a string.

        Args:
            string (str): The string to extract Arabic characters from.

        Returns:
            list: A list of extracted Arabic characters.
        """
        arabic_chars = re.findall(r"[\u0600-\u06FF]", string)
        logger.info(f"Extracted Arabic characters from '{string}': {arabic_chars}")
        return arabic_chars

    @keyword("Convert Number To Arabic")
    def convert_number_to_arabic(self, number):
        """
        Converts a number to Arabic numeral format.

        Args:
            number (int/float/str): The number to convert.

        Returns:
            str: The number in Arabic numeral format.
        """
        arabic_numerals = {
            "0": "٠",
            "1": "١",
            "2": "٢",
            "3": "٣",
            "4": "٤",
            "5": "٥",
            "6": "٦",
            "7": "٧",
            "8": "٨",
            "9": "٩"
        }
        result = "".join([arabic_numerals[char] for char in str(number)])
        logger.info(f"Converted number '{number}' to Arabic format: {result}")
        return result

    @keyword("Convert Arabic To Number")
    def convert_arabic_to_number(self, arabic_number):
        """
        Converts a number in Arabic numeral format to standard format.

        Args:
            arabic_number (str): The number in Arabic numeral format.

        Returns:
            str: The number in standard format.
        """
        standard_numerals = {
            "٠": "0",
            "١": "1",
            "٢": "2",
            "٣": "3",
            "٤": "4",
            "٥": "5",
            "٦": "6",
            "٧": "7",
            "٨": "8",
            "٩": "9"
        }
        result = "".join([standard_numerals[char] for char in arabic_number])
        logger.info(f"Converted Arabic number '{arabic_number}' to standard format: {result}")
        return result

    @keyword("Convert Digit String To Float String")
    def convert_to_float_and_back_to_string(self, digit_string):
        """
        Converts a string containing an integer to float and then returns it as a string.

        Args:
            digit_string (str): A string containing an integer value

        Returns:
            str: The float value converted back to string

        Raises:
            ValueError: If the input string cannot be converted to a float
        """
        try:
            # First convert to int, then to float
            int_value = int(digit_string)
            float_value = float(int_value)
            return str(float_value)
        except ValueError:
            raise ValueError(f"Could not convert '{digit_string}' to int then float")
