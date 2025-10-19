from robot.api import logger
from datetime import datetime
from tabulate import tabulate


class KeywordListener:
    ROBOT_LISTENER_API_VERSION = 3

    def __init__(self):
        # Per-test case metrics
        self.keyword_count = 0
        self.passed_keywords = 0
        self.failed_keywords = 0
        self.passed_critical_keywords = 0
        self.failed_critical_keywords = 0
        self.test_start_time = None
        self.test_end_time = None

        # Suite-level metrics
        self.suite_start_time = None
        self.suite_end_time = None
        self.total_test_cases = 0
        self.total_passed_tests = 0
        self.total_failed_tests = 0
        self.total_passed_critical_keywords = 0
        self.total_failed_critical_keywords = 0

    def start_suite(self, data, result):
        self.suite_name = getattr(data, 'name')
        self.suite_start_time = datetime.now()
        self.total_test_cases = 0
        self.total_passed_tests = 0
        self.total_failed_tests = 0
        self.total_passed_critical_keywords = 0
        self.total_failed_critical_keywords = 0

    def start_test(self, data, result):
        self.test_name = getattr(data, 'name')
        self.keyword_count = 0
        self.passed_keywords = 0
        self.failed_keywords = 0
        self.passed_critical_keywords = 0
        self.failed_critical_keywords = 0
        self.test_start_time = datetime.now()

    # def end_user_keyword(self, data, implementation, result):
    #     test_data = [
    #         [ "Keyword Name", getattr(result, 'kwname', None) ],
    #         [ "Keyword Source", str(implementation.source) ],
    #         [ "Keyword Start Time", str(result.starttime) ],
    #         [ "Keyword End Time", str(result.endtime) ],
    #         [ "Keyword Elapsed Time", str(result.elapsedtime) ],
    #         [ "Keyword Status", getattr(result, 'status', None) ],
    #         [ "Keyword Type", getattr(result, 'type', None) ],
    #         [ "Keyword Library", getattr(result, 'libname', None) ],
    #         [ "Keyword Line Number", getattr(result, 'lineno', None) ],
    #     ]
    #     test_table = tabulate(test_data, headers = [ "Keyword Information", "Value" ], tablefmt = "pretty")
    #     logger.console("\n[Keyword Summary]\n" + test_table)

    def start_keyword(self, data, result):
        self.keyword_count += 1

    def end_keyword(self, data, result):
        # Handle criticality based on keyword arguments
        critical_flag = "CRITICAL" in result.args or "critical" in result.args

        if result.status == "PASS":
            self.passed_keywords += 1
            if critical_flag:
                self.passed_critical_keywords += 1
        elif result.status == "FAIL":
            self.failed_keywords += 1
            if critical_flag:
                self.failed_critical_keywords += 1

    def end_test(self, data, result):
        self.test_end_time = datetime.now()
        test_duration = (self.test_end_time - self.test_start_time).total_seconds()

        # Log test case summary
        test_data = [
            [ "Test Name", self.test_name ],
            [ "Suite Name", result.parent.name ],
            [ "Test Status", result.status ],
            [ "Duration (seconds)", f"{test_duration:.2f}" ],
            [ "Keywords Executed", self.keyword_count ],
            [ "Keywords Passed", self.passed_keywords ],
            [ "Keywords Failed", self.failed_keywords ],
            [ "Critical Keywords Passed", self.passed_critical_keywords ],
            [ "Critical Keywords Failed", self.failed_critical_keywords ],
        ]
        test_table = tabulate(test_data, headers = [ "Metric", "Value" ], tablefmt = "pretty")
        logger.console("\n[Test Case Summary]\n" + test_table)

        # Update suite-level metrics
        self.total_test_cases += 1
        self.total_passed_critical_keywords += self.passed_critical_keywords
        self.total_failed_critical_keywords += self.failed_critical_keywords

        if result.status == "PASS":
            self.total_passed_tests += 1
        elif result.status == "FAIL":
            self.total_failed_tests += 1

    def end_suite(self, data, result):
        # Skip suite summary if running a single test case
        if len(result.tests) <= 1:
            return

        self.suite_end_time = datetime.now()
        suite_duration = (self.suite_end_time - self.suite_start_time).total_seconds()

        # Calculate percentages
        if self.total_test_cases > 0:
            pass_percentage = (self.total_passed_tests / self.total_test_cases) * 100
            fail_percentage = (self.total_failed_tests / self.total_test_cases) * 100
        else:
            pass_percentage = fail_percentage = 0.0

        # Log test suite summary
        suite_data = [
            [ "Suite Name", self.suite_name ],
            [ "Suite Path", data.source ],
            [ "Suite Status", result.status ],
            [ "Start Time", self.suite_start_time.strftime('%H:%M:%S') ],
            [ "End Time", self.suite_end_time.strftime('%H:%M:%S') ],
            [ "Duration (seconds)", f"{suite_duration:.2f}" ],
            [ "Total Test Cases", self.total_test_cases ],
            [ "Passed Test Cases", self.total_passed_tests ],
            [ "Failed Test Cases", self.total_failed_tests ],
            [ "Critical Keywords Passed", self.total_passed_critical_keywords ],
            [ "Critical Keywords Failed", self.total_failed_critical_keywords ],
            [ "Pass Percentage", f"{pass_percentage:.2f}%" ],
            [ "Fail Percentage", f"{fail_percentage:.2f}%" ],
        ]
        suite_table = tabulate(suite_data, headers = [ "Metric", "Value" ], tablefmt = "pretty")
        logger.console("\n[Test Suite Summary]\n" + suite_table)
