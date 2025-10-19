from robot.api import logger
from tabulate import tabulate
from collections import defaultdict
from robot.libraries.BuiltIn import BuiltIn


class LocatorFailureListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        # Initialize a dictionary to store locator failure details
        self.failed_locators = defaultdict(lambda: { "count": 0, "keywords": [ ], "tests": [ ] })

    def end_keyword(self, name, attributes):
        """
        Triggered when a keyword finishes execution. Checks for failures and stores locator details.
        """
        if attributes.status == "FAIL":
            # Check if the keyword arguments contain a locator
            for arg in attributes.args:
                if self._is_locator(arg):
                    locator = arg

                    # Increment the count for the locator
                    self.failed_locators[ locator ][ "count" ] += 1

                    # Store the keyword name
                    if str(name) not in self.failed_locators[ locator ][ "keywords" ]:
                        self.failed_locators[ locator ][ "keywords" ].append(str(name))

                    # Store the current test name
                    current_test = BuiltIn().get_variable_value("${TEST NAME}")
                    if current_test and current_test not in self.failed_locators[ locator ][ "tests" ]:
                        self.failed_locators[ locator ][ "tests" ].append(current_test)

    def end_test(self, name, attributes):
        """
        Logs locator failures for the test case after it finishes.
        """
        if attributes.status == "FAIL" and self.failed_locators:
            self._log_locator_failures("Test Case Locator Failure Summary")

    def end_suite(self, name, attributes):
        """
        Logs locator failures for the entire test suite after it finishes.
        """
        if attributes.parent is None and self.failed_locators:
            self._log_locator_failures("Test Suite Locator Failure Summary")

    def close(self):
        """
        Logs locator failures at the end of the execution if running a module.
        """
        if self.failed_locators:
            self._log_locator_failures("Module Locator Failure Summary")

    def _log_locator_failures(self, title):
        """
        Helper method to log a summary of locator failures.
        """
        logger.console(f"\n[{title}]")
        summary_data = [ ]
        for locator, details in self.failed_locators.items():
            summary_data.append([
                locator,
                details[ "count" ],
                ", ".join(details[ "keywords" ]),
                ", ".join(details[ "tests" ]),
            ])
        summary_table = tabulate(
            summary_data,
            headers = [ "Locator", "Failure Count", "Keywords", "Tests" ],
            tablefmt = "pretty"
        )
        logger.console(summary_table)

    @staticmethod
    def _is_locator(arg):
        """
        Helper method to determine if an argument is a locator.
        Adjust logic to match your application's definition of a locator.
        """
        locator_prefixes = [ "//", "css:", "xpath:", "id:", "name:" ]
        return isinstance(arg, str) and any(arg.startswith(prefix) for prefix in locator_prefixes)
