import random
import math
from Libraries.Variables.Cities import *
from datetime import datetime
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn


@library(doc_format='ROBOT')
class Generators:
    def __init__(self):
        self.cities = CITIES
        self.card = ''
        self.expiry_date = ''
        self.cvv = ''
        self.city = ''
        self.address = ''
        self.postal_code = ''

    def generate_random_address(self):
        """Generate a random city, address, and postal code in Saudi Arabia."""
        self.city = random.choice(self.cities)
        self.address = f"{random.randint(1, 9999)} {self.city} St"
        self.postal_code = f"{random.randint(10000, 99999)}"
        return self.city, self.address, self.postal_code

    def generate_expiry_date(self):
        """Generate a random expiry date."""
        now = datetime.now()
        current_month = now.month
        current_year = now.year % 100  # Get last two digits of the year (e.g., 25 for 2025)

        # Generate a future expiry date
        while True:
            month = random.randint(1, 12)
            year = random.randint(current_year, current_year + 5)  # 5-year range

            if (year > current_year) or (year == current_year and month > current_month):
                break  # Ensure the expiry date is after the current month

        self.expiry_date = f"{str(month).zfill(2)}/{year}"
        return self.expiry_date

    def generate_cvv(self):
        """Generate a random CVV."""
        self.cvv = ''.join(random.choices("0123456789", k=3))
        return self.cvv

    @keyword("Generate Random PyNumber")
    def generate_random_py_number(self, range_min=None,
                                  range_max=None,
                                  number_of_digits=None,
                                  output_type="int",
                                  prefix=""):
        """
        Generates a random number based on the provided range, number of digits, or both.

        :param int range_min: Minimum value for the random number (optional).
        :param int range_max: Maximum value for the random number (optional).
        :param int number_of_digits: Exact number of digits for the generated number (optional).
        :param str output_type: Output type ("int" (default), "float", or "string").
        :param str prefix: String to prepend to the result (optional, forces string output).

        :return: The generated number, formatted based on `output_type`. If `prefix` is provided, the result is returned as a string.
        :rtype: int, float, or str

        :raises ValueError: If no valid number can be generated based on the inputs.
        """
        # Case 1: When both range_min/range_max and number_of_digits are provided
        if range_min is not None or range_max is not None:
            if number_of_digits is not None:
                # Ensure range respects the number of digits
                range_min = max(range_min or 0, 10 ** (
                        number_of_digits - 1))  # Ensure minimum is at least the smallest number with given digits
                range_max = min(range_max * 10 ** (number_of_digits - 1),
                                (10 ** number_of_digits) - 1)  # Ensure maximum doesn't exceed number_of_digits

                # Ensure valid ranges
                if range_min > range_max:
                    raise ValueError(f"Cannot generate a {number_of_digits}-digit number in the given range.")
            else:
                # If only range_min and range_max are provided, just generate a number within the range
                range_min = range_min or 0
                range_max = range_max or 10
            # Generate a number within the adjusted range
            if output_type == "float":
                number = random.uniform(range_min, range_max)
            else:
                number = random.randint(range_min, range_max)

        # Case 2: If only number_of_digits is provided, generate a number with the exact number of digits
        elif number_of_digits is not None:
            if number_of_digits < 1:
                raise ValueError("Number of digits must be at least 1")
            range_min = 10 ** (number_of_digits - 1)
            range_max = (10 ** number_of_digits) - 1
            number = random.randint(range_min, range_max)

        # Case 3: Error if neither range nor number_of_digits is provided
        else:
            raise ValueError("You must provide either a range (range_min, range_max) or number_of_digits.")

        # Convert the number based on the requested output type
        if output_type == "int":
            number = int(number)
        elif output_type == "float":
            number = float(number)
        elif output_type == "string":
            number = str(int(number))  # Convert to string from an integer

        # If a prefix is provided, always return the result as a string
        if prefix:
            return f"{prefix}{number}"

        # Return the result in its native type (int, float, or string)
        return number
