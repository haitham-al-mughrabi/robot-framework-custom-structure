import uuid
from typing import Dict, Any, Optional, Union, Callable, List, Tuple
from robot.api.deco import keyword, library
from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from SessionManager import SessionManager
from RequestSender import RequestSender
from TokenManager import TokenManager
from ResponseHandler import ResponseHandler
from RequestUtils import RequestUtils


@library(doc_format = 'ROBOT', auto_keywords=True)
class RobotRequestsManager:
    """
    A wrapper for Robot Framework's RequestsLibrary that enhances session management.

    Features:
    - Session management (creation, deletion, updates)
    - Automatic retry for failed requests
    - Session expiry detection & auto-renewal
    - Global timeout for requests
    - Logging API requests & responses
    - JSON Schema validation for responses
    - Enhanced response objects with easy access to common attributes
    """

    def __init__(self, auto_json: bool = True, auto_log: bool = True, detailed_response: bool = True,
                 return_json: bool = True, token_endpoint: Optional[ str ] = None):
        """
        Initialize RequestsLibrary instance and session tracking.

        :param auto_json: Automatically parse JSON responses
        :param auto_log: Automatically log requests and responses
        :param detailed_response: Return detailed ResponseWrapper objects instead of raw responses
        :param return_json: When True, returns JSON for JSON responses (overrides detailed_response for JSON)
        :param token_endpoint: Endpoint for token validation/refresh (optional)
        """
        # Initialize the components
        self.session_manager = SessionManager()
        self.token_manager = TokenManager(token_endpoint)
        self.response_handler = ResponseHandler(auto_json, detailed_response, return_json)
        self.request_sender = RequestSender(self.session_manager, self.token_manager,
                                            self.response_handler, auto_log)
        self.utils = RequestUtils()

        # Configuration options
        self.auto_json = auto_json
        self.auto_log = auto_log
        self.detailed_response = detailed_response
        self.return_json = return_json

    @keyword("Set Response Handling Options")
    def set_response_handling_options(self, auto_json: bool = None, auto_log: bool = None,
                                      detailed_response: bool = None, return_json: bool = None):
        """
        Configure how responses are handled and returned.

        :param auto_json: Automatically parse JSON responses
        :param auto_log: Automatically log requests and responses
        :param detailed_response: Return detailed ResponseWrapper objects instead of raw responses
        :param return_json: When True, returns JSON for JSON responses (overrides detailed_response for JSON)
        """
        if auto_json is not None:
            self.auto_json = auto_json
            self.response_handler.auto_json = auto_json
        if auto_log is not None:
            self.auto_log = auto_log
            self.request_sender.auto_log = auto_log
        if detailed_response is not None:
            self.detailed_response = detailed_response
            self.response_handler.detailed_response = detailed_response
        if return_json is not None:
            self.return_json = return_json
            self.response_handler.return_json = return_json

        logger.info(f"Response handling options updated: auto_json={self.auto_json}, "
                    f"auto_log={self.auto_log}, detailed_response={self.detailed_response}, "
                    f"return_json={self.return_json}")

    # Session Management Methods
    @keyword("Create API Session")
    def create_session(self, alias, url, headers = None, **kwargs):
        """Creates a new API session and stores it for tracking."""
        return self.session_manager.create_session(alias, url, headers, **kwargs)

    @keyword("Create Random API Session")
    def create_random_session(self, url, headers = None, **kwargs):
        """Creates a session with a randomly generated alias."""
        return self.session_manager.create_random_session(url, headers, **kwargs)

    @keyword("Delete API Session")
    def delete_session(self, alias):
        """Deletes a specific API session."""
        return self.session_manager.delete_session(alias)

    @keyword("Delete All API Sessions")
    def delete_all_sessions(self):
        """Deletes all stored API sessions."""
        return self.session_manager.delete_all_sessions()

    @keyword("Update Session Headers")
    def update_session_headers(self, alias, new_headers):
        """Updates session headers dynamically."""
        return self.session_manager.update_session_headers(alias, new_headers)

    @keyword("Get API Session Details")
    def get_session_details(self, alias):
        """Retrieves the full details of a session."""
        return self.session_manager.get_session_details(alias)

    # Request Sending Methods - Unified under send_api_request
    @keyword("Send API Request")
    def send_api_request(self, method = None, alias = None, endpoint = None, url = None, **kwargs):
        """
        Unified method for sending API requests with comprehensive options.

        :param method: HTTP method (GET, POST, etc.)
        :param alias: The session alias (optional)
        :param endpoint: API endpoint (relative to base URL)
        :param url: Full URL for the request (when not using session)
        :param kwargs: Additional request parameters including:
            - max_retries: Maximum number of retries
            - delay: Time between retries
            - token: Authentication token
            - token_type: Type of token (default: Bearer)
            - token_check_on_failure: Whether to check/refresh token on failure
            - custom_headers: Headers for this request only
            - random_session: Create a random session if alias not provided
            - expected_status: Expected HTTP status code(s)
        """
        return self.request_sender.send_request(method, alias, endpoint, url, **kwargs)

    @keyword("Send Batch Requests")
    def send_batch_requests(self, requests_list, **kwargs):
        """
        Sends multiple API requests.

        :param requests_list: List of request dictionaries
        :param kwargs: Common parameters for all requests
        """
        return self.request_sender.send_batch_requests(requests_list, **kwargs)

    @keyword("Set Global API Timeout")
    def set_global_timeout(self, timeout_seconds):
        """Sets a global timeout for API requests."""
        self.request_sender.global_timeout = timeout_seconds
        logger.info(f"Global timeout set to {timeout_seconds} seconds")

    # Token Management Methods
    @keyword("Check Token Expiration")
    def check_token_expiration(self, alias):
        """Checks if the token in a session is expired."""
        headers = self.session_manager.get_session_headers(alias)
        return self.token_manager.validate_token(headers)

    @keyword("Update Session Token")
    def update_session_token(self, alias, new_token, token_type = "Bearer"):
        """Updates the authorization token for an existing session."""
        current_headers = self.session_manager.get_session_headers(alias)
        if current_headers:
            current_headers[ "Authorization" ] = f"{token_type} {new_token}"
            return self.session_manager.update_session_headers(alias, current_headers)
        return False

    @keyword("Refresh Session Token")
    def refresh_session_token(self, alias):
        """Attempts to refresh the token for a session."""
        headers = self.session_manager.get_session_headers(alias)
        if headers:
            new_token = self.token_manager.refresh_token(headers)
            if new_token:
                return self.update_session_token(alias, new_token)
        return False

    @keyword("Create API Session With Token")
    def create_session_with_token(self, alias, url, token, token_type = "Bearer", headers = None, **kwargs):
        """Creates a new API session with authentication token."""
        headers = headers or { }
        headers[ "Authorization" ] = f"{token_type} {token}"
        return self.session_manager.create_session(alias, url, headers = headers, **kwargs)

    @keyword("Set Token Endpoint")
    def set_token_endpoint(self, endpoint):
        """Set the endpoint used for token validation and refresh."""
        self.token_manager.token_endpoint = endpoint
        logger.info(f"Token endpoint set to: {endpoint}")

    # Response Handling Methods
    @keyword("Extract JSON From Response")
    def extract_json_from_response(self, response, json_path = None, default = None):
        """Extract JSON data or a specific value from a response."""
        return self.response_handler.extract_json(response, json_path, default)

    @keyword("Get Response Status Code")
    def get_response_status_code(self, response):
        """Get the status code from a response object."""
        return self.response_handler.get_status_code(response)

    @keyword("Get Response Headers")
    def get_response_headers(self, response, header_name = None):
        """Get headers from a response object."""
        return self.response_handler.get_headers(response, header_name)

    @keyword("Check Response Success")
    def check_response_success(self, response):
        """Check if a response indicates success."""
        return self.response_handler.check_success(response)

    @keyword("Get Response Cookies")
    def get_response_cookies(self, response, cookie_name = None):
        """Get cookies from a response object."""
        return self.response_handler.get_cookies(response, cookie_name)

    @keyword("Get Response Content Type")
    def get_response_content_type(self, response):
        """Get the Content-Type header from a response."""
        return self.response_handler.get_content_type(response)

    @keyword("Get Response Content")
    def get_response_content(self, response, as_text = True):
        """Get the content from a response."""
        return self.response_handler.get_content(response, as_text)

    @keyword("Get Response Elapsed Time")
    def get_response_elapsed_time(self, response):
        """Get the elapsed time of a request in seconds."""
        return self.response_handler.get_elapsed_time(response)

    @keyword("Validate API Response")
    def validate_response(self, response, schema):
        """Validates API response against a JSON schema."""
        return self.response_handler.validate_response(response, schema)

    @keyword("Log API Request")
    def log_api_request(self, alias, method, endpoint, response):
        """Logs API request and response."""
        return self.request_sender._log_api_request(alias, method, endpoint, response)

    # Wait Methods
    @keyword("Wait Until API Status")
    def wait_until_api_status(self, method, alias, endpoint, expected_status = 200, timeout = 60, interval = 5,
                              **kwargs):
        """Wait until an API endpoint returns an expected status code."""
        return self.request_sender.wait_until_status(method, alias, endpoint, expected_status,
                                                     timeout, interval, **kwargs)

    @keyword("Wait Until API Response")
    def wait_until_api_response(self, method, alias, endpoint, condition_func, timeout = 60, interval = 5, **kwargs):
        """Wait until an API endpoint returns a response that satisfies a condition."""
        return self.request_sender.wait_until_response(method, alias, endpoint, condition_func,
                                                       timeout, interval, **kwargs)

    @keyword("Wait Until JSON Path Value")
    def wait_until_json_path_value(self, method, alias, endpoint, json_path, expected_value, timeout = 60, interval = 5,
                                   **kwargs):
        """Wait until an API endpoint returns a specific value for a JSON path."""

        def check_json_path_value(response):
            actual_value = self.response_handler.extract_json(response, json_path)
            if actual_value == expected_value:
                return True
            logger.info(f"Waiting for {json_path} = {expected_value}, got {actual_value}")
            return False

        return self.wait_until_api_response(method, alias, endpoint, check_json_path_value,
                                            timeout, interval, **kwargs)
