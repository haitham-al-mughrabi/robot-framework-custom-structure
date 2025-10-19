from robot.api.deco import keyword, library
from typing import Any, Type, Union, Tuple
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn


@library(doc_format='ROBOT')
class VariableUtils:
    """
    A utility class to check if a variable is None, get its type, and perform related operations.
    This class is designed to be used as a library in Robot Framework.
    """

    def __init__(self):
        self.builtin = BuiltIn()

    @keyword(name="Is None")
    def is_none(self, variable: Any) -> bool:
        """
        Check if the given variable is None.

        *Arguments:*
        - `variable`: The variable to check.

        *Returns:*
        - `bool`: True if the variable is None, False otherwise.

        *Example (Robot Framework):*
        | ${is_none}= | Is None | ${None} |
        | Should Be True | ${is_none} |
        """
        return variable is None

    @keyword(name="Is Not None")
    def is_not_none(self, variable: Any) -> bool:
        """
        Check if the given variable is not None.

        *Arguments:*
        - `variable`: The variable to check.

        *Returns:*
        - `bool`: True if the variable is not None, False otherwise.

        *Example (Robot Framework):*
        | ${is_not_none}= | Is Not None | ${42} |
        | Should Be True | ${is_not_none} |
        """
        return variable is not None

    @keyword(name="Get Variable Type")
    def get_variable_type(self, variable: Any) -> str:
        """
        Get the type of the given variable as a string.

        *Arguments:*
        - `variable`: The variable to check.

        *Returns:*
        - `str`: The type of the variable (e.g., "int", "str", "list").

        *Example (Robot Framework):*
        | ${type}= | Get Variable Type | ${42} |
        | Should Be Equal | ${type} | int |
        """
        return type(variable).__name__

    @keyword(name="Default If None")
    def default_if_none(self, variable: Any, default: Any) -> Any:
        """
        Return the variable if it is not None, otherwise return the default value.

        *Arguments:*
        - `variable`: The variable to check.
        - `default`: The default value to return if the variable is None.

        *Returns:*
        - The variable if it is not None, otherwise the default value.

        *Example (Robot Framework):*
        | ${result}= | Default If None | ${None} | Default Value |
        | Should Be Equal | ${result} | Default Value |
        """
        return variable if variable is not None else default

    @keyword(name="Raise If None")
    def raise_if_none(self, variable: Any, error_message: str = "Variable cannot be None"):
        """
        Raise an exception if the variable is None.

        *Arguments:*
        - `variable`: The variable to check.
        - `error_message` (str): The error message to raise if the variable is None.

        *Raises:*
        - `ValueError`: If the variable is None.

        *Example (Robot Framework):*
        | Raise If None | ${None} | Custom error message |
        """
        if variable is None:
            raise ValueError(error_message)

    @keyword(name="Check Variable Type")
    def check_variable_type(self, variable: Any, expected_type: Union[Type, Tuple[Type, ...]]) -> bool:
        """
        Check if the variable is of the expected type.

        *Arguments:*
        - `variable`: The variable to check.
        - `expected_type` (type or tuple of types): The expected type(s) of the variable.

        *Returns:*
        - `bool`: True if the variable is of the expected type, False otherwise.

        *Example (Robot Framework):*
        | ${is_int}= | Check Variable Type | ${42} | int |
        | Should Be True | ${is_int} |
        """
        return isinstance(variable, expected_type)

    @keyword(name="Check Variable Type Or None")
    def check_variable_type_or_none(self, variable: Any, expected_type: Union[Type, Tuple[Type, ...]]) -> bool:
        """
        Check if the variable is of the expected type or None.

        *Arguments:*
        - `variable`: The variable to check.
        - `expected_type` (type or tuple of types): The expected type(s) of the variable.

        *Returns:*
        - `bool`: True if the variable is of the expected type or None, False otherwise.

        *Example (Robot Framework):*
        | ${is_int_or_none}= | Check Variable Type Or None | ${None} | int |
        | Should Be True | ${is_int_or_none} |
        """
        return variable is None or isinstance(variable, expected_type)

    @keyword(name="Coalesce")
    def coalesce(self, *variables: Any) -> Any:
        """
        Return the first non-None value from the provided variables.

        *Arguments:*
        - `*variables`: Variable number of arguments to check.

        *Returns:*
        - The first non-None value, or None if all variables are None.

        *Example (Robot Framework):*
        | ${result}= | Coalesce | ${None} | ${None} | First Non-None | Second Non-None |
        | Should Be Equal | ${result} | First Non-None |
        """
        for var in variables:
            if var is not None:
                return var
        return None

    @keyword(name="Is Empty")
    def is_empty(self, variable: Any) -> bool:
        """
        Check if the variable is None or an empty collection (e.g., empty list, dict, or string).

        *Arguments:*
        - `variable`: The variable to check.

        *Returns:*
        - `bool`: True if the variable is None or empty, False otherwise.

        *Example (Robot Framework):*
        | ${is_empty}= | Is Empty | ${[]} |
        | Should Be True | ${is_empty} |
        """
        if variable is None:
            return True
        if isinstance(variable, (str, list, dict, set, tuple)):
            return len(variable) == 0
        return False

    @keyword(name="Is Not Empty")
    def is_not_empty(self, variable: Any) -> bool:
        """
        Check if the variable is not None and not an empty collection.

        *Arguments:*
        - `variable`: The variable to check.

        *Returns:*
        - `bool`: True if the variable is not None and not empty, False otherwise.

        *Example (Robot Framework):*
        | ${is_not_empty}= | Is Not Empty | ${[1, 2, 3]} |
        | Should Be True | ${is_not_empty} |
        """
        return not self.is_empty(variable)

    @keyword(name="Delete Variable By Name")
    def delete_variable_by_name(self, variable_name, scope = 'test'):
        """
        Deletes a variable from the specified scope using its exact name.

        Arguments:
            variable_name: Name of the variable as a string (e.g., "a" or "${a}")
            scope: Scope of the variable to delete. Options are 'global', 'test', or 'local'.
                  Default is 'test'.
        """
        # Format the variable name properly
        var_name = str(variable_name)
        if not var_name.startswith(('$', '@', '&')):
            var_name = f"${{{var_name}}}"

        # Normalize scope to lowercase for case-insensitive comparison
        scope = scope.lower()

        try:
            # Now we have the proper variable name, try to delete it
            if scope == 'global':
                try:
                    # Check if the variable exists and then set to None
                    self.builtin.set_global_variable(var_name, None)
                    logger.info(f"Deleted global variable: {var_name}")
                except Exception as e:
                    logger.info(f"Global variable {var_name} not found to delete: {str(e)}")

            elif scope == 'test':
                try:
                    # Set to None which is the closest to deletion in Robot Framework
                    self.builtin.set_test_variable(var_name, None)
                    logger.info(f"Deleted test variable: {var_name}")
                except Exception as e:
                    logger.info(f"Test variable {var_name} not found to delete: {str(e)}")

            elif scope == 'local':
                try:
                    # Try to set the local variable to None
                    vars_namespace = self.builtin._variables
                    if hasattr(vars_namespace, 'set_local'):
                        # Extract variable name without ${}
                        name_without_prefix = var_name[ 2:-1 ] if var_name.startswith('${') and var_name.endswith(
                            '}') else var_name
                        vars_namespace.set_local(name_without_prefix, None)
                        logger.info(f"Deleted local variable: {var_name}")
                    else:
                        logger.info(f"Could not access local variable scope for: {var_name}")
                except Exception as e:
                    logger.info(f"Local variable {var_name} not found to delete: {str(e)}")

            else:
                raise ValueError(f"Invalid scope: {scope}. Use 'global', 'test', or 'local'.")

        except Exception as e:
            logger.error(f"Failed to delete variable '{var_name}' with scope '{scope}': {str(e)}")

    @keyword(name="Delete Variable")
    def delete_variable(self, var_value, scope = 'test'):
        """
        IMPORTANT: This keyword expects the actual variable NAME as a string, not the variable itself.

        For example:
        Delete Variable    a    test    # Deletes variable ${a}
        Delete Variable    my_var    global    # Deletes variable ${my_var}

        To delete using variable values, use Delete Variable By Value instead.

        Arguments:
            var_value: Name of the variable to delete as a string (without ${})
            scope: Scope of the variable to delete. Options are 'global', 'test', or 'local'.
                  Default is 'test'.
        """
        # Just call the by_name version since we expect a string name here
        return self.delete_variable_by_name(var_value, scope)

    @keyword(name="Delete Variable By Value")
    def delete_variable_by_value(self, value, scope = 'test'):
        """
        Attempt to find and delete a variable by its value.
        Note: This is not reliable as multiple variables could have the same value.

        Arguments:
            value: The value of the variable to find and delete
            scope: Scope of the variable to delete. Options are 'global', 'test', or 'local'.
                  Default is 'test'.
        """
        # Get all variables in the current scope
        all_vars = self.builtin.get_variables()

        # Search for variables with the matching value
        matching_vars = [ ]
        for name, var_value in all_vars.items():
            if str(var_value) == str(value):
                matching_vars.append(name)

        if not matching_vars:
            logger.info(f"No variables found with value: {value}")
            return

        # Delete all matching variables
        for var_name in matching_vars:
            # Skip internal variables that start with @
            if var_name.startswith('@'):
                continue

            formatted_name = f"${{{var_name}}}"
            logger.info(f"Found variable with matching value: {formatted_name}")
            self.delete_variable_by_name(formatted_name, scope)

    @keyword("Retrieve Variable Type")
    def retrieve_variable_type(self, variable):
        """
        Retrieve the type of the given variable as a string.

        Args:
            variable: The variable to check.

        Returns:
            str: The name of the variable's type.
        """
        return type(variable).__name__
