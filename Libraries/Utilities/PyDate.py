import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from typing import Dict, Union, Optional
import re


@library(doc_format='ROBOT')
class PyDate:
    def __init__(self):
        self.builtin = BuiltIn()
        self.year_to_start = None
        self.month_to_start = None
        self.back_years = None
        self.back_months = None
        self.date_format = "%Y-%m-%d"

    @keyword("Add Random Months")
    def add_random_months(self, number_of_months: int, date_format: str = '%Y-%m-%d') -> str:
        """
        Add a random number of months to the current date based on the provided range,
        ensuring that the result is at least one month in the future.
        :param number_of_months: Maximum number of months to add
        :param date_format: The format in which to return the date
        :return: The new date as a formatted string
        """
        # Get current date
        current_date = datetime.now()

        # Ensure number_of_months is positive and set a default random range if needed
        if number_of_months <= 0:
            number_of_months = random.randint(1, 30)

        # Generate a random number of months within the specified range, starting from 1
        random_months = random.randint(1, number_of_months)

        # Add the random number of months to the current date
        new_date = current_date + relativedelta(months=random_months)

        # Return the formatted date
        return new_date.strftime(date_format)

    @keyword("Generate Random Birthdate")
    def generate_random_birthdate(self, year_to_start=None, month_to_start=None, back_years=None,
                                  back_months=None, date_format="%Y-%m-%d"):
        """
        Generate Random Birth Date Based On Provided Data.
        :param year_to_start: Starting year for calculation (default: current year).
        :param month_to_start: Starting month for calculation (default: current month).
        :param back_years: Number of years to go back (default: random 1 to 50).
        :param back_months: Number of months to go back within the year (default: random 0 to 11).
        :param date_format: The format in which to return the date.
        :return: Random birth date as a formatted string.
        """
        # Set starting year and month
        self.year_to_start = year_to_start if year_to_start is not None else datetime.now().year
        self.month_to_start = month_to_start if month_to_start is not None else datetime.now().month
        self.back_years = back_years if back_years is not None else random.randint(1, 50)
        self.back_months = back_months if back_months is not None else random.randint(0, 11)
        self.date_format = date_format

        # If month provided as string, convert to month number
        if isinstance(self.month_to_start, str):
            self.month_to_start = datetime.strptime(self.month_to_start, "%B").month

        # Calculate start date and subtract years and months
        start_date = datetime(self.year_to_start, self.month_to_start, 1)
        start_date -= relativedelta(years=self.back_years, months=self.back_months)

        # Calculate end of month for the target month
        end_of_month = (start_date + relativedelta(months=1)) - timedelta(days=1)

        # Generate a random day within that month
        random_day = random.randint(1, end_of_month.day)
        random_date = datetime(start_date.year, start_date.month, random_day)

        return random_date.strftime(self.date_format)

    @keyword("Parse Date")
    def parse_date(self, date_input: Union[str, datetime],
                   format_string: Optional[str] = None) -> Dict[str, Union[int, str, None]]:
        """
        Parse a date string or datetime object and return its components as a dictionary.

        Args:
            date_input: A string representation of a date or a datetime object
            format_string: Optional format string to use for parsing (if date_input is a string)
                          Example: "%Y-%m-%d %H:%M:%S"

        Returns:
            A dictionary containing the date components:
            {
                'day': int,
                'month': int,
                'year': int,
                'hour': int or None,
                'minute': int or None,
                'second': int or None,
                'microsecond': int or None,
                'timezone': str or None
            }
        """
        # Initialize the result dictionary with None values
        result = {
            'day': None,
            'month': None,
            'year': None,
            'hour': None,
            'minute': None,
            'second': None,
            'microsecond': None,
            'timezone': None
        }

        # Convert input to datetime object
        dt = None

        if isinstance(date_input, datetime):
            dt = date_input
        elif isinstance(date_input, str):
            try:
                if format_string:
                    dt = datetime.strptime(date_input, format_string)
                else:
                    # Try to use a simple regex pattern to detect common date formats
                    # This is a fallback if dateutil is not available
                    date_patterns = [
                        # ISO format: YYYY-MM-DD
                        r"(\d{4})-(\d{1,2})-(\d{1,2})",
                        # US format: MM/DD/YYYY
                        r"(\d{1,2})/(\d{1,2})/(\d{4})",
                        # European format: DD.MM.YYYY
                        r"(\d{1,2})\.(\d{1,2})\.(\d{4})",
                    ]

                    for pattern in date_patterns:
                        match = re.search(pattern, date_input)
                        if match:
                            if pattern == date_patterns[0]:  # ISO
                                year, month, day = map(int, match.groups())
                            elif pattern == date_patterns[1]:  # US
                                month, day, year = map(int, match.groups())
                            elif pattern == date_patterns[2]:  # European
                                day, month, year = map(int, match.groups())

                            dt = datetime(year, month, day)

                            # Try to extract time if present
                            time_match = re.search(r"(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?", date_input)
                            if time_match:
                                hour, minute = map(int, time_match.groups()[:2])
                                second = int(time_match.groups()[2]) if time_match.groups()[2] else 0
                                dt = dt.replace(hour=hour, minute=minute, second=second)

                            # Try to extract timezone if present
                            tz_match = re.search(r"([+-])(\d{2}):?(\d{2})", date_input)
                            if tz_match:
                                sign, tz_hour, tz_minute = tz_match.groups()
                                result['timezone'] = f"{sign}{tz_hour}:{tz_minute}"

                            break

                    # If no pattern matched, try to use the specified format or fail
                    if dt is None:
                        try:
                            # Try to import dateutil for more flexible parsing
                            from dateutil import parser as dateutil_parser
                            dt = dateutil_parser.parse(date_input)
                        except (ImportError, ValueError):
                            raise ValueError(f"Failed to parse date: {date_input}")
            except (ValueError, TypeError) as e:
                raise ValueError(f"Failed to parse date: {e}")
        else:
            raise TypeError("date_input must be a string or datetime object")

        # Extract date components
        result['day'] = dt.day
        result['month'] = dt.month
        result['year'] = dt.year

        # Extract time components if present
        if dt.hour != 0 or dt.minute != 0 or dt.second != 0 or dt.microsecond != 0:
            result['hour'] = dt.hour
            result['minute'] = dt.minute
            result['second'] = dt.second

            if dt.microsecond != 0:
                result['microsecond'] = dt.microsecond

        # Extract timezone if present
        if dt.tzinfo:
            offset = dt.utcoffset()
            if offset:
                hours, remainder = divmod(int(offset.total_seconds()), 3600)
                minutes = remainder // 60
                sign = '+' if hours >= 0 else '-'
                result['timezone'] = f"{sign}{abs(hours):02d}:{minutes:02d}"
            else:
                result['timezone'] = str(dt.tzinfo)

        return result
