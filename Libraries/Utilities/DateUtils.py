from robot.api import logger
from robot.api.deco import keyword, library
from robot.libraries.String import String
from robot.libraries.Collections import Collections
from StringOperations import StringOperations
from MathOperations import MathOperations
from LogicalOperations import LogicalOperations
from robot.libraries.BuiltIn import BuiltIn


@library(doc_format='ROBOT')
class DateUtils:
    """
    DateUtils class for handling date and time operations in Robot Framework.

    This class provides keywords for date manipulation including:
    - Getting the current date/time
    - Modifying dates by adding or subtracting time values
    - Reformatting dates
    - Reversing date formats

    It leverages existing StringOperations, MathOperations, and LogicalOperations classes.
    """

    def __init__(self):
        # Import DateTime library and get an instance of it
        BuiltIn().import_library('DateTime')
        self.datetime_lib = BuiltIn().get_library_instance("DateTime")
        self.string_lib = String()
        self.collections_lib = Collections()
        self.string_ops = StringOperations()
        self.math_ops = MathOperations()
        self.logical_ops = LogicalOperations()
        self.builtin = BuiltIn()
        self.EMPTY = ""

    @keyword("Modify Today Date")
    def modify_today_date(self, action_value, action="Increment", reverse_date=False):
        """
        Get Today's Date Then Modify The Date By Either Add Or Subtract Days From Today's Date.

        Arguments:
            action_value: Time value to add or subtract (e.g., "1d", "2h")
            action: "Increment" or "Reduction" to add or subtract
            reverse_date: Whether to reverse the date format (e.g., from DD-MM-YYYY to YYYY-MM-DD)

        Returns:
            The modified date as a string
        """
        today_date = self.get_todays_date_and_or_time()

        modified_date = self.increment_or_reduction_given_date(
            given_date=today_date,
            action=action,
            action_value=action_value
        )

        reformatted_date = self.reformat_date(modified_date)

        if reverse_date:
            reformatted_date = self.reverse_data(original_date=reformatted_date)

        return reformatted_date

    @keyword("Get Todays Date And Or Time")
    def get_todays_date_and_or_time(self, date_only=False, time_only=False,
                                    date_format="%d.%m.%Y %H:%M", date_seperator="-"):
        """
        Use Get Current Date To Get Today's Date. You can get either the date or the time or both values.

        Arguments:
            date_only: Return only the date part if True
            time_only: Return only the time part if True
            date_format: The format to use for the date/time
            date_seperator: The separator to use in the date format

        Returns:
            The current date/time as a string
        """
        try:
            # Replace date separators in the format string
            date_format = self.string_lib.replace_string_using_regexp(
                date_format,
                "[.-/]",
                date_seperator,
                count=2
            )

            # Get current date with no timezone adjustment
            # Directly format it according to the requested format
            if date_only:
                optimized_date_format = self.string_lib.split_string(
                    date_format,
                    separator=" ",
                    max_split=1
                )
                return self.datetime_lib.get_current_date(
                    result_format=optimized_date_format[0]
                )
            elif time_only:
                optimized_date_format = self.string_lib.split_string(
                    date_format,
                    separator=" ",
                    max_split=1
                )
                return self.datetime_lib.get_current_date(
                    result_format=optimized_date_format[1]
                )
            else:
                # For both date and time, use the complete format
                return self.datetime_lib.get_current_date(
                    result_format=date_format
                )
        except Exception as e:
            logger.error(f"Error in get_todays_date_and_or_time: {str(e)}")
            # Fallback to basic format
            return self.datetime_lib.get_current_date()

    @keyword("Increment Or Reduction Given Date")
    def increment_or_reduction_given_date(self, given_date, action="Increment",
                                          action_value="1d", date_format=None):
        """
        Increment Or Reduction Given Date

        Main method that determines the type of date/time value and delegates to specialized methods.

        Accepted Action Values:
        days, day, d
        hours, hour, h
        minutes, minute, mins, min, m
        seconds, second, secs, sec, s
        milliseconds, millisecond, millis, ms
        microseconds, microsecond, us, μs (new in RF 6.0)
        nanoseconds, nanosecond, ns (new in RF 6.0)
        Example: 1 d, 7 s

        Arguments:
            given_date: The date to modify
            action: "Increment" or "Reduction"
            action_value: Value to add or subtract (e.g., "1d", "7s")
            date_format: Format for the output date

        Returns:
            The modified date
        """
        try:
            # Determine the type of date input
            if self._is_date_time(given_date):
                return self._handle_date_time(given_date, action, action_value, date_format)
            elif self._is_date_only(given_date):
                return self._handle_date_only(given_date, action, action_value, date_format)
            elif self._is_time_only(given_date):
                return self._handle_time_only(given_date, action, action_value, date_format)
            else:
                # Default case: treat as date-time
                return self._handle_date_time(given_date, action, action_value, date_format)
        except Exception as e:
            self.builtin.log(f"Error in increment_or_reduction_given_date: {str(e)}", level="ERROR")
            raise

    def _is_date_time(self, date_string):
        """Check if string has both date and time components."""
        # Check if string contains both date and time components
        import re
        # Match patterns like: 2025-03-07 00:00:00.000 or 2025-03-07 00:00:00
        date_time_pattern = r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}'
        return bool(re.match(date_time_pattern, date_string))

    def _is_date_only(self, date_string):
        """Check if string has only a date component."""
        import re
        # Match patterns like: 2025-03-07 or 07.03.2025 or 07/03/2025
        date_only_pattern = r'^(\d{4}-\d{2}-\d{2}|\d{2}[./-]\d{2}[./-]\d{4})$'
        return bool(re.match(date_only_pattern, date_string))

    def _is_time_only(self, time_string):
        """Check if string has only a time component."""
        import re
        # Match patterns like: 00:00:00 or 00:00
        time_only_pattern = r'^\d{2}:\d{2}(:\d{2})?$'
        return bool(re.match(time_only_pattern, time_string))

    def _parse_action_value(self, action_value):
        """Parse the action value into amount and unit."""
        import re
        match = re.match(r'^(\d+)([a-zA-Z]+)$', action_value)
        if not match:
            raise ValueError(f"Invalid action_value format: {action_value}")

        amount, unit = match.groups()
        amount = int(amount)

        # Map to standard unit names
        unit_map = {
            'd': 'days',
            'day': 'days',
            'days': 'days',
            'h': 'hours',
            'hour': 'hours',
            'hours': 'hours',
            'm': 'minutes',
            'min': 'minutes',
            'mins': 'minutes',
            'minute': 'minutes',
            'minutes': 'minutes',
            's': 'seconds',
            'sec': 'seconds',
            'secs': 'seconds',
            'second': 'seconds',
            'seconds': 'seconds'
        }

        if unit not in unit_map:
            raise ValueError(f"Unknown time unit: {unit}")

        return amount, unit_map[unit]

    def _handle_date_time(self, given_date, action, action_value, date_format=None):
        """Handle date-time values for both increment and reduction."""
        from datetime import datetime, timedelta

        # Parse the date-time string
        # Strip milliseconds if present
        if '.' in given_date:
            given_date = given_date.split('.')[0]

        # Parse to datetime object
        dt = datetime.strptime(given_date, "%Y-%m-%d %H:%M:%S")

        # Parse action value
        amount, unit = self._parse_action_value(action_value)

        # Create timedelta
        delta_args = {unit: amount}
        delta = timedelta(**delta_args)

        # Apply action
        if action == "Reduction":
            result_dt = dt - delta
        else:  # Increment
            result_dt = dt + delta

        # Format the result
        result_str = result_dt.strftime("%Y-%m-%d %H:%M:%S")

        if date_format:
            return self.datetime_lib.convert_date(result_str, date_format=date_format)
        return result_str

    def _handle_date_only(self, given_date, action, action_value, date_format=None):
        """Handle date-only values for both increment and reduction."""
        from datetime import datetime, timedelta

        # Convert different date formats to a standard format
        try:
            # Try YYYY-MM-DD format
            dt = datetime.strptime(given_date, "%Y-%m-%d")
        except ValueError:
            try:
                # Try DD.MM.YYYY format
                dt = datetime.strptime(given_date, "%d.%m.%Y")
            except ValueError:
                try:
                    # Try DD/MM/YYYY format
                    dt = datetime.strptime(given_date, "%d/%m/%Y")
                except ValueError:
                    raise ValueError(f"Unsupported date format: {given_date}")

        # Parse action value
        amount, unit = self._parse_action_value(action_value)

        # For date-only, only support day units
        if unit != 'days':
            raise ValueError(f"Only day units supported for date-only operations, got: {unit}")

        # Create timedelta
        delta = timedelta(days=amount)

        # Apply action
        if action == "Reduction":
            result_dt = dt - delta
        else:  # Increment
            result_dt = dt + delta

        # Format the result
        result_str = result_dt.strftime("%Y-%m-%d")

        if date_format:
            return self.datetime_lib.convert_date(result_str, date_format=date_format)
        return result_str

    def _handle_time_only(self, given_time, action, action_value, date_format=None):
        """Handle time-only values for both increment and reduction."""
        from datetime import datetime, timedelta

        # Parse the time string
        # Use a dummy date
        dummy_date = "2000-01-01 "

        # Handle different time formats
        if len(given_time) == 5:  # HH:MM
            dt = datetime.strptime(dummy_date + given_time, "%Y-%m-%d %H:%M")
        else:  # HH:MM:SS
            dt = datetime.strptime(dummy_date + given_time, "%Y-%m-%d %H:%M:%S")

        # Parse action value
        amount, unit = self._parse_action_value(action_value)

        # Create timedelta
        delta_args = {unit: amount}
        delta = timedelta(**delta_args)

        # Apply action
        if action == "Reduction":
            result_dt = dt - delta
        else:  # Increment
            result_dt = dt + delta

        # Format the result (time only)
        if len(given_time) == 5:  # HH:MM
            result_str = result_dt.strftime("%H:%M")
        else:  # HH:MM:SS
            result_str = result_dt.strftime("%H:%M:%S")

        if date_format:
            # Since this is time-only, we need to create a dummy date-time
            dummy_result = dummy_date.strip() + " " + result_str
            return self.datetime_lib.convert_date(dummy_result, date_format=date_format)
        return result_str

    @keyword("Reformat Date")
    def reformat_date(self, date_string, date_seperator="-"):
        """
        Get Date From DateTime Variable

        Arguments:
            date_string: The date string to reformat
            date_seperator: The separator to use in the date

        Returns:
            The reformatted date
        """
        try:
            # Using StringOperations to split the string
            date_parts = self.string_ops.string_to_list(date_string, " ")
            if date_parts and len(date_parts) > 0:
                return date_parts[0]
            return date_string
        except Exception as e:
            logger.error(f"Error in reformat_date: {str(e)}")
            return date_string

    @keyword("Get Date Or Time From DateTime String")
    def get_date_or_time_from_datetime_string(self, datetime_string, date_or_time="Date"):
        """
        Get Date Or Time From DateTime String

        Arguments:
            datetime_string: The datetime string to parse
            date_or_time: "Date" or "Time" to specify which part to return

        Returns:
            Either the date or time part of the datetime string
        """
        try:
            # Using StringOperations to split the string
            separated_date_time = self.string_ops.string_to_list(datetime_string, " ")

            if date_or_time == 'Date' and len(separated_date_time) > 0:
                return separated_date_time[0]
            elif date_or_time == 'Time' and len(separated_date_time) > 1:
                return separated_date_time[-1]
            return datetime_string
        except Exception as e:
            logger.error(f"Error in get_date_or_time_from_datetime_string: {str(e)}")
            return datetime_string

    @keyword("Reverse Data")
    def reverse_data(self, original_date, date_seperator="-"):
        """
        Reverse the order of elements in a date string

        Arguments:
            original_date: The date string to reverse
            date_seperator: The separator used in the date

        Returns:
            The reversed date string
        """
        try:
            # Using StringOperations to split and join
            date_as_list = self.string_ops.string_to_list(original_date, date_seperator)

            # Reverse the list
            self.collections_lib.reverse_list(date_as_list)

            # Join the list with the separator
            reversed_date = self.string_ops.list_to_string(date_as_list, date_seperator)

            return reversed_date
        except Exception as e:
            logger.error(f"Error in reverse_data: {str(e)}")
            return original_date
