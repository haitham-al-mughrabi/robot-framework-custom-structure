from robot.api.deco import keyword, library
import operator


@library(doc_format='ROBOT')
class CustomConditioning:
    """
    A custom Robot Framework library for handling dynamic conditional evaluations
    and comparisons for strings and numbers.
    """

    @keyword(name="Dynamic IF")
    def dynamic_if(self, condition, **variables):
        """
        Dynamically evaluates a condition and returns its result using eval.

        :param condition: The condition to evaluate as a string (e.g., "x + y if x > y else y").
        :param variables: Keyword arguments representing the variables used in the condition.
        :return: The result of the evaluated condition.
        """
        # Evaluate the condition in the context of the provided variables
        return eval(condition, {}, variables)

    @keyword(name="Inline IF")
    def inline_if(self, condition, condition_satisfied, condition_failed):
        """
        Dynamically evaluates and returns a value based on a given condition.

        Arguments:
        - condition: A boolean value to determine which value to return.
        - condition_satisfied: The value to return if the condition is `True`.
        - condition_failed: The value to return if the condition is `False`.

        Returns:
        - The `condition_satisfied` value if the condition is `True`, otherwise the `condition_failed` value.

        Example:
        | ${result} = | Inline IF | ${5 > 3} | "Greater" | "Smaller" |
        | Should Be Equal | ${result} | Greater |
        """
        return condition_satisfied if condition else condition_failed

    @keyword(name="Compare Strings")
    def dynamic_string_comparator(self, string1: str = "", string2: str = "", operator_sign: str = "==",
                                  case_transform1: str = "none", case_transform2: str = "none") -> bool:
        """
        Compares two strings based on a given comparison operator with optional case transformation.

        Arguments:
        - string1: The first string to compare. Default is an empty string.
        - string2: The second string to compare. Default is an empty string.
        - operator_sign: A comparison operator (`==`, `!=`, `<`, `<=`, `>`, `>=`). Default is `==`.
        - case_transform1: Case transformation for `string1`. Options: "lower", "upper", "none". Default is "none".
        - case_transform2: Case transformation for `string2`. Options: "lower", "upper", "none". Default is "none".

        Returns:
        - `True` if the comparison satisfies the condition, otherwise `False`.

        Raises:
        - ValueError: If an invalid operator or case transformation option is provided.

        Example:
        | dynamic_string_comparator("Apple", "apple", "==", "lower", "lower") → True
        | dynamic_string_comparator("Test", "test", "!=", "upper", "none") → True
        """
        operators = {
            "==": operator.eq,
            "!=": operator.ne,
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge
        }

        if operator_sign not in operators:
            raise ValueError(f"Invalid operator: {operator_sign}")

        case_transform_options = {"lower": str.lower, "upper": str.upper, "none": lambda x: x}

        if case_transform1 not in case_transform_options or case_transform2 not in case_transform_options:
            raise ValueError("Invalid case transform option. Use 'lower', 'upper', or 'none'.")

        string1 = case_transform_options[case_transform1](string1)
        string2 = case_transform_options[case_transform2](string2)

        return operators[operator_sign](string1, string2)

    @keyword(name="Compare Numbers")
    def dynamic_number_comparator(self, num1, num2, operator_sign):
        """
        Dynamically compares two numbers based on a given comparison operator.

        Supports integers, floats, and string representations of numbers.

        Arguments:
        - num1: The first number to compare (int, float, or string representation of a number).
        - num2: The second number to compare (int, float, or string representation of a number).
        - operator_sign: A comparison operator (`==`, `!=`, `<`, `<=`, `>`, `>=`).

        Returns:
        - `True` if the comparison satisfies the condition, otherwise `False`.

        Raises:
        - ValueError: If the inputs are not numeric or the operator is invalid.
        - RuntimeError: If an error occurs during evaluation.

        Example:
        | ${result} = | Compare Numbers | 10.5 | 20.3 | "<" |
        | Should Be Equal | ${result} | True |

        Edge Cases:
        - Handles mixed numeric types (e.g., int and float).
        - Example: Compare Numbers | 5 | 5.0 | "==" | → True
        - Validates operator correctness before attempting evaluation.
        """
        # Ensure both numbers are floats (to handle all numeric types seamlessly)
        try:
            num1 = float(num1)
            num2 = float(num2)
        except ValueError:
            raise ValueError(f"Invalid number(s) provided: num1='{num1}', num2='{num2}'")

        # List of supported operators
        supported_operators = ["==", "!=", "<", "<=", ">", ">="]

        # Validate the operator
        if operator_sign not in supported_operators:
            raise ValueError(
                f"Invalid operator '{operator_sign}' provided. Supported operators: {', '.join(supported_operators)}"
            )

        # Dynamically construct and evaluate the comparison expression
        expression = f"{num1} {operator_sign} {num2}"
        try:
            result = eval(expression)
            return result
        except Exception as e:
            raise RuntimeError(f"Error evaluating expression: {expression}. Error: {str(e)}")

    @keyword(name="Dynamic Conditional")
    def dynamic_conditional(self, expression_list, context=None, else_value=None):
        """
        Dynamically evaluates a series of if-elif-else conditions with variable support.

        Arguments:
        - expression_list: A list of tuples where each tuple contains a condition as a string
                           and a corresponding result value.
                           Format: [(condition1, result1), (condition2, result2), ...]
        - context: A dictionary of variables to be used in condition evaluation (default: None).
        - else_value: The value to return if none of the conditions are satisfied (default: None).

        Returns:
        - The result corresponding to the first condition that evaluates to `True`.
          If no conditions are `True`, returns the `else_value`.

        Raises:
        - ValueError: If the conditions are not valid or evaluation fails.

        Example:
        | ${result} = | Dynamic Conditional |
        | ...         | [("x > 3", "Greater"), ("x < 3", "Smaller")] | {"x": 5} |
        | Should Be Equal | ${result} | Greater |
        """
        context = context or {}

        for condition, result in expression_list:
            if isinstance(condition, str):
                condition = f'"{condition}"' if " " in condition else condition
            try:
                if eval(condition, {}, context):
                    return result
            except Exception as e:
                raise ValueError(f"Error evaluating condition: '{condition}'. Error: {str(e)}")

        return else_value

    @keyword("Create Lambda")
    def create_lambda(self, *variables, expression):
        """
           Create a dynamic lambda function with any number of inputs and a custom expression.

           :param variables: Variable names for the lambda function (e.g., "x", "y", "z").
           :param expression: The string expression to evaluate in the lambda body.
           :return: A dynamically created lambda function.
           """
        # Join variables into a single comma-separated string
        variables_string = ", ".join(variables)

        # Construct the lambda dynamically
        lambda_code = f"lambda {variables_string}: {expression}"

        # Evaluate and return the lambda function
        return eval(lambda_code)
