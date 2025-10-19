from robot.api import logger
from robot.api.deco import keyword, library
import re


@library(doc_format = 'ROBOT')
class MathOperations:
    def __init__(self, force_return_type = None):
        """
        Initializes the MathOperations library.

        Args:
            force_return_type (str, optional): If specified, forces all operations to return this type.
                                              Valid values are 'int', 'float', 'str', or None (default).
        """
        self.force_return_type = force_return_type

    @keyword("Add Numbers")
    def add_numbers(self, num1, num2, return_type = None):
        """
        Adds two numbers.

        Arguments:
            num1         The first number.
            num2         The second number.
            return_type  Optional type for result. Valid values: 'int', 'float', 'str', or None (use default behavior).

        Returns the result of the addition with the specified type or same type as input when possible.
        """
        # Store original force_return_type
        original_force_type = self.force_return_type
        # Set temporary return type if specified
        if return_type:
            self.force_return_type = return_type
        original_types = [ type(num1), type(num2) ]
        num1, num2, target_type = self.convert_to_numbers_with_type(num1, num2)
        result = num1 + num2
        logger.info(f"Added {num1} and {num2}: {result}")

        # Convert to target type
        converted_result = self.convert_result_to_target_type(result, target_type, original_types)

        # Restore original force_return_type if temporary was set
        if return_type:
            self.force_return_type = original_force_type

        return converted_result

    @keyword("Subtract Numbers")
    def subtract_numbers(self, num1, num2, return_type = None):
        """
        Subtracts the second number from the first number.

        Arguments:
            num1         The first number.
            num2         The second number.
            return_type  Optional type for result. Valid values: 'int', 'float', 'str', or None (use default behavior).

        Returns the result of the subtraction with the specified type or same type as input when possible.
        """
        # Store original force_return_type
        original_force_type = self.force_return_type
        # Set temporary return type if specified
        if return_type:
            self.force_return_type = return_type

        original_types = [ type(num1), type(num2) ]
        num1, num2, target_type = self.convert_to_numbers_with_type(num1, num2)
        result = num1 - num2
        logger.info(f"Subtracted {num2} from {num1}: {result}")

        # Convert to target type
        converted_result = self.convert_result_to_target_type(result, target_type, original_types)

        # Restore original force_return_type if temporary was set
        if return_type:
            self.force_return_type = original_force_type

        return converted_result

    @keyword("Multiply Numbers")
    def multiply_numbers(self, num1, num2, return_type = None):
        """
        Multiplies two numbers.

        Arguments:
            num1         The first number.
            num2         The second number.
            return_type  Optional type for result. Valid values: 'int', 'float', 'str', or None (use default behavior).

        Returns the result of the multiplication with the specified type or same type as input when possible.
        """
        # Store original force_return_type
        original_force_type = self.force_return_type
        # Set temporary return type if specified
        if return_type:
            self.force_return_type = return_type

        original_types = [ type(num1), type(num2) ]
        num1, num2, target_type = self.convert_to_numbers_with_type(num1, num2)
        result = num1 * num2
        logger.info(f"Multiplied {num1} and {num2}: {result}")

        # Convert to target type
        converted_result = self.convert_result_to_target_type(result, target_type, original_types)

        # Restore original force_return_type if temporary was set
        if return_type:
            self.force_return_type = original_force_type

        return converted_result

    @keyword("Divide Numbers")
    def divide_numbers(self, num1, num2, return_type = None):
        """
        Divides the first number by the second number.

        Arguments:
            num1         The first number.
            num2         The second number.
            return_type  Optional type for result. Valid values: 'int', 'float', 'str', or None (use default behavior).

        Returns the result of the division with the specified type or same type as input when possible.
        """
        # Store original force_return_type
        original_force_type = self.force_return_type
        # Set temporary return type if specified
        if return_type:
            self.force_return_type = return_type

        original_types = [ type(num1), type(num2) ]
        num1, num2, target_type = self.convert_to_numbers_with_type(num1, num2)
        if num2 == 0:
            raise ValueError("Division by zero is not allowed.")
        result = num1 / num2
        logger.info(f"Divided {num1} by {num2}: {result}")

        # Convert to target type
        converted_result = self.convert_result_to_target_type(result, target_type, original_types)

        # Restore original force_return_type if temporary was set
        if return_type:
            self.force_return_type = original_force_type

        return converted_result

    @keyword("Toggle Sign")
    def toggle_sign(self, num, return_type = None):
        """
        Toggles the sign of a number (positive to negative or vice versa).

        Arguments:
            num          The number to toggle.
            return_type  Optional type for result. Valid values: 'int', 'float', 'str', or None (use default behavior).

        Returns the number with toggled sign with the specified type or same type as input when possible.
        """
        # Store original force_return_type
        original_force_type = self.force_return_type
        # Set temporary return type if specified
        if return_type:
            self.force_return_type = return_type

        original_type = type(num)
        num, _ = self.convert_to_number_with_type(num)
        result = -num
        logger.info(f"Toggled sign of {num}: {result}")

        # Convert to target type
        converted_result = self.convert_result_to_target_type(result, None, [ original_type ])

        # Restore original force_return_type if temporary was set
        if return_type:
            self.force_return_type = original_force_type

        return converted_result

    @keyword("Format Decimal To Fixed Integer")
    def format_decimal_to_fixed_integer(self, num, decimal_places = 0):
        """
        Formats a decimal number to a fixed integer.

        Arguments:
            num              The number to format.
            decimal_places   The number of decimal places to round to.

        Returns the formatted integer.
        """
        num, _ = self.convert_to_number_with_type(num)
        result = int(round(num, decimal_places))
        logger.info(f"Formatted {num} to fixed integer: {result}")
        return result

    @keyword("Format Fixed Number To Decimal")
    def format_fixed_number_to_decimal(self, num, decimal_places = 2):
        """
        Formats a fixed number to a decimal.

        Arguments:
            num              The number to format.
            decimal_places   The number of decimal places to round to.

        Returns the formatted decimal.
        """
        num, _ = self.convert_to_number_with_type(num)
        result = round(float(num), decimal_places)
        logger.info(f"Formatted {num} to decimal: {result}")
        return result

    @keyword("Division Remainder")
    def division_remainder(self, num1, num2, return_type = None):
        """
        Returns the remainder of dividing the first number by the second number.

        Arguments:
            num1         The first number.
            num2         The second number.
            return_type  Optional type for result. Valid values: 'int', 'float', 'str', or None (use default behavior).

        Returns the remainder of the division with the specified type or same type as input when possible.
        """
        # Store original force_return_type
        original_force_type = self.force_return_type
        # Set temporary return type if specified
        if return_type:
            self.force_return_type = return_type

        original_types = [ type(num1), type(num2) ]
        num1, num2, target_type = self.convert_to_numbers_with_type(num1, num2)
        if num2 == 0:
            raise ValueError("Division by zero is not allowed.")
        result = num1 % num2
        logger.info(f"Remainder of {num1} divided by {num2}: {result}")

        # Convert to target type
        converted_result = self.convert_result_to_target_type(result, target_type, original_types)

        # Restore original force_return_type if temporary was set
        if return_type:
            self.force_return_type = original_force_type

        return converted_result

    @keyword("Evaluate Expression")
    def evaluate_expression(self, expression):
        """
        Evaluates a mathematical or logical expression following standard rules.

        Arguments:
            expression    The expression to evaluate (e.g., "7+8*5 > 40" or "10 < 20 and 5 == 5").

        Returns the result of the evaluated expression (boolean for logical expressions, numeric for mathematical expressions).
        """
        # Validate the expression to ensure it only contains numbers, operators, and spaces
        if not self.is_valid_expression(expression):
            raise ValueError(f"Invalid expression: {expression}")

        try:
            # Evaluate the expression using Python's built-in eval()
            result = eval(expression)
            logger.info(f"Evaluated expression '{expression}': {result}")

            # Try to maintain type consistency if result is numeric
            if isinstance(result, (int, float)) and not isinstance(result, bool):
                # Try to convert to int if it's a whole number
                if result == int(result):
                    result = int(result)

            return result
        except Exception as e:
            logger.error(f"Failed to evaluate expression: {e}")
            raise ValueError(f"Failed to evaluate expression: {e}")

    def is_valid_expression(self, expression):
        """
        Validates the expression to ensure it only contains numbers, operators, and spaces.

        Args:
            expression (str): The expression to validate.

        Returns:
            bool: True if the expression is valid, otherwise False.
        """
        # Regular expression to match valid mathematical and logical expressions
        pattern = r"^[\d\s\+\-\*\/\.\(\)<>=!&|]+$"
        return bool(re.match(pattern, expression))

    def convert_to_numbers_with_type(self, num1, num2):
        """
        Converts two inputs to numbers while tracking original types.

        Args:
            num1: The first input.
            num2: The second input.

        Returns:
            tuple: Two numbers and target type.
        """
        num1_val, num1_type = self.convert_to_number_with_type(num1)
        num2_val, num2_type = self.convert_to_number_with_type(num2)

        # Determine target type (precedence: float > int > str)
        if float in [ num1_type, num2_type ]:
            target_type = float
        else:
            target_type = int

        return num1_val, num2_val, target_type

    def convert_to_number_with_type(self, num):
        """
        Converts an input to a number while tracking original type.

        Args:
            num: The input to convert.

        Returns:
            tuple: The converted number and its original type.
        """
        if isinstance(num, str):
            try:
                # Handle decimal numbers
                if "." in num:
                    return float(num), float
                else:
                    # Use regular int() without base specification but first make
                    # sure we strip any leading zeros to avoid octal interpretation
                    cleaned_num = num.lstrip('0')
                    # If it was all zeros, return 0
                    if not cleaned_num:
                        return 0, int
                    return int(cleaned_num), int
            except ValueError as e:
                raise ValueError(f"Could not convert string '{num}' to a number: {str(e)}")
        elif isinstance(num, int):
            return num, int
        elif isinstance(num, float):
            return num, float
        else:
            raise ValueError(f"Invalid input type: {type(num)}")

    def convert_result_to_target_type(self, result, target_type, original_types):
        """
        Converts the result to the most appropriate type based on inputs.

        Args:
            result: The calculation result.
            target_type: The target numeric type (int or float).
            original_types: List of original input types.

        Returns:
            The result converted to the appropriate type.
        """
        # First check if force_return_type is set
        if self.force_return_type:
            if self.force_return_type == 'int':
                return int(result) if result == int(result) else int(round(result))
            elif self.force_return_type == 'float':
                return float(result)
            elif self.force_return_type == 'str':
                # For strings, avoid decimal point if it's a whole number
                if result == int(result):
                    return str(int(result))
                return str(result)

        # Check if result is a whole number
        is_whole_number = result == int(result)

        # If all inputs were strings
        if all(t == str for t in original_types):
            # If it's a whole number, return string without decimal
            if is_whole_number:
                return str(int(result))
            return str(result)

        # If result is a whole number, prefer int representation
        if is_whole_number:
            # Even for division which normally returns float, convert to int
            return int(result)

        # If one of the inputs was a float, or the result cannot be expressed as an int
        if float in original_types or target_type == float:
            return float(result)

        # Default to int for whole numbers (should not reach here if above logic is correct)
        return int(result) if is_whole_number else float(result)

    def convert_to_number(self, num):
        """
        Legacy method for backward compatibility.

        Args:
            num: The input to convert.

        Returns:
            The converted number.
        """
        val, _ = self.convert_to_number_with_type(num)
        return val

    def convert_to_numbers(self, num1, num2):
        """
        Legacy method for backward compatibility.

        Args:
            num1: The first input.
            num2: The second input.

        Returns:
            tuple: Two converted numbers.
        """
        n1, n2, _ = self.convert_to_numbers_with_type(num1, num2)
        return n1, n2
