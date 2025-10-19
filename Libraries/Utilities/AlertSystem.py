import os
from robot.api import logger
from robot.api.deco import keyword, library
from robot.libraries.BuiltIn import BuiltIn
from Libraries.Utilities.PathExtractor import PathExtractor


@library(doc_format = 'ROBOT')
class AlertSystem:
    """
    A Robot Framework library for displaying customizable alerts in a web UI.

    This library provides keywords to display interactive, customizable alerts
    in the browser during test execution, which can be useful for debugging
    or highlighting important test steps.
    """

    def __init__(self):
        """
        Initialize the AlertSystem with optional path to JS file.

        The JavaScript file path is determined automatically using PathExtractor.
        """
        self.builtin = BuiltIn()
        BuiltIn().import_library('Browser')
        self.browser = BuiltIn().get_library_instance('Browser')
        self._resources_loaded_flag = False
        self.path_extractor = PathExtractor()
        # Set the JS file path
        self.js_file_path = self.path_extractor.get_project_directory() + '/Libraries/Scripts/alert_system.js'

        # Load the JS code from file
        self._js_code = self._load_js_code()

    def _load_js_code(self):
        """
        Load the JavaScript code from the file.

        Returns:
            str: The JavaScript code as a string
        """
        try:
            with open(self.js_file_path, 'r', encoding = 'utf-8') as file:
                js_code = file.read()
            logger.debug(f"Successfully loaded alert system JS from {self.js_file_path}")
            return js_code
        except Exception as e:
            error_msg = f"Failed to load JavaScript file from {self.js_file_path}: {e}"
            logger.error(error_msg)
            # Return a minimal JS that will show an error message if used
            return """(elements,arg)=>{
                console.error("Alert system JS file could not be loaded");
                window.showAlert = function(type, message, title) {
                    console.error("Alert system not properly loaded. Message was: " + message);
                    alert("Alert system error: " + message);
                };
                window.showGroupedAlert = window.showAlert;
                return false;
            };"""

    @keyword("Load Alert System Resources")
    def load_alert_system_resources(self, force_reload = False):
        """
        Loads alert CSS and JS into the current page by defining the `showAlert` function globally.

        Args:
            force_reload (bool, optional): Force reload even if already loaded. Default is False.
        """
        # Check if already loaded to avoid duplicates
        if not force_reload:
            check_js = """(elements,arg)=>{
                return typeof window.showAlert === 'function';
            }"""
            already_loaded = self.browser.evaluate_javascript('html', check_js, arg = None, all_elements = False)
            if already_loaded:
                logger.debug("Alert system resources already loaded, skipping.")
                self._resources_loaded_flag = True
                return

        # Reload the JS code in case the file has changed
        if force_reload:
            self._js_code = self._load_js_code()

        result = self.browser.evaluate_javascript('html', self._js_code, arg = None, all_elements = False)
        self._resources_loaded_flag = True
        logger.info("Alert system resources loaded successfully.")
        return result

    def _ensure_resources_loaded(self):
        """
        Private method to ensure alert resources are loaded before showing an alert.
        Returns True if resources were already loaded, False if they needed to be loaded.
        """
        check_js = """(elements,arg)=>{
            return typeof window.showAlert === 'function';
        }"""
        try:
            already_loaded = self.browser.evaluate_javascript('html', check_js, arg = None, all_elements = False)
            if not already_loaded:
                self.load_alert_system_resources()
                return False
            return True
        except Exception as e:
            logger.debug(f"Error checking if alert system is loaded: {e}")
            # If there's an error, try to load the resources
            self.load_alert_system_resources()
            return False

    @keyword("Add Custom Automation Alert")
    def add_custom_automation_alert(self, alert_title, alert_context, timeout = 5000, status_index = 0,
                                    context_direction = "ltr", alert_position = 5, show_countdown = False):
        """
        Displays a customizable alert on the screen. Automatically loads alert resources if needed.

        Args:
            alert_title (str): The title of the alert.
            alert_context (str): The main content or body of the alert.
            timeout (int, optional): Duration in milliseconds before the alert disappears. Default is 5000.
            status_index (int, optional):
                Alert type index (0: Success, 1: Error, 2: Info, 3: Warning, 4: Waiting, 5: Critical, 6: Debug).
                Default is 0.
            context_direction (str, optional): Text direction ("ltr" or "rtl"). Default is "ltr".
            alert_position (int, optional):
                Screen position index (0: Top-Left, 1: Top-Middle, 2: Top-Right, 3: Bottom-Left,
                4: Bottom-Middle, 5: Bottom-Right). Default is 5.
            show_countdown (bool, optional): Display a countdown timer showing seconds until alert closes.
                Default is False.
        """
        # Ensure resources are loaded
        self._ensure_resources_loaded()

        statuses = [ "success", "error", "info", "warning", "waiting", "critical", "debug" ]
        positions = [ "top-left", "top-middle", "top-right", "bottom-left", "bottom-middle", "bottom-right" ]

        status = statuses[ status_index ]
        position = positions[ alert_position ]
        args = [ status, alert_context, alert_title, timeout, context_direction, position, show_countdown ]
        js_code = """(elements,args)=>{
            return showAlert(args[0], args[1], args[2], args[3], args[4], args[5], args[6]);
        }
        """
        self.browser.evaluate_javascript('body', js_code,
                                         arg = args, all_elements = False)
        logger.info(f"Displayed alert: {alert_title} - {alert_context}")

    @keyword("Add Grouped Automation Alert")
    def add_grouped_automation_alert(self, alert_title, alert_context, timeout = 5000, status_index = 0,
                                     context_direction = "ltr", alert_position = 5, show_countdown = False):
        """
        Displays a customizable alert on the screen, grouping similar alerts together.
        Automatically loads alert resources if needed.

        Args:
            alert_title (str): The title of the alert.
            alert_context (str): The main content or body of the alert.
            timeout (int, optional): Duration in milliseconds before the alert disappears. Default is 5000.
            status_index (int, optional):
                Alert type index (0: Success, 1: Error, 2: Info, 3: Warning, 4: Waiting, 5: Critical, 6: Debug).
                Default is 0.
            context_direction (str, optional): Text direction ("ltr" or "rtl"). Default is "ltr".
            alert_position (int, optional):
                Screen position index (0: Top-Left, 1: Top-Middle, 2: Top-Right, 3: Bottom-Left,
                4: Bottom-Middle, 5: Bottom-Right). Default is 5.
            show_countdown (bool, optional): Display a countdown timer showing seconds until alert closes.
                Default is False.
        """
        # Ensure resources are loaded
        self._ensure_resources_loaded()

        statuses = [ "success", "error", "info", "warning", "waiting", "critical", "debug" ]
        positions = [ "top-left", "top-middle", "top-right", "bottom-left", "bottom-middle", "bottom-right" ]

        status = statuses[ status_index ]
        position = positions[ alert_position ]
        args = [ status, alert_context, alert_title, timeout, context_direction, position, show_countdown ]
        js_code = """(elements,args)=>{
            return showGroupedAlert(args[0], args[1], args[2], args[3], args[4], args[5], args[6]);
        }
        """
        self.browser.evaluate_javascript('body', js_code,
                                         arg = args, all_elements = False)
        logger.info(f"Displayed grouped alert: {alert_title} - {alert_context}")
