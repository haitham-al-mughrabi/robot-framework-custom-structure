from robot.api import logger
from robot.api.deco import keyword, library
from MathOperations import MathOperations


@library(doc_format='ROBOT')
class LogicalOperations:
    def __init__(self):
        self.MathOperations = MathOperations()

    @keyword("Less Than")
    def less_than(self, num1, num2):
        """
        Checks if the first number is less than the second number.

        Args:
            num1 (int/float/str): The first number.
            num2 (int/float/str): The second number.

        Returns:
            bool: True if num1 < num2, otherwise False.
        """
        num1, num2 = self.MathOperations.convert_to_numbers(num1, num2)
        return num1 < num2

    @keyword("Less Than Or Equal To")
    def less_than_or_equal_to(self, num1, num2):
        """
        Checks if the first number is less than or equal to the second number.

        Args:
            num1 (int/float/str): The first number.
            num2 (int/float/str): The second number.

        Returns:
            bool: True if num1 <= num2, otherwise False.
        """
        num1, num2 = self.MathOperations.convert_to_numbers(num1, num2)
        return num1 <= num2

    @keyword("Bigger Than")
    def bigger_than(self, num1, num2):
        """
        Checks if the first number is greater than the second number.

        Args:
            num1 (int/float/str): The first number.
            num2 (int/float/str): The second number.

        Returns:
            bool: True if num1 > num2, otherwise False.
        """
        num1, num2 = self.MathOperations.convert_to_numbers(num1, num2)
        return num1 > num2

    @keyword("Bigger Than Or Equal To")
    def bigger_than_or_equal_to(self, num1, num2):
        """
        Checks if the first number is greater than or equal to the second number.

        Args:
            num1 (int/float/str): The first number.
            num2 (int/float/str): The second number.

        Returns:
            bool: True if num1 >= num2, otherwise False.
        """
        num1, num2 = self.MathOperations.convert_to_numbers(num1, num2)
        return num1 >= num2

    @keyword("Equal")
    def equal(self, num1, num2):
        """
        Checks if two numbers are equal.

        Args:
            num1 (int/float/str): The first number.
            num2 (int/float/str): The second number.

        Returns:
            bool: True if num1 == num2, otherwise False.
        """
        num1, num2 = self.MathOperations.convert_to_numbers(num1, num2)
        return num1 == num2

    @keyword("Not Equal")
    def not_equal(self, num1, num2):
        """
        Checks if two numbers are not equal.

        Args:
            num1 (int/float/str): The first number.
            num2 (int/float/str): The second number.

        Returns:
            bool: True if num1 != num2, otherwise False.
        """
        num1, num2 = MathOperations().convert_to_numbers(num1, num2)
        return num1 != num2
