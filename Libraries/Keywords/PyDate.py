import random
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn


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
