from datetime import datetime, timedelta
import random
from robot.api.deco import keyword, library
from robot.api import logger
from Libraries.Variables.Date import FORMATS


@library(doc_format='ROBOT')
class BirthdateGenerator:
    """
    A class that provides keywords for generating birthdates for people 18 years or older.
    This class can be used with Robot Framework to generate valid birthdates
    in various formats for testing purposes.
    """

    def __init__(self):
        self.date_formats = FORMATS

    @keyword("Generate Adult Birthdate")
    def generate_adult_birthdate(self, min_age=18, max_age=80, format='yyyy-mm-dd'):
        """
        Generates a random birthdate for a person with an age between min_age and max_age.

        Arguments:
        - min_age: Minimum age of the person (default: 18)
        - max_age: Maximum age of the person (default: 100)
        - format: Date format, supports common formats (default: yyyy-mm-dd)

        Available formats:
        - yyyy-mm-dd (e.g., 2003-05-15)
        - mm/dd/yyyy (e.g., 05/15/2003)
        - dd/mm/yyyy (e.g., 15/05/2003)
        - dd-mm-yyyy (e.g., 15-05-2003)
        - mm-dd-yyyy (e.g., 05-15-2003)
        - yyyy/mm/dd (e.g., 2003/05/15)
        - mmddyyyy (e.g., 05152003)
        - yyyymmdd (e.g., 20030515)

        Returns:
        - A string containing the birthdate in the specified format

        Example:
        | ${birthdate} = | Generate Adult Birthdate | min_age=21 | format=mm/dd/yyyy |
        """
        # Convert to integers just in case they're passed as strings
        min_age = int(min_age)
        max_age = int(max_age)

        # Validate age range
        if min_age < 0 or max_age < min_age:
            raise ValueError(f"Invalid age range: min_age={min_age}, max_age={max_age}")

        # Validate format
        if format.lower() not in self.date_formats:
            valid_formats = ', '.join(self.date_formats.keys())
            raise ValueError(f"Invalid format: {format}. Valid formats are: {valid_formats}")

        # Get current date
        today = datetime.now()

        # Calculate the date range
        earliest_date = today - timedelta(days=365.25 * max_age)
        latest_date = today - timedelta(days=365.25 * min_age)

        # Convert to timestamps for random generation
        earliest_ts = earliest_date.timestamp()
        latest_ts = latest_date.timestamp()

        # Generate a random timestamp in the range
        random_ts = random.uniform(earliest_ts, latest_ts)
        random_date = datetime.fromtimestamp(random_ts)

        # Account for leap years and invalid dates
        try:
            # Ensure the date is valid (e.g., not February 29 in a non-leap year)
            random_date = datetime(random_date.year, random_date.month, random_date.day)
        except ValueError:
            # If the date is invalid, adjust it to a valid date
            if random_date.month == 2 and random_date.day == 29:
                random_date = datetime(random_date.year, 2, 28)

        # Format the date according to the specified format
        date_format = self.date_formats[format.lower()]
        formatted_date = random_date.strftime(date_format)

        logger.info(f"Generated birthdate: {formatted_date} (age: {self._calculate_age(random_date)} years)")
        return formatted_date

    def get_available_date_formats(self):
        """
        Returns a list of all available date formats supported by the BirthdateGenerator.

        Returns:
        - A list of strings representing the supported date formats

        Example:
        | ${formats} = | Get Available Date Formats |
        """
        return list(self.date_formats.keys())

    def _calculate_age(self, birthdate):
        """
        Calculate the age in years for a given birthdate.

        Arguments:
        - birthdate: A datetime object representing the birthdate

        Returns:
        - An integer representing the age in years
        """
        today = datetime.now()
        age = today.year - birthdate.year

        # Adjust age if birthday hasn't occurred yet this year
        if (today.month, today.day) < (birthdate.month, birthdate.day):
            age -= 1

        return age
